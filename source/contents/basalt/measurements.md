<!-- #### Procesamiento de muestras -->

En un hilo separado al módulo de optical flow, corre el estimador de VIO
encargado de realizar el bundle adjustment sobre los cuadros y muestras de la
IMU recientes para estimar la pose. Este toma como entrada las muestras de la
IMU junto a los keypoints 2D detectados para cada imagen, o sea la salida del
módulo de optical flow. Este módulo es el que efectivamente realizará la
integración y optimización con toda la información recibida y producirá como
salida en una cola, la estimación de los estados del agente a localizar.

##### Inicialización y preintegración {#basalt-preintegration}

<!-- TODO: Acá la idea original era referenciar a la secciónimu_calibration.md
que dejé a medias en vez de mandar directamente al libro de Barfoot -->

Para comenzar, el hilo de procesamiento de este módulo espera a que la primera
muestra de la IMU arribe. Estas muestras son recibidas de forma raw y antes de
tratarlas, Basalt utiliza parámetros de calibración estáticos provistos por
archivos de configuración para corregirlas. La corrección ocurre con base al
modelo de calibración de IMU explicado en @barfootStateEstimationRobotics2017
secc. 6.4.4 sin considerar todavía los
parámetros de los procesos aleatorios detallados en la misma. Una particularidad
de Basalt, es que el acelerómetro es utilizado como origen del agente localizado
y, fundándose en esto, se fija su orientación. Es decir, no se aplica ningún
tipo de corrección de orientación al calibrar las muestras del acelerómetro.
Esto hace que la matriz de alineamiento para el acelerómetro tenga ceros en su
triángulo superior (ver @schubertBasaltTUMVI2018 secc. IV.B y
\Cref{app:imucalib-issue}).

Luego de recibir esta primer muestra de la IMU se comienza la ejecución del
bucle principal, el cual espera indefinidamente por resultados encolados por el
módulo de optical flow para realizar una iteración. El primer par de muestras de
cámaras junto a la primera muestra de la IMU posterior al par estéreo son
utilizados para inicializar el estado del agente en el primer cuadro. Esto es ya
que a cada cuadro se le asigna un estado que se compone de la posición,
orientación, velocidad y biases del giroscopio y acelerómetro que se estimaron
para tal cuadro. Notar que en Basalt, hablar de cuadros es equivalente a hablar
de instantes de tiempo, ya que los únicos puntos en el tiempo para los cuales el
sistema produce una pose estimada son
las timestamps del par estéreo de imágenes recibidas.

Para inicializar el primer estado se toman varias suposiciones. En particular,
se asume que el dispositivo comienza en la posición $(0, 0, 0)$ y sin
aceleración ni velocidad, esto permite utilizar el vector de aceleración
reportado por la muestra del acelerómetro como el vector de gravedad y computar
así la inclinación del agente. Notar que esta inclinación no es capaz de
informar la orientación de forma completa al no poder contemplar uno de los ejes
de rotación del cuerpo. Por esta razón es recomendable iniciar la corrida con el
agente rotado con su eje vertical paralelo al vector gravedad, esto hará
que Basalt compute la orientación identidad. Tal rotación suele corresponder con
la posición de reposo pensada por el fabricante, o al menos este ha sido el caso
en los dispositivos utilizados en este trabajo. Además, es conveniente
posicionar el agente mirando hacia “adelante” ajustando el _yaw_ [^wikipedia-roll-pitch-yaw], como el
usuario considere apropiado según su entorno.

[^wikipedia-roll-pitch-yaw]: Los términos _roll_, _pitch_ y _yaw_ provenientes de
la aeronáutica son muy utilizados para hablar de la orientación de un cuerpo:
<https://en.wikipedia.org/wiki/Aircraft_principal_axes>

<!-- TODO@correct: No supe explicar la inicialización de marg_data en este punto por que todavía no la había leído -->

<!-- TODO@maybe: explicar por qué no basta con el acelerómetro para definir la orientación completa con un grafico,
hablar del producto cruz entre g y +Z, tilt vs orientación -->

En instantes posteriores, o sea al recibir nuevas imágenes, se realiza la
llamada preintegración de muestras consecutivas de la IMU. Considerando que
estas muestras arriban a mayores frecuencias que las de las cámaras,
preintegrarlas es un proceso que intenta resumir las muestras entre los cuadros
a una única pseudo-muestra que sucede en los mismos instantes de tiempo que los
cuadros como se ve en el ejemplo de la \figref{fig:sample-frequencies}.

\fig{fig:sample-frequencies}{source/figures/sample-frequencies.pdf}{%
Ejemplo de frecuencias}{%
Frecuencia de distintos eventos para un ejemplo con cámaras a 30 fps y muestras
de la IMU a 150 Hz.
}

El proceso de preintegración es el siguiente. Dado el cuadro previo $i$ con
timestamp $t_i$ y el cuadro posterior $j$ con timestamp $t_j$, se intenta
computar una pseudo-muestra $\Delta \mathbf{s} = (\Delta \mathbf{R}, \Delta \mathbf{v},
\Delta \mathbf{p}) \in SO(3) \times \R^3 \times \R^3$ que representa cambios de orientación, velocidad y posición
respectivamente según las mediciones de la IMU que ocurrieron desde $t_i$ hasta
$t_j$. Para cada timestamp $t$ de la IMU tal que $t_i < t \leq t_j$ tenemos la
muestra de aceleración lineal $\mathbf{a}_t$ y de velocidad angular
$\mathbf{\upomega}_t$. Definimos entonces de forma recursiva la pseudo-muestra
$\Delta \mathbf{s}$ de la siguiente manera:

<!-- $$ -->

\begin{align}
\label{eq:imu-preintegration}
(\Delta \mathbf{R}_{t_i}, \Delta \mathbf{v}_{t_i}, \Delta
\mathbf{p}_{t_i}) & := (\mathbf{I}, \mathbf{0}, \mathbf{0})
\\
\Delta \mathbf{R}_{t+1} & := \Delta \mathbf{R}_t exp(\mathbf{\upomega}_{t+1} \Delta t)
\\
\Delta \mathbf{v}_{t+1} & := \Delta \mathbf{v}_t + \Delta{\mathbf{R}_t}
\mathbf{a}_{t+1} \Delta t
\\
\Delta \mathbf{p}_{t+1} & := \Delta \mathbf{p}_t + \Delta \mathbf{v}_t \Delta t
\\
\Delta \mathbf{s}_{t} & := (\Delta \mathbf{R}_{t}, \Delta \mathbf{v}_{t}, \Delta
\mathbf{p}_{t})
\\
\Delta \mathbf{s} & := \Delta \mathbf{s}_{t_j}
\end{align}

<!-- $$ -->

Es destacable mencionar que este tipo de preintegración es también utilizado
por los otros sistemas estudiados Kimera y ORB-SLAM3. La ventaja que presenta es
que sus características son bien conocidas gracias al trabajo de
@forsterOnManifoldPreintegrationRealTime2017 y las expresiones necesarias para
el cómputo de residuales, como sus jacobianos, son cerradas y fueron derivadas
de forma ejemplar en dicho trabajo.

Entonces, con esta muestra preintegrada junto a los datos del nuevo cuadro (sus
keypoints), se procede a la etapa de `measure` del módulo de VIO. Aquí lo
primero que se hace es predecir que el estado de este nuevo instante estará
basado en el estado del instante anterior más la adición de las muestras
preintegradas de la IMU. El resto de la etapa de `measure` se basa en el manejo
y actualización de la base de datos de los puntos de interés en 3D, o
_landmarks_, y sus _observaciones_, junto a algo que, en Basalt, está fuertemente
ligado: la toma de cuadros clave, o _keyframes_.

##### Base de datos de landmarks

<!-- #define MN_CAMERA_DISTORTIONS %\
Detallaremos en la \Cref{sec:data-characteristics} este tipo de distorsiones.
-->

Recordemos que el módulo de optical flow encuentra keypoints en cada cuadro,
esto es, una landmark o punto de interés en la escena 3D proyectada sobre el
plano de la imagen 2D. Más aún este módulo era capaz de hacer el seguimiento de
keypoints similares mediante optical flow, es decir, de keypoints que observan
la misma landmark. Parte de nuestro objetivo entonces será triangular las
posiciones de estas landmarks considerando las observaciones tomadas.
Consideremos además la naturaleza altamente ruidosa de estas observaciones, con
landmarks que aparecen y desaparecen de la visión de los cuadros por múltiples
razones como: ser ocluidas por objetos en el entorno, ser distorsionadas por el
ángulo del observador, distorsiones inherentes de los sensores ópticos\marginnote{MN_CAMERA_DISTORTIONS} como el
motion blur, la sobreexposición, el ruido introducido por la ganancia del amplificador de señal
digital, o simplemente porque dejan de estar en el campo de visión de las
cámaras. Por estas razones entonces, será fundamental la correcta gestión de la
información de las landmarks y sus observaciones. En Basalt, la clase que se
encarga de esto es la `LandmarkDatabase` con la estructura como se define en el \Cref{lst:basalt-defs}.

\clearpage

```{#lst:basalt-defs .cpp caption="Estructuras de Basalt"}
class LandmarkDatabase {
  map<LandmarkId, Landmark> landmarks;
  map<FrameId, map<FrameId, Keypoint>> observations;
}

class Landmark {
 FrameId keyframe;
 Vector2 direction;
 double inverse_distance;
}

class Keypoint {
  LandmarkId landmark_id;
  Vector2 position;
}
```

En la implementación de este Módulo, los términos de keypoint y landmark tienden
a utilizarse de forma intercambiable, significando keypoint algo distinto a lo
que era en el módulo de optical flow. Para evitar confusión, se han diferenciado
los términos de manera explícita en el pseudo código anterior. `Landmark` se
utilizará para referirse al punto de interés en la escena tridimensional,
mientras que `Keypoint` será un punto 2D que observa la proyección de una
landmark definida por `landmark_id`. Entonces la `LandmarkDatabase` es
simplemente una colección de todas las `landmarks` de interés y de los keypoints
que la observaron en `observations`.

Una `Landmark` surge de un keypoint observado en el módulo de optical flow en
algún cuadro y comparte el mismo identificador. Explicaremos los campos
`direction` e `inverse_distance` que determinan la posición en 3D de la misma
más adelante. Un cuadro se identifica tanto por la timestamp en el que fue
tomado como por cuál de las dos cámaras lo tomó; `FrameId` tiene esta
información. Una landmark existe en referencia a un cuadro, y un cuadro que es
referenciado por landmarks debe ser un keyframe por la implementación; decimos
que el keyframe aloja estas landmarks. Una observación en `observations` tiene
entonces un mapeo de keyframes a los `Keypoints` que observan a las landmarks
alojadas en el keyframe. Un `Keypoint` es reconocido en un cuadro particular, y
solo tiene sentido como coordenadas en ese cuadro, es esto lo que representa el
segundo `FrameId` de la definición de `observations`.

Habiendo dicho esto, al recibir un nuevo cuadro, `measure` simplemente recorre
todas las observaciones o `Keypoint`s que este trae y se añaden a la base de
datos las observaciones de landmarks ya existente en la misma. Observaciones de
landmarks no registradas en la base de datos se guardan para poder determinar si
el módulo amerita la toma de un nuevo keyframe.

##### Keyframes

En contraste con sistemas como Kimera y ORB-SLAM3 que tienen condiciones más
intrincadas, en Basalt, la heurística para decidir si el cuadro actual será un
keyframe es muy sencilla: si _más del 30% de las observaciones del cuadro actual
corresponden a landmarks no registradas y han pasado más de, por defecto, 5
cuadros consecutivos que no fueron keyframes_, el cuadro actual será tomado como
un keyframe. La toma de keyframes es lo que registra nuevas landmarks a la base
de datos y realiza la estimación inicial de su posición.

En primer lugar, todas las observaciones _“desconectadas”_ correspondientes al
30% o más anterior que no correspondían a ninguna landmark, intentarán ser
registradas en la base de datos. Para esto es necesario poder encontrar una
segunda observación con la que realizar la triangulación y poder así estimar la
posición tridimensional de la landmark al registrarla.

Se tiene entonces que para cada observación desconectada $\mathbf{p}_h \in \R^2$
producida por la cámara $h$ del keyframe se recorrerán todos los cuadros desde
el último keyframe, buscando por una segunda observación $\mathbf{p}_t \in \R^2$
de esta landmark producida en alguna cámara $t$. En caso de encontrarla se
continúa de la siguiente manera:\newline

- La cámara $h$ del keyframe tiene una pose estimada para la IMU en esa timestamp
  que denominaremos $\mathbf{T}_{i_h} \in SE(3)$. Similarmente tendremos
  $\mathbf{T}_{i_t}$ para la cámara $t$.

- A su vez como los parámetros de calibración son estáticos y conocidos,
  tenemos la función de proyección $\pi_h$, sus parámetros intrínsecos
  $\mathbf{i}_h$ y la pose relativa $\mathbf{T}_{i_h c_h} \in SE(3)$ de la cámara $h$ respecto a la IMU. Similarmente con
  $\pi_t$, $\mathbf{i}_t$ y $\mathbf{T}_{i_t c_t}$ para la cámara $t$.

- Podemos ahora desproyectar $\mathbf{p}_h$ y $\mathbf{p}_t$ a sus respectivas
  proyecciones (rayos) estimados $\mathbf{p}'_h := \pi^{-1}_h(\mathbf{p}_h, \mathbf{i}_h)$
  y $\mathbf{p}'_t := \pi^{-1}_t(\mathbf{p}_t, \mathbf{i}_t)$ con $\mathbf{p}'_h,
  \mathbf{p}'_t \in \R^3$ en coordenadas homogéneas.

- Computamos ahora la transformación de la IMU de $h$ a la IMU de $t$ dada por
  $\mathbf{T}_{i_h i_t} := \mathbf{T}_{i_h}^{-1} \mathbf{T}_{i_t}$

- Luego podemos tener la transformación de la cámara $h$ a $t$ con
  $\mathbf{T}_{c_h c_t} := \mathbf{T}_{i_h c_h}^{-1} \mathbf{T}_{i_h i_t}
\mathbf{T}_{i_t c_t}$

- Finalmente con estos tres datos $\mathbf{p}'_h$, $\mathbf{p}'_t$ y
  $\mathbf{T}_{c_h c_t}$ es posible triangular el punto 3D resultante de la
  forma descrita en @hartleyMultipleViewGeometry2004 Cap. 12. Cabe aclarar que
  se necesitará utilizar cuadrados mínimos lineales para obtener el punto 3D
  final ya que los rayos proyectados provienen de mediciones ruidosas y
  usualmente no se alinearan de forma perfecta. Obtendremos el punto de la
  escena en coordenadas homogéneas en $\R^4$ con el cuarto componente
  representando el inverso de la distancia entre la cámara y el punto de
  interés, mientras que los tres primeros componentes corresponden al
  _bearing vector_, es decir, un vector unitario que determina la dirección
  desde la cámara hacia la landmark.\newline

<!-- TODO@def: distancia inversa: ver paper referenciado en basalt [6]: Inverse depth parametrization
for monocular SLAM -->
<!-- TODO@def: Este último punto está raro por que no entendía bien de lo que
estaba hablando -->
<!-- TODO@def: bearing vector -->
<!-- TODO@def: la sección "DLT con SVD" no existe. Buscar DLT triangulation with SVD,
quizás ver el apendix de multiple view geometry que se veía bueno -->
<!-- TODO@def: que son coordenadas homogéneas. Supongo que se explicaría casi por
su cuenta en la sección "DLT con SVD" cuando se explicar el resultado de la triangulación -->

Un detalle a considerar es que Basalt comprueba que la distancia relativa entre
los dos cuadros, la _baseline_, sea lo suficientemente grande para considerar la
triangulación exitosa, de lo contrario se busca un nuevo cuadro para comparar
con el keyframe. Esta comprobación se reduce a revisar que la norma del vector
de traslación contenido en $\mathbf{T}_{c_h c_t}$ sea de, por defecto, más
de 5 cm.

Como se ve en la definición de `Landmark`, la posición 3D de estos puntos de
interés no se almacena exactamente de la misma forma que la triangulación los
produce. En particular, no se almacena el bearing vector directamente, sino que
se utiliza un punto 2D más compacto `direction` que lo codifica (para esto se
utiliza una _proyección estereográfica_ como se explica en la
\figref{fig:stereographic-projection}) junto a `inverse_distance`, la distancia inversa
a este punto producto de la triangulación, de esta forma la posición de la
landmark queda ligada al keyframe que la aloja.

\fig{fig:stereographic-projection}{source/figures/stereographic-projection.pdf}{Proyección estereográfica}{%
Interpretación geométrica de la proyección estereográfica utilizada para
representar bearing vectors. Las coordenadas definidas por la propiedad \mono{Vector2
direction} en \mono{Landmark} definen un punto en el plano $XY$ ($Z=0$) mostrado en azul. Para
obtener el vector unitario correspondiente, se traza una línea desde el punto
$(0,\ 0,\ -1)^T$ hacia \mono{direction} en el plano $XY$. El vector en el que esta línea
interseca a la esfera unitaria será el bearing vector codificado. Se muestran
tres ejemplos en rojo, verde y amarillo, con líneas punteadas que representan
las líneas trazadas y flechas representando los bearing vectors obtenidos.
}

Si todos los procedimientos relacionados con la triangulación de estos dos cuadros
fueron correctos, se almacena la landmark nueva en la base de datos. De haber
otras observaciones de esta landmark no se utilizan todavía para añadir
información a su posición, sino que simplemente se añaden las observaciones
para uso futuro.
