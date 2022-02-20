<!-- TODO@high: este archivo tiene muchos TODOs pero basicamente lo que le hace falta
es una buena proofread y arreglar los errores que se detecten ahí -->

<!-- TODO@high@def: explicar bundle adjustment (en el paper de s-ptam hay alta explicación de una o dos oraciones) -->
<!-- TODO@high@def: que es motion blur -->
<!-- TODO@high@def: Estoy implicitamente hablando de un optimizador, cuando hablo de factor graphs? -->
<!-- TODO@high@def: Explicar factores no-lineales, o almenos decir que no se explican -->
<!-- TODO@high@def: Que son features? -->
<!-- TODO@high@def: Que es loop closing? -->
<!-- TODO@high@def: Que es OpenCV -->
<!-- TODO@high@def: Que son grafos de poses, factor graphs, y factores -->
<!-- TODO@high@def: VIO habla acerca de componentes: (patch tracking, landmark
representation, first-estimate Jacobians, marginalization
scheme) que podría ser interesante discutir -->
<!-- TODO: Mencionar que TUM lo desarrolla y las personas que lo mantienen -->
<!-- TODO@high@def: Que es cuadrados minimos -->
<!-- TODO@high@def: levenverg-marquard is also in use (see vio_lm_lambda_initial), I might need to explain it -->
<!-- TODO@high@def: que son SE(2), SO(3) etc: ver https://ethaneade.com/ -->
<!-- TODO@high@ref: Checkear que los 6 papers de basalt esten siendo citados -->
<!-- TODO@high@ref: Los papers de orbslam y kimera deberían estar citados -->
<!-- TODO@high@def: que es el acrónimo VIO? -->

# Implementación de Basalt

## Problemáticas preliminares

Un problema central en este tipo de sistemas es el de poder generar un mapa y
una trayectoria que sea _globalmente consistente_. Con esto nos referimos a que
nuevas mediciones tengan en cuenta todas las mediciones anteriores en el
sistema. Una forma ingenua de encarar este problema sería realizando _bundle
adjustment_ sobre todas las imágenes capturadas a lo largo de una corrida,
integrando de alguna forma todas las mediciones provenientes de la IMU.
Desafortunadamente, este método excede rápidamente cualquier capacidad de
cómputo de la que dispongamos, y aún más teniendo en cuenta que nuestro objetivo
es localizar en tiempo real al dispositivo de XR.

Por esta razón, es usual recurrir a distintas formas de reducir la complejidad
del problema. Para realizar _odometría visual-inercial (VIO)_, es común que
se ejecute la función de optimización sobre una _ventana local_ de cuadros y
muestras recientemente capturadas, ignorando muestras históricas y acumulando
error en las estimaciones a lo largo del tiempo. Además, este enfoque tiene la
problemática añadida de que una porción significativa de los fotogramas
capturados tienen posiciones similares que no añaden información al estimador, o
incluso que algunos fotogramas puedan ser de baja calidad por contener _motion
blur_ u otro tipo de anomalías. Por otro lado, soluciones que intenta realizar
_mapeo visual-inercial_ realizan el bundle adjustment sin utilizar todas las
imágenes capturadas, si no que se limitan a la utilización de algunos fotogramas
clave, o _keyframes_ elegidos mediante criterios que priorizan cuadros nítidos y
con distancias (_baselines_) prudenciales entre ellos.

Como las muestras de IMU vienen a altas frecuencias, es común que estas se pre
integren de forma tal de combinar muestras simultáneas entre dos keyframes en
una única entrada del optimizador. Sin embargo, un problema en el que esta
integración incurre, es que las mediciones de las IMU son altamente ruidosas, y
acumularlas durante tiempos prolongados acumula también cantidades
significativas de error. Este factor nos limita el tiempo que puede transcurrir
entre dos keyframes; como ejemplo en @mur-artalVisualInertialMonocularSLAM2017
se habla de keyframes que no pueden tener más de 0,5 segundos entre sí. A su
vez, tener keyframes a muy bajas frecuencias afecta la calidad de las
estimaciones de velocidad y biases; estos últimos son offsets de medición
inherentemente variables de los acelerómetros y giroscopios a los que es
necesario estimar para compensar por ellos en la medición final.

## Propuesta

La novedad de Basalt es que formula el mapeo visual-inercial como un problema de
bundle adjustment con mediciones visuales e inerciales a altas frecuencias.
Utiliza un _grafo de factores_ similarmente a otros sistemas, también llamado
_grafo de poses_ en este contexto por contener poses a estimar como nodos. En
lugar de utilizar todos los fotogramas se propone realizar la optimización en
dos capas. La capa de VIO, emplea un sistema de odometría visual-inercial, que
ya de por sí supera a otros sistemas del mismo tipo, proveyendo estimaciones de
movimiento a la misma frecuencia que el sensor de la cámara provee imágenes.
Luego, se seleccionan keyframes y se introducen _factores no-lineales_
entre estos que estiman la diferencia de posición relativa entre estos.
Estos dos factores, keyframes y poses relativas, se utilizan en la capa de
bundle-adjustment global.

La capa de VIO, utiliza features que son rápidas y buenas para tracking
(_optical flow_), mientras que en la capa de mapeo se usan features adecuadas
para _loop closing_ que son indiferentes a las condiciones de luz o al punto de
vista de la cámara. De esta forma tenemos un sistema que es capaz de utilizar
las mediciones a alta frecuencias de los sensores y al mismo tiempo tiene la
capacidad de detectar a frecuencias más bajas cuando se está en ubicaciones ya
visitadas, obteniendo así un mapa que es globalmente consistente. Además, el
problema de optimización se reduce, ya que a diferencia de otros sistemas, no es
necesario estimar velocidades ni biases.

## Implementación

A continuación se describe la arquitectura e implementación de Basalt de una
manera más detallada. Esta sección surge directamente de la lectura del código
fuente del sistema e intenta proveer detalles más bien pragmáticos que se
encuentran en el mismo, pero que pueden quedar escondidos en publicaciones de
más alto nivel. A su vez, se toman ciertas licencias literarias que deberían
ayudar al entendimiento y que no son posibles a la hora de escribir código.

### Odometría visual-inercial

Cómo vimos en la introducción, el funcionamiento de Basalt se divide en dos
etapas. La primera etapa de odometría visual-inercial (VIO), en el cual se
emplea un sistema de VIO que supera a sistemas equivalentes de vanguardia
mientras que la segunda etapa de mapeo visual-inercial (VIM), toma keyframes
producidos por la capa de VIO y ejecuta un algoritmo de _bundle adjustment_ para
obtener un mapa global consistente. Algo que no se mencionó en la introducción
es que estas dos capas son completamente independientes. En una corrida usual de
un dataset, lo que se realiza es la ejecución pura y exclusiva del sistema VIO y
es este el que decide y almacena persistentemente qué cuadros y con qué
información el sistema de VIM, de ejecutarse, debería utilizar al realizar el
proceso de _bundle adjustment_.

Esta sección explora los componentes fundamentales de la capa de VIO: _optical
flow_, _bundle adjustment visual-inercial_ y finalmente el proceso de
_optimización y de marginalización parcial_.

#### Optical flow

<!-- TODO@fig: algún gráfico que represente lo que le entra al módulo y lo que
sale, lo mismo para todo el pipeline de VIO, y lo mismo para todo Basalt -->

El módulo de VIO toma dos tipos de entrada, una de ellas son las muestras raw de
la IMU; y la otra, contra intuitivamente, no son las imágenes raw provenientes
de las cámaras, sino que son los _keypoints_ resultantes de ellas. Recordemos
que los keypoints no son más que la ubicación y rotación en dos dimensiones
sobre el plano de la imagen de las _features_ detectadas. Las features a su vez
son la representación de los puntos de interés o _landmarks_ de la escena
tridimensional proyectados sobre las imágenes. El proceso de detectar features,
computar su transformación entre distintos cuadros, y producir los keypoints de
entrada para el módulo de VIO, está a cargo del módulo de _optical flow_ (o
_flujo óptico_). Cabe aclarar que optical flow es el nombre que recibe tanto el
campo vectorial que representa el movimiento aparente de puntos entre dos
imágenes, como el proceso de estimarlo. Este puede ser denso, si se considera el
flujo de todos los píxeles, o no (_sparse_) si solo se computa el flujo de
algunos keypoints como en el caso que veremos.

El [módulo][`frametoframeopticalflow`] de optical flow corre en un thread
individual y es por donde las muestras del par de cámaras estéreo ingresan al
pipeline de Basalt. Inicialmente se genera una representación piramidal de las
imágenes, o también llamada de _mipmaps_, esta es una forma tradicional
[@williamsPyramidalParametrics1983] de almacenar una imagen en memoria junto a versiones
reescaladas de la misma (Fig. \figref{fig:mipmap}). Los mipmaps tienen múltiples utilidades en
computación gráfica (e.g., _filtrado trilineal_, _LODs_, reducción de
_patrones moiré_) pero en el caso de Basalt serán utilizados para darle robustez
al algoritmo de seguimiento de features (_feature tracking_).

[`frametoframeopticalflow`]: TODO@high

\fig{fig:mipmap}{source/figures/mipmap.jpg}{Mipmaps}{%
Representación piramidal (mipmaps) de un cuadro del conjunto de datos EuRoC.
}

Posteriormente se realiza la detección de features nuevas sobre las imágenes
utilizando el algoritmo _FAST_ [@rostenFasterBetterMachine2010a] para detección
de esquinas implementado sobre OpenCV. Aquí es notable
aclarar que Basalt es uno de los sistemas que menos depende de OpenCV, ya que
tiende a re implementar muchas de las técnicas y algoritmia de forma
especializada y, como veremos en otros módulos, otras tareas razonablemente
complejas como la optimización de grafos de poses se implementan también dentro
del proyecto y sin recurrir a librerías externas. Esta es una de las varias
razones por las que este sistema logra tan buen rendimiento, ya que las
librerías externas suelen tener campos y comprobaciones dedicadas al caso
general del problema que intenta solucionar, mientras que Basalt puede
prescindir de todas las que no apliquen al problema de VIO. Siguiendo con la
detección de features, una heurística particular de Basalt es la división del
cuadro completo en celdas de tamaño configurable (por defecto 50 por 50 píxeles)
en donde se detectan las nuevas features, por celda solo se conserva la feature
de mejor calidad o con mejor _respuesta (response)_ (aunque la cantidad a
conservar es también configurable), y siempre que la celda tenga alguna feature
localizada de frames anteriores, no se intenta detectar nuevas. Esto contrasta
con sistemas como Kimera-VIO que corren la detección FAST sobre el cuadro entero
y evitan la redetección mediante el uso de _máscaras_ que le instruyen al
algoritmo a obviar esas secciones. Desafortunadamente la construcción de tales
máscaras suele ser costosa y la heurística de Basalt, a pesar de desperdiciar
espacio por no permitir la detección de nuevas características entre celdas, es
más eficiente ya que en situaciones comunes se logran detectar una cantidad
razonable de features sin problemas. Esta detección de features nuevas se
realiza unicamente sobre la primera cámara (usualmente la izquierda), mientras
que en la otra cámara se reutiliza el método de seguimiento de keypoints que se
describe a continuación.

<!-- TODO@fig: Agregar imágenes de los parches, de la detección de features, del optical flow -->

En cada instante de tiempo que entran un nuevo par de imágenes se tiene acceso a
toda la información recolectada del instante anterior, en particular a sus
keypoints. Una suposición razonable es que las imágenes correspondientes a este
nuevo instante van a compartir mucho de los keypoints con las imágenes
anteriores y en posiciones similares. En base a esa suposición Basalt logra
ahorrarse tener que volver a detectar features de la imagen con FAST y en cambio
el problema se transforma en, dado una imagen anterior (inicial), sus keypoints
y una imagen nueva (objetivo), estimar donde ocurren esos mismos keypoints en la
imagen nueva. Para esto, por cada keypoint anterior, se genera un parche
$\Omega$ alrededor de su ubicación de, por defecto, 52 coordenadas de píxeles
(i.e., un círculo rasterizado en un bloque de 8 por 8 píxeles). Considerando
entonces que este parche debería estar en la imagen nueva en coordenadas
cercanas a las del keypoint anterior, queremos encontrar la transformación $T
\in SE(2)$ que le ocurrió al parche, y por ende al nuevo keypoint que se
encontraría en el centro de este nuevo parche. Basalt emplea entonces
optimización por cuadrados mínimos mediante el algoritmo iterativo de
Gauss-Newton para encontrar $T$ utilizando un residual $r$ con:

<!-- TODO@correct: Realmente es gauss newton lo que se hace? ver optical_flow_max_iterations -->
<!-- TODO@high@correct: Not quite, es inverse-compositional method, que es un gauss newton
sobre algo un poco distinto: https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0910/zhao.pdf
por eso aparece el hessiano y cosas de esa pinta -->
<!-- TODO: Mencionar ZNCC como norma no utilizada: https://martin-thoma.com/zero-mean-normalized-cross-correlation/ -->

$$
r_i =
  \frac{I_{t + 1}(\mathbf{T} \mathbf{x}_i)}{\overline{I_{t + 1}}} -
  \frac{I_{t}(\mathbf{x}_i)}{\overline{I_{t}}}
  \ \ \ \ \forall \mathbf{x}_i \in \Omega
$$

con $I_t(\mathbf{x})$ la intensidad de la imagen anterior en el pixel ubicado en
las coordenadas $\mathbf{x}$ (análogamente $I_{t + 1}(\mathbf{x})$ para la
imagen objetivo); y $\overline{I_{t}}$ siendo la intensidad media del parche
$\Omega$ en la imagen inicial (análogamente $\overline{I_{t + 1}}$ para la
imagen objetivo y el parche transformado $\mathbf{T}\Omega$). Notar que al
normalizar las intensidades obtenemos un valor que es invariante incluso ante
cambios de iluminación.

Los detalles del cálculo de gradientes y jacobianos están basados en el método
de @lucasIterativeImageRegistration1981 para tracking de features (_KLT_). El
uso adicional de mipmaps sobre KLT fue originalmente expuesto en
@bouguetPyramidalImplementationLucas1999.

<!-- TODO@def: "asegurar que la estimacion fue exitosa" == outlier filtering.
Quizás hablar un poco de eso -->

Para asegurar que la estimación fue exitosa, se invierte el problema y se
intenta trackear desde la imagen nueva hacia la inicial y, si el resultados está
muy alejado de la posición inicial, el nuevo keypoint se considera inválido y se
descarta. Otro detalle a aclarar es que, recordando que la detección de features
con FAST solo ocurre en las imágenes de una de las cámaras, es posible ahora
entender que las features en la segunda cámara son "detectadas" con este método,
es decir, simplemente se considera la imagen de la segunda cámara en el mismo
instante de tiempo como la imagen objetivo.

Finalmente, el último de los pasos que ocurre cuando el módulo de optical flow
procesa un cuadro es el de filtrado de keypoints, en el cual se desproyectan los
keypoints a posiciones en la escena tridimensional y en caso de que el error
epipolar supere cierto umbral, estos keypoints serán descartados.

<!-- TODO@high@def: Que es la desproyección -->
<!-- TODO@high@def: Qué es el error epipolar -->

#### Bundle adjustment visual-inercial

<!-- Cosas que tienen que estar:
- [ ] pi es estático (no autocalibration comparado a openvins)
- [ ] se estima la pose del IMU
- [ ] el estado es sk (frame_poses?), sf (frame_states), sl (lmdb)
- [ ] "representation of unit vectors in 3D" stereographic projection
- [ ] "reprojection error"
 -->

<!-- TODO@high@def: Qué es bundle adjustment -->

En un hilo separado al módulo de optical flow, corre el estimador de VIO
encargado de realizar en bundle adjustment sobre los cuadros y muestras de la
IMU recientes para estimar la pose. Este toma como entrada las muestras de la
IMU junto a los keypoints 2D detectados para cada imagen, o sea la salida del
módulo de optical flow. Este módulo es el que efectivamente realizará la
integración y optimización con toda la información recibida y producirá como
salida en una cola, la estimación de los estados del agente a localizar.

##### Inicialización y pre-integración {#basalt-preintegration}

<!-- TODO@def: referencia a la sección "Calibración de IMU", escribirla, referenciarla -->

Para comenzar, el hilo de procesamiento de este módulo espera a que la primera
muestra de la IMU arribe. Estas muestras son recibidas de forma raw y antes de
tratarlas, Basalt utiliza los parámetros de calibración estáticos provistos por
archivos de configuración para corregirlas. La corrección, o calibración, ocurre
como se explica en la sección de "Calibración de IMU" sin considerar todavía los
parámetros de los procesos aleatorios detallados en la misma. Una particularidad
de Basalt, es que el acelerómetro es utilizado como origen del agente localizado
y, fundándose en esto, se fija su orientación. Es decir, no se aplica ningún
tipo de corrección de orientación al calibrar las muestras del acelerómetro.
Esto hace que la matriz de alineamiento para el acelerómetro tenga ceros en su
triángulo superior (ver @schubertBasaltTUMVI2018 secc. IV.B y _discusión
relacionada [^basalt-headers-issue8]_).

[^basalt-headers-issue8]: <https://gitlab.com/VladyslavUsenko/basalt-headers/-/issues/8>

Luego de recibir esta primer muestra de la IMU se comienza la ejecución del
bucle principal, el cual espera indefinidamente por resultados encolados por el
módulo de optical flow para realizar una iteración. El primer par de muestras de
cámara junto a la primera muestra de la IMU posterior al par estéreo son
utilizados para inicializar el estado del agente en el primer cuadro. Esto es ya
que a cada cuadro se le asigna un estado que se compone de la posición,
orientación, velocidad y biases del giroscopio y acelerómetro que se estimaron
para tal cuadro. Notar que en Basalt, hablar de cuadros es equivalente a hablar
de instantes de tiempo, ya que los únicos puntos en el tiempo considerados son
las timestamps del par estéreo de imágenes recibidas.

Para inicializar el primer estado se toman varias suposiciones. En particular,
se asume que el dispositivo comienza en la posición $(0, 0, 0)$ y sin
aceleración ni velocidad, esto permite utilizar el vector de aceleración
reportado por la muestra del acelerómetro como el vector de gravedad y computar
así la inclinación del agente. Notar que esta inclinación no es capaz de
informar la orientación de forma completa al no poder contemplar uno de los ejes
de rotación del cuerpo. Por esta razón es recomendable iniciar la corrida con el
agente rotado con su eje $+\mathbf{Z}$ paralelo al vector gravedad, esto hará
que Basalt compute la orientación identidad. Tal rotación suele corresponder con
la posición de reposo pensada por el fabricante, o al menos este ha sido el caso
en los dispositivos utilizados en este trabajo. Además, es conveniente
posicionar el agente mirando hacia “adelante” (ajustar el _yaw_), como el
usuario considere apropiado según su entorno.

<!-- TODO@correct: No supe explicar la inicialización de marg_data en este punto por que todavía no la había leído -->

<!-- TODO@def: explicar pitch, roll, yaw -->
<!-- TODO@maybe: explicar por qué no basta con el acelerómetro para definir la orientación completa con un grafico,
hablar del producto cruz entre g y +Z, tilt vs orientación -->

En instantes posteriores (i.e., al recibir nuevas imágenes), se realiza la
llamada pre-integración de muestras consecutivas de la IMU. Considerando que
estas muestras arriban a mayores frecuencias que las de las cámaras,
pre-integrarlas es un proceso que intenta resumir las muestras entre los cuadros
a una única pseudo-muestra que sucede en los mismos instantes de tiempo que los
cuadros como se muestra en el ejemplo de \figref{fig:sample-frequencies}.

<!-- TODO@high@fig: benja recomendó hacer el grafico más grande y la verdad que sí, capaz ponerlo hasta 0.3s -->

\fig{fig:sample-frequencies}{source/figures/sample-frequencies.pdf}{%
Ejemplo de frecuencias}{%
Frecuencia de distintos eventos para un ejemplo con cámaras a 30fps y muestras
de la IMU a 240hz.
}

El proceso de pre-integración es el siguiente. Dado el cuadro previo $i$ con
timestamp $t_i$ y el cuadro posterior $j$ con timestamp $t_j$, se intenta
computar una pseudo-muestra $\Delta \mathbf{s} = (\Delta \mathbf{R}, \Delta \mathbf{v},
\Delta \mathbf{p})$ que representa cambios de orientación, velocidad y posición
respectivamente según las mediciones de la IMU que ocurrieron desde $t_i$ hasta
$t_j$. Para cada timestamp $t$ de la IMU tal que $t_i < t \leq t_j$ tenemos la
muestra de aceleración lineal $\mathbf{a}_t$ y de velocidad angular
$\mathbf{\omega}_t$. Definimos entonces de forma recursiva la pseudo-muestra
$\Delta \mathbf{s}$ de la siguiente manera:

<!-- TODO@high@def: entender este conjunto de ecuaciones requiere:
- saber que R es 3x3. Y que es lo que significa multiplicar por R
- qué es exp
EDIT: ya hice la seccion de transforms.md ahora por si las dudas deberia
leer todo lo de basalt de vuelta para ver si tiene sentido igualmente antes
de sacar el to-do.
 -->

<!-- $$ -->

\begin{align}
\label{eq:imu-preintegration}
(\Delta \mathbf{R}_{t_i}, \Delta \mathbf{v}_{t_i}, \Delta
\mathbf{p}_{t_i}) & := (\mathbf{I}, \mathbf{0}, \mathbf{0})
\\
\Delta \mathbf{R}_{t+1} & := \Delta \mathbf{R}_t exp(\mathbf{\omega}_{t+1} \Delta t)
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

Es destacable mencionar que este tipo de pre-integración es también utilizado
por los otros sistemas estudiados Kimera y ORB-SLAM3. La ventaja que presenta es
que sus características son bien conocidas gracias al trabajo de
@forsterOnManifoldPreintegrationRealTime2017 y las expresiones necesarias para
el cómputo de residuales, como sus jacobianos, son cerradas y fueron derivadas
de forma ejemplar en dicho trabajo.

Entonces, con esta muestra pre-integrada junto a los datos del nuevo cuadro (sus
keypoints), se procede a la etapa de `measure` del módulo de VIO. Aquí lo
primero que se hace es predecir que el estado de este nuevo instante estará
basado en el estado del instante anterior más la adición de las muestras
pre-integradas de la IMU. El resto de la etapa de `measure` se basa en el manejo
y actualización de la base de datos de los puntos de interés en 3D, o
_landmarks_, y sus observaciones, junto a algo que, en Basalt, está fuertemente
ligado: la toma de cuadros clave, o _keyframes_.

##### Base de datos de landmarks

Recordemos que el módulo de optical flow encuentra keypoints en cada cuadro,
esto es, una landmark o punto de interés en la escena 3D proyectada sobre el
plano de la imagen 2D. Más aún este módulo era capaz de hacer el seguimiento de
keypoints similares mediante optical flow, es decir, de keypoints que observan a
la misma landmark. Parte de nuestro objetivo entonces será triangular las
posiciones de estas landmarks considerando las observaciones tomadas.
Consideremos además la naturaleza altamente ruidosa de estas observaciones, con
landmarks que aparecen y desaparecen de la visión de los cuadros por múltiples
razones como: ser ocluidas por objetos de escena, ser distorsionadas por el
ángulo del observador, artefactos intrínsecos de los sensores ópticos como el
motion blur o el ruido introducido por la ganancia del amplificador de señal
digital, o simplemente porque dejan de estar en el campo de visión de las
cámaras. Por estas razones entonces, será fundamental la correcta gestión de la
información de las landmarks y sus observaciones. En Basalt, la clase que se
encarga de esto es la `LandmarkDatabase` con la siguiente estructura.

```C++
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

Habiendo dicho esto, al recibir un nuevo cuadro `measure` simplemente recorre
todas las observaciones o `Keypoint`s que este trae y se añaden a la base de
datos las observaciones de landmarks ya existente en la misma. Observaciones de
landmarks no registradas en la base de dato se guardan para poder determinar si
el módulo amerita la toma de un nuevo keyframe.

##### Keyframes

En contraste con sistemas como Kimera y ORB-SLAM3 que tienen condiciones más
intrincadas, en Basalt, la heurística para decidir si el cuadro actual será un
keyframe es muy sencilla: si _más del 30% de las observaciones del cuadro actual
corresponden a landmarks no registradas y han sucedido más de, por defecto, 5
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
de esta landmark producida en alguna cámara $t$. En caso de encontrarla se sigue
considerando lo siguiente.

<!-- LTeX: language=es-AR -->

- La cámara $h$ dels keyframe tiene una pose estimada para la IMU en esa timestamp
  que denominaremos $\mathbf{T}_{i_h} \in SE(3)$. Similarmente tendremos
  $\mathbf{T}_{i_t}$ para la cámara $t$.

- A su vez como los parámetros de calibración son estáticos y conocidos,
  conocemos la función de proyección $\pi_h$, sus parámetros intrínsecos
  $\mathbf{i}_h$ y la pose relativa de la cámara $h$ respecto a la IMU. Llamaremos
  a esta transformación fija $\mathbf{T}_{i_h c_h} \in SE(3)$. Similarmente con
  $\pi_t$, $\mathbf{i}_t$ y $\mathbf{T}_{i_t c_t}$ para la cámara $t$.

- Podemos ahora desproyectar $\mathbf{p}_h$ y $\mathbf{p}_t$ a sus respectivas
  posiciones 3D estimadas $\mathbf{p}'_h := \pi^{-1}_h(\mathbf{p}_h, \mathbf{i}_h)$
  y $\mathbf{p}'_t := \pi^{-1}_t(\mathbf{p}_t, \mathbf{i}_t)$ con $\mathbf{p}'_h,
\mathbf{p}'_t \in \R^3$.

- Computamos ahora la transformación de la IMU de $h$ a la IMU de $t$ dada por
  $\mathbf{T}_{i_h i_t} := \mathbf{T}_{i_h}^{-1} \mathbf{T}_{i_t}$

- Luego podemos tener la transformación de la cámara $h$ a $t$ con
  $\mathbf{T}_{c_h c_t} := \mathbf{T}_{i_h c_h}^{-1} \mathbf{T}_{i_h i_t}
\mathbf{T}_{i_t c_t}$

- Finalmente con estos tres datos $\mathbf{p}'_h$, $\mathbf{p}'_t$ y
  $\mathbf{T}_{c_h c_t}$ es posible realizar la triangulación utilizando DLT con
  SVD como se explicó en la sección "DLT con SVD" para obtener un punto en
  coordenadas homogéneas en $\R^4$ con el cuarto componente representando el
  inverso de la distancia entre la cámara y el punto de interés, mientras que
  los tres primeros componentes corresponden al _bearing vector_, es decir, un
  vector unitario que determina la dirección desde la cámara hacia la landmark.

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
los dos cuadros, la baseline, sea lo suficientemente grande para considerar la
triangulación exitosa, de lo contrario se busca un nuevo cuadro para comparar
con el keyframe. Esta comprobación se reduce a revisar que la norma del vector
de traslación contenido en $\mathbf{T}_{c_h c_t}$ sea de, por defecto, más
de 5cm.

Como se ve en la definición de `Landmark`, la posición 3D de estos puntos de
interés no se almacena exactamente de la misma forma que la triangulación los
produce. En particular, no se almacena el bearing vector directamente, sino que
se utiliza un punto 2D más compacto `direction` que lo codifica (para esto se
utiliza una proyección estereográfica como se explica en la
\figref{fig:stereographic-projection}) junto a `inverse_distance`, la distancia inversa
a este punto producto de la triangulación, de esta forma la posición de la
landmark queda ligada al keyframe que la aloja.

\fig{fig:stereographic-projection}{source/figures/stereographic-projection.png}{Proyección estereográfica}{%
Interpretación geométrica de la proyección estereográfica utilizada para
representar bearing vectors. Las coordenadas definidas por la propiedad \mono{Vector2
direction} definen un punto en el plano $XY$ ($Z=0$) mostrado en azul. Para
obtener el vector unitario correspondiente, se traza una línea desde el punto
$(0 0 -1)^T$ hacia \mono{direction} en el plano $XY$. El vector en el que esta línea
interseca a la esfera unitaria será el bearing vector codificado. Se muestran
tres ejemplos en rojo, verde y amarillo, con lineas punteadas que representan
las líneas trazadas y flechas representando los bearing vectors obtenidos.
}

Si todos los procedimientos relacionados a la triangulación de estos dos cuadros
fueron correctos, se almacena la landmark nueva en la base de datos. De haber
otras observaciones de esta landmark no se utilizan todavía para añadir
información a su posición, si no que simplemente se añaden las observaciones
para uso futuro.

<!-- TODO@license: openvslam, avoid reading ORB-SLAM3 code -->
<!-- TODO@future: punto de mejora para basalt: usar dogleg minimization en vez de levenberg-marquardt. No se si vale la pena mencionarlo -->
<!-- TODO@question: question for basalt: why are they not using gtsam/g2o/ceres for the solvers? -->
<!-- TODO@future: parallelization/vectorization of gauss newton seems very easy, levenberg marquardt not so much -->

#### Optimización y marginalización (TODO)

<!-- TODO@high -->
