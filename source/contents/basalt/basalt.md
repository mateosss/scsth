<!-- TODO@def: VIO habla acerca de componentes: (patch tracking, landmark
representation, first-estimate Jacobians, marginalization
scheme) que podría ser interesante discutir -->
<!-- TODO@high@ref: Checkear que los 6 papers de basalt esten siendo citados -->
<!-- TODO: I think this paper has what I need to understand the code better http://www.roboticsproceedings.org/rss09/p37.pdf -->

# Implementación de un sistema

## Basalt

### Preliminares

La decisión sobre cuál sistema de localización visual-inercial integrar con
Monado no fue sencilla. Fue necesario descartar docenas de implementaciones e
incluso así, no fue trivial entender si los sistemas elegidos finalmente
resultaron los más adecuados para el contexto de XR. Cada implementación
presentaba ventajas y desventajas, aunque es usual que las respectivas
publicaciones se concentren en destacar solo las métricas favorables. Más aún,
es necesario conocimiento experto para comprender cómo la elección de ciertos
fundamentos teóricos, técnicas algorítmicas, decisiones arquitecturales o de
tecnología afectan a la calidad del tracking dedicado a XR. Gran parte
de este trabajo se basó en el estudio de los conceptos necesarios para poder
tomar este tipo de decisiones.

A grandes rasgos y sin un orden en particular, las propiedades deseables que se
consideraron a la hora de elegir sistemas fueron:

1. Versatilidad en la configuración sensores: Monado necesita soportar una gran
  variedad de dispositivos, es por esto que se prefirieron sistemas que soporten
  la mayor cantidad de combinaciones y tipos de sensores. En el mejor de los
  casos, Monado debería ser capaz de localizar desde cascos con cámaras estéreo
  y una IMU, hasta celulares con una única cámara y sin giroscopio.

2. Licencia permisiva: La licencia y filosofía de Monado da gran libertad al
   programador que lo utilice de hacer lo que desee con su código fuente. Esto
   incluye poder utilizarlo en proyectos en dónde se prefiere no distribuir
   dicho código. Licencias de código libre “virales” como la GPL
   [@GNUGeneralPublic] no permiten esto y enlazar Monado a sistemas con este
   tipo de licencias contagiaría a los proyectos que dependen de Monado
   quitándoles la libertad de decidir no publicar su código.

3. Desarrolladores activos: Estos sistemas suelen surgir de grupos de
   investigación y es muy común que se abandonen luego de que el trabajo sea
   publicado. Será necesario encontrar, dentro de lo posible, sistemas con un
   desarrollo activo, con mantenedores accesibles y que, en el mejor de los
   casos, acepten contribuciones a su proyecto.

4. Estabilidad, facilidad de instalación y buenas prácticas de desarrollo: Los
   sistemas de SLAM son muy complejos y es usual que se optimicen para funcionar
   únicamente en los conjuntos de datos de prueba dejando de lado estas
   características que son fundamentales a la hora de querer brindar un sistema
   para ser utilizado por usuarios finales.

5. Rendimiento: El área de XR tiende a buscar la reducción del tamaño de los
   dispositivos para mejorar su ergonomía y practicidad. Un sistema de tracking
   debe ser capaz de operar en contextos con recursos acotados, debería utilizar
   poca memoria, poca energía y ser capaz de estimar poses a altas frecuencias y
   utilizando poca capacidad de cómputo.

6. Precisión: Por último y no menos importante, queremos que la precisión de la
   localización sea adecuada. El nivel de precisión requerido dependerá del tipo
   de aplicación. Es común que se necesite precisión submilimétrica en contextos
   de VR donde la simulación cubre completamente el campo de visión del usuario,
   y fallos en el tracking puedan inducir mareos. Mientras que para otros
   contextos como AR realizado por un celular, no es tan vital contar con ese
   nivel de exactitud.

#### Sistemas integrados

En este trabajo se integraron con Monado tres sistemas de código libre
distintos, primero _Kimera-VIO_ [@rosinolKimeraOpenSourceLibrary2020], luego
_ORB-SLAM3_ [@camposORBSLAM3AccurateOpenSource2021] y finalmente _Basalt_
[@usenkoBasaltVisualInertialMapping2020].

Kimera-VIO[^kimera-repo] es una implementación desarrollada en el Instituto de
Tecnología de Massachusetts (MIT) con una licencia permisiva BSD-2
[@2ClauseBSDLicense]. Fue publicada originalmente en octubre de 2019 y su última
actualización significativa[^kimera-last-update], en dónde se introduce la
posibilidad utilizar una única cámara, ocurrió en abril de 2021.
Kimera resultó inicialmente atractivo por su licencia y su promesa de correr en
tiempo real. Además de esto posee funcionalidades muy interesantes para XR como
la reconstrucción y análisis semántico del entorno en el que el dispositivo se
encuentra. Desgraciadamente, no logró ser adecuado mostrando grandes
dificultades a la hora de correrlo en sensores distintos a los presentados en su
publicación. Más aún el término “tiempo real” en el contexto de la publicación
es ambiguo, ya que está lejos de ser capaz de ejecutarse a frecuencias adecuadas
para XR y es más adecuado para uso en robots con frecuencias de menos de 10 Hz
[@rosinolKimeraOpenSourceLibrary2020, Fig. 5].

ORB-SLAM3[^orbslam3-repo] es desarrollado por la Universidad de Zaragoza con una
licencia viral GPL-3.0 [@GNUGeneralPublic]. Fue publicado inicialmente en julio
de 2020 y su última actualización significativa[^orbslam3-last-update] ocurrió
en diciembre de 2021. ORB-SLAM3 es la tercera iteración de una línea de sistemas
que dominan las tablas comparativas de SLAM desde hace unos cuantos años y es
por esto que se implementó incluso aunque no posea una licencia permisiva. El
sistema presenta varios métodos novedosos que mejoran la precisión del tracking
mientras que muestra ser capaz de estimar poses a unos 20 Hz o 30 Hz
[@camposORBSLAM3AccurateOpenSource2021, Tabla 6]. El sistema es el más versátil
del campo permitiendo ser ejecutado en configuraciones con una cámara
(monocular) o dos (estéreo), con o sin uso de la IMU e incluso con cámaras de
profundidad. Además, soporta la reconstrucción de múltiples mapas y la capacidad
de interconectarlos o incluso guardarlos en almacenamiento persistente para ser
reutilizados en sesiones de tracking posteriores. Una desventaja es que la
trayectoria que se da al construir el mapa es particularmente ruidosa y difícil
de utilizar en XR. Se plantea como trabajo a futuro investigar más acerca de la
funcionalidad de reutilización del mapa y como funciona el tracking con mapas ya
construidos.

Finalmente, Basalt[^basalt-repo] es desarrollado por el Instituto Técnico de
Múnich con una licencia permisiva BSD-3 [@3ClauseBSDLicense]. Fue publicado
originalmente en abril de 2019 y su última actualización
significativa[^basalt-last-update] [@demmelBasaltSquareRoot2021] ocurrió en
octubre de 2021. Basalt solo es capaz de correr en tiempo real su sistema de VIO
necesitando de una pasada offline de su _“mapper”_ para lograr un mapa
consistente. A pesar de esto, mostró ser sorprendentemente preciso y tener un
gran desempeño. En particular, es un sistema que puede correr fácilmente a 60 Hz
consumiendo cuadros a mayores resoluciones que las probadas en ORB-SLAM3 y
Kimera y duplicando las frecuencias de muestreo a 60 fps. Esta capacidad de
soportar mayor cantidad de muestras aumenta significativamente la precisión de
la trayectoria a pesar de que no sea un sistema de SLAM completo. Además de
esto, el sistema es notablemente más sencillo de compilar al tener un buen
manejo de sus dependencias, posee mejores prácticas de ingeniería de software y
es en general mucho más estable logrando fácilmente sesiones de tracking
ininterrumpidas a diferencia de los sistemas anteriores.

[^kimera-repo]: <https://github.com/MIT-SPARK/Kimera-VIO>
[^orbslam3-repo]: <https://github.com/UZ-SLAMLab/ORB_SLAM3>
[^basalt-repo]: <https://gitlab.com/VladyslavUsenko/basalt>
[^kimera-last-update]: <https://github.com/MIT-SPARK/Kimera-VIO/pull/152>
[^orbslam3-last-update]: <https://github.com/UZ-SLAMLab/ORB_SLAM3/releases/tag/v1.0-release>
[^basalt-last-update]: <https://gitlab.com/VladyslavUsenko/basalt/-/commit/24325f2a>

Los tres sistemas fueron integrados en Monado con distintos niveles de éxito,
pueden verse demostraciones de cómo funcionan en los videos referenciados al pie
de página [^kimera-video] [^orbslam3-video] [^basalt-video]. Más adelante, en el
[](#evaluation), se verán resultados y distintas métricas comparativas entre los
sistemas.

[^kimera-video]: Kimera-VIO con Monado: <https://youtu.be/gxu3Ve8VCnI>
[^orbslam3-video]: ORB-SLAM3 con Monado: <https://youtu.be/kJwWY973b10>
[^basalt-video]: Basalt con Monado: <https://youtu.be/ajuqQ7E1MFw>

Las terminologías y jerga del área de SLAM/VIO pueden resultar abrumadoras, pero
se espera que introduciéndolas en el contexto de una implementación concreta se
puedan entender mejor los problemas que los sistemas, en general, tienen que
resolver. Por todas las razones mencionadas anteriormente, Basalt es actualmente
el sistema de preferencia para ser utilizado con Monado y, si bien se estudió el
código fuentes de los tres sistemas, en esta parte del trabajo que sigue a
continuación _nos vamos a enfocar en profundizar en la implementación de
Basalt_.

#### Problemáticas de un sistema

<!-- #define MN_BUNDLE_ADJUSTMENT %\
Introdujimos el término bundle adjustment (BA) en la \Cref{def:bundle-adjustment}
en el contexto de cuadrados mínimos. Este se refiere al refinamiento simultáneo de un conjunto de
poses de cámara, o vistas, y puntos 3D en el mapa que han sido observados por
estas vistas. Así, se intenta reducir el llamado “error de reproyección” del
conjunto actualizando tanto las poses de las cámaras como la posición de los
puntos observados. Este error hace referencia a la distancia entre las
posiciones de los puntos y en dónde las vistas esperan que estos
se encuentren \autocite{hartleyMultipleViewGeometry2004}.
-->

Un problema central en este tipo de sistemas es el de poder generar un mapa y
una trayectoria que sean _globalmente consistentes_. Con esto nos referimos a que
nuevas mediciones tengan en cuenta todas las mediciones anteriores en el
sistema. Una forma ingenua de encarar esto, sería realizando _bundle adjustment_\marginnote{MN_BUNDLE_ADJUSTMENT}
sobre todas las imágenes capturadas a lo largo de una corrida,
integrando además las mediciones provenientes de la IMU.
Desafortunadamente, este método excede rápidamente cualquier capacidad de
cómputo de la que dispongamos, y aún más teniendo en cuenta que nuestro objetivo
es localizar en tiempo real al dispositivo de XR.

Por esta razón, es usual recurrir a distintas formas de reducir la complejidad
del problema. Para realizar _odometría visual-inercial (VIO)_, es común que
se ejecute la función de optimización sobre una _ventana local_ de cuadros y
muestras recientemente capturadas, ignorando muestras históricas y acumulando
error en las estimaciones a lo largo del tiempo. Además, esta mirada tiene la
desventaja adicional de que una porción significativa de los fotogramas
capturados podrían tener posiciones similares que no añadirían demasiada información al estimador, o
incluso que algunos fotogramas puedan ser de baja calidad por contener _motion
blur_ u otro tipo de anomalías. Por otro lado, soluciones que intentan hacer
_mapeo visual-inercial_ realizan el bundle adjustment sin utilizar todas las
imágenes capturadas, sino que se limitan a la utilización de algunos fotogramas
clave, o _keyframes_ elegidos mediante criterios que priorizan cuadros nítidos y
con distancias (_baselines_) prudenciales entre ellos.

Como las muestras de IMU vienen a mayor frecuencia que las de la cámara, es
común que estas se _preintegren_ de forma tal de combinar muestras simultáneas entre dos keyframes en
una única entrada del optimizador. Sin embargo, un problema en el que esta
integración incurre, es que las mediciones de las IMU son altamente ruidosas, y
acumularlas durante tiempos prolongados acumula también cantidades
significativas de error. Este factor nos limita el tiempo que puede transcurrir
entre dos keyframes; como ejemplo en @mur-artalVisualInertialMonocularSLAM2017
se habla de keyframes que no pueden tener más de medio segundo entre sí. Además,
tener keyframes a muy bajas frecuencias afecta la calidad de las
estimaciones de velocidad y _biases_; estos últimos son offsets de medición
inherentemente variables de los acelerómetros y giroscopios a los que es
necesario reestimar de forma constante para compensar por ellos en la medición final.

#### Propuesta de Basalt

<!-- TODO@high@end: vi que esta Margin note parece salirse tambien -->
<!-- #define MN_FACTOR_GRAPH %\
Los grafos de factores son una muy buena forma de representar problemas con
muchas variables aleatorias interdependientes y muestras que las relacionan (factores).
En general, el uso de estos grafos trae beneficios
computacionales interesantes y son de gran importancia para el área de SLAM.
Sin embargo, no nos adentraremos demasiado en el tema en este trabajo y dirigimos
al lector interesado a \textcite{dellaertFactorGraphsRobot2017}.
-->

<!-- XXX: USO FACTOR NO LINEAL SIN EXPLICARLO!! -->
La novedad de Basalt [@usenkoBasaltVisualInertialMapping2020] es que formula el mapeo visual-inercial como un problema de
bundle adjustment y utiliza, de una forma específica, todas mediciones visuales e inerciales a altas frecuencias.
Usa un _grafo de factores_\marginnote{MN_FACTOR_GRAPH} [^gtsam-whatarefactorgraphs] de forma similar a otros sistemas, también llamado
_grafo de poses_ en este contexto por contener poses a estimar como nodos. En
lugar de utilizar todos los fotogramas se propone realizar la optimización en
dos capas. La capa de VIO, emplea un sistema de odometría visual-inercial, que
ya de por sí supera a otros sistemas del mismo tipo, proveyendo estimaciones de
movimiento a la misma frecuencia que el sensor de la cámara provee imágenes.
Luego, se seleccionan keyframes y se agregan _factores no-lineales_
entre estos que estiman la diferencia de posición relativa.
Estos dos factores, keyframes y poses relativas, se utilizan en la capa de
bundle-adjustment global.

[^gtsam-whatarefactorgraphs]: Artículo introductorio a los grafos de factores: <https://gtsam.org/2020/06/01/factor-graphs.html>

<!-- #define MN_LOOP_CLOSING %\
Esto es fundamental para entender cuándo el dispositivo está visitando un lugar
por el que ya pasó. Esto se denomina “loop closing”.
-->

<!-- #define MN_FEATURES %\
Las features son puntos de interés relevados en una imagen.
Son estos los puntos que triangularemos en el bundle adjustment.
-->

La capa de VIO, detecta _features_\marginnote{MN_FEATURES} que son rápidas y buenas para seguir durante
varios cuadros (esto es el _optical flow_ que veremos en la sección
[](#optical-flow)), mientras que en la capa de mapeo se usan features adecuadas
que son indiferentes a las condiciones de luz o al punto de
vista de la cámara\marginnote{MN_LOOP_CLOSING}. De esta forma tenemos un sistema que es capaz de utilizar
las mediciones a alta frecuencias de los sensores y al mismo tiempo tiene la
capacidad de detectar cuando se está en ubicaciones ya
visitadas, obteniendo así un mapa que es globalmente consistente. Además, el
problema de optimización se reduce, ya que a diferencia de otros sistemas, no es
necesario estimar velocidades ni biases (de la IMU).

### Implementación

A continuación describiremos la arquitectura e implementación de Basalt de una
manera más detallada. Estas secciones surgen directamente de la lectura del código
fuente del sistema e intentan proveer detalles más bien pragmáticos que se
encuentran en el mismo, pero que pueden quedar escondidos en las publicaciones de
más alto nivel que presentan estos sistemas. A su vez, se toman ciertas licencias literarias que deberían
ayudar al entendimiento y que no son posibles a la hora de escribir código.

Cómo vimos anteriormente, el funcionamiento de Basalt se divide en dos
etapas. La primera etapa de odometría visual-inercial (VIO), en el cual se
emplea un sistema de VIO que supera a sistemas equivalentes de vanguardia
mientras que la segunda etapa de mapeo visual-inercial (VIM), toma keyframes
producidos por la capa de VIO y ejecuta un algoritmo de bundle adjustment para
obtener un mapa global consistente. Estas dos capas son completamente
independientes. En una corrida usual, se ejecuta inicialmente el sistema de VIO y
es este el que decide y almacena persistentemente qué cuadros y con qué
información el sistema de VIM, de ejecutarse, debería utilizar al realizar el
proceso de bundle adjustment.

Esto significa que, por defecto, no contamos con la capacidad de utilizar el VIM
en tiempo real para XR, solo el VIO. Por ende solo este fue integrado con
Monado. Se plantea como trabajo a futuro la paralelización del VIM en un hilo separado para poder correrlo
en tiempo real[^basalt-issue69]. Exploraremos entonces, en esta parte del
trabajo, los componentes fundamentales de la capa de VIO: _optical flow_,
_bundle adjustment visual-inercial_ y finalmente el proceso de _optimización y
de marginalización parcial_.

[^basalt-issue69]: Discusión sobre como adaptar Basalt para poder correr el VIM
en tiempo real: <https://gitlab.com/VladyslavUsenko/basalt/-/issues/69>

#### Optical flow {#optical-flow}

<!-- TODO@fig: algún gráfico que represente lo que le entra al módulo y lo que
sale, lo mismo para todo el pipeline de VIO, y lo mismo para todo Basalt -->

El módulo de VIO toma dos tipos de entrada, una de ellas son las muestras raw de
la IMU; y la otra, contra intuitivamente, no son las imágenes raw provenientes
de las cámaras, sino que son los _keypoints_ resultantes de ellas. Estos son la posición en dos dimensiones
sobre el plano de la imagen de las _features_ detectadas. Las features a su vez
son la representación de los puntos de interés o _landmarks_ de la escena
tridimensional proyectados sobre las imágenes. El proceso de detectar features,
computar su transformación entre distintos cuadros, y producir los keypoints de
entrada para el módulo de VIO, está a cargo del módulo de _optical flow_ (o
_flujo óptico_). Cabe aclarar que optical flow es el nombre que recibe tanto el
campo vectorial que representa el movimiento aparente de puntos entre dos
imágenes, como el proceso de estimarlo. Este puede ser denso, si se considera el
flujo de todos los píxeles, o no (_sparse_) si solo se computa el flujo de
algunos keypoints como es el caso que veremos.

El módulo de optical flow corre en un hilo
separado y es por donde las muestras del par de cámaras estéreo ingresan al
pipeline de Basalt. Inicialmente se genera una representación piramidal de las
imágenes, o también llamada de _mipmaps_, esta es una forma tradicional
[@williamsPyramidalParametrics1983] de almacenar una imagen en memoria junto a versiones
reescaladas de la misma como se ve en la \figref{fig:mipmap}. Los mipmaps tienen múltiples utilidades en
computación gráfica (p. ej. _filtrado trilineal_, _LODs_, reducción de
_patrones moiré_) pero en el caso de Basalt serán utilizados para darle robustez
al algoritmo de seguimiento de features o _feature tracking_.

\fig{fig:mipmap}{source/figures/mipmap.png}{Mipmaps}{%
Representación piramidal (mipmaps) de un cuadro del conjunto de datos estándar
EuRoC \autocite{burriEuRoCMicroAerial2016}.
}

<!-- #define MN_OPENCV %\
OpenCV es una de las bibliotecas de visión por computadora más populares y
utilizadas en este tipo de sistemas. Combina múltiples algoritmos y presenta
una licencia permisiva Apache 2 \autocite{ApacheLicenseVersion} (prev. BSD-3 \autocite{3ClauseBSDLicense}).
-->

Posteriormente se realiza la detección de features nuevas sobre las imágenes
utilizando el algoritmo _FAST_ [@rostenFasterBetterMachine2010a] para detección
de esquinas, o puntos sobresalientes de la imagen en general (keypoints), implementado
sobre _OpenCV_\marginnote{MN_OPENCV}. Resulta importante aclarar que Basalt es uno de
los sistemas que menos depende de OpenCV, siendo `cv::FAST` el único algoritmo de la
biblioteca en uso durante una ejecución usual. El proyecto
tiende a reimplementar muchas de las técnicas y algoritmia de forma
especializada y, como veremos en otros módulos, otras tareas razonablemente
complejas como la optimización de grafos de poses se implementan también dentro
del proyecto y sin recurrir a bibliotecas externas. Esta es una de las varias
razones por las que el sistema logra tan buen rendimiento, ya que
estas bibliotecas suelen necesitar de campos y comprobaciones generales
del problema que intenta solucionar, mientras que Basalt puede
prescindir de todas las que no apliquen a VIO. Aunque, también es cierto que estas
reimplementaciones añaden complejidad al sistema.

Siguiendo con la
detección de features, una heurística particular de Basalt es la división del
cuadro completo en celdas de, por defecto, 50 por 50 píxeles en donde se
detectan los nuevos puntos de interés. Por celda solo se conserva la feature
de mejor calidad o con mejor _respuesta (response)_, aunque se puede configurar
para detectar más de una. Siempre que la celda tenga alguna
localizada de cuadros anteriores, no se intenta detectar nuevas. Esto contrasta
con sistemas como Kimera-VIO que corren la detección FAST sobre el cuadro entero
y evitan la redetección mediante el uso de _máscaras_ que le instruyen al
algoritmo a obviar esas secciones. Desafortunadamente la construcción de tales
máscaras suele ser costosa y la heurística de Basalt, a pesar de desperdiciar
espacio por no permitir la detección de nuevas características entre celdas, es
más eficiente, ya que en situaciones comunes se logran detectar una cantidad
razonable de features sin problemas. Esta detección se
realiza únicamente sobre la primera cámara, usualmente la izquierda, mientras
que en la otra cámara se reutiliza el método de seguimiento de keypoints que se
describe a continuación.

<!-- TODO@fig: Agregar imágenes de los parches, de la detección de features, del optical flow -->

En cada instante de tiempo que entran un nuevo par de imágenes se tiene acceso a
toda la información recolectada del instante anterior, en particular a sus
keypoints. Una suposición razonable es que las imágenes correspondientes a este
nuevo instante van a compartir muchos de los keypoints con las imágenes
anteriores y en posiciones similares. Con esa suposición Basalt logra
ahorrarse tener que volver a detectar features de la imagen con FAST y en cambio
el problema se transforma en, dado una imagen anterior (inicial), sus keypoints
y una imagen nueva (objetivo), estimar donde ocurren esos mismos keypoints en la
imagen nueva. Para esto, por cada keypoint anterior, se genera un parche
$\Omega$ alrededor de su ubicación de, por defecto, 52 puntos como se ve en el
ejemplo de la \figref{fig:patches}.

\fig{fig:patches}{source/figures/patches.png}{Parches}{%
Ejemplos de los parches de 52 puntos considerados para computar el optical flow
de distintos keypoints de una imagen.
}

Considerando
entonces que este parche debería estar en la imagen nueva en coordenadas
cercanas a las del keypoint anterior, queremos encontrar la transformación $\mathbf{T}
\in SE(2)$ que le ocurrió al parche, y por ende al nuevo keypoint que se
encontraría en el centro de este nuevo parche. Basalt emplea entonces
optimización por cuadrados mínimos mediante el algoritmo iterativo de
Gauss-Newton para encontrar $\mathbf{T}$ utilizando un residual $r$ con:

<!-- TODO@correct: Realmente es gauss newton lo que se hace? ver optical_flow_max_iterations -->
<!-- TODO@correct: Not quite, es inverse-compositional method, que es un gauss newton
sobre algo un poco distinto: https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0910/zhao.pdf
por eso aparece el hessiano y cosas de esa pinta -->
<!-- TODO: Mencionar ZNCC como norma no utilizada: https://martin-thoma.com/zero-mean-normalized-cross-correlation/ -->

$$
r_i =
  \frac{I_{t + 1}(\mathbf{T} \mathbf{x}_i)}{\overline{I_{t + 1}}} -
  \frac{I_{t}(\mathbf{x}_i)}{\overline{I_{t}}}
  \ \ \ \ \forall \mathbf{x}_i \in \Omega
$$

Y aquí siendo $I_t(\mathbf{x})$ la intensidad de la imagen anterior en el pixel ubicado en
las coordenadas $\mathbf{x}$, análogamente $I_{t + 1}(\mathbf{x})$ para la
imagen objetivo; y siendo $\overline{I_{t}}$ la intensidad media del parche
$\Omega$ en la imagen inicial, análogamente $\overline{I_{t + 1}}$ para la
imagen objetivo y el parche transformado $\mathbf{T}\Omega$. Notar que al
normalizar las intensidades obtenemos un valor que es invariante incluso ante
cambios de iluminación.

Los detalles del cálculo de gradientes y jacobianos están basados en el método
de @lucasIterativeImageRegistration1981 para tracking de features (_KLT_). El
uso adicional de mipmaps sobre KLT fue originalmente expuesto en
@bouguetPyramidalImplementationLucas1999.

Para asegurar que la estimación fue exitosa se invierte el problema y se intenta
trackear desde la imagen nueva hacia la inicial y, si el resultado está muy
alejado de la posición inicial, el nuevo keypoint se considera inválido
(un _outlier_) y se lo descarta. Otro detalle a aclarar es que, recordando que la
detección costosa de features con FAST solo ocurría en las imágenes de una de
las cámaras, es posible ahora entender que las features en la segunda cámara
pueden ser “detectadas” con este método menos costoso. Es decir, simplemente se
computa el optical flow desde la imagen de la cámara izquierda a la de la cámara
derecha en el mismo instante de tiempo.

Finalmente, el último de los pasos que ocurre cuando el módulo de optical flow
procesa un cuadro, es el de filtrado de keypoints, en el cual se desproyectan los
keypoints a posiciones en la escena tridimensional y en caso de que el error
de reproyección supere cierto umbral, estos keypoints serán descartados por
considerarse outliers.

#### Bundle adjustment visual-inercial

<!-- Cosas que tienen que estar:
- [ ] pi es estático (no autocalibration comparado a openvins)
- [ ] se estima la pose del IMU
- [ ] el estado es sk (frame_poses?), sf (frame_states), sl (lmdb)
- [ ] "representation of unit vectors in 3D" stereographic projection
- [ ] "reprojection error"
 -->

En un hilo separado al módulo de optical flow, corre el estimador de VIO
encargado de realizar el bundle adjustment sobre los cuadros y muestras de la
IMU recientes para estimar la pose. Este toma como entrada las muestras de la
IMU junto a los keypoints 2D detectados para cada imagen, o sea la salida del
módulo de optical flow. Este módulo es el que efectivamente realizará la
integración y optimización con toda la información recibida y producirá como
salida en una cola, la estimación de los estados del agente a localizar.

##### Inicialización y preintegración {#basalt-preintegration}

<!-- TODO@high@def: referencia a la sección "Calibración de IMU", escribirla, referenciarla -->

\begin{mdframed}[backgroundcolor=shadecolor]
TODO: En el párrafo que sigue hablo de una sección “Calibración de IMU” que todavía no
existe, tengo la mitad de esa sección escrita pero todavía estoy considerando si
agregarla al trabajo o simplemente referenciarla de un libro.
Cuando uno trabaja con sensores se tienen modelos matemáticos que describen las
distorsiones que se suelen dar en el sensor. Calibrar un sensor significa
encontrar los valores de los parámetros de este modelo para tu sensor particular.

Se usa también cuadrados mínimos no lineales para calibrar un sensor. Uno toma varias
mediciones y despues optimiza para encontrar los parámetros más adecuados.

Esto aplica exactamente igual para las cámaras (aunque ahí hay muchos más
modelos en uso). Y hay unos detalles muy copados de los que hablar por que
el equipo de Basalt desarrolló sus propios modelos de cámaras que son muy
rápidos por que están bien pensados para SLAM (la inversa de los modelos tienen expresión
cerrada que no es usual en los modelos de cámara estándar). Además tengo un merge request abierto
en donde contribuyo un nuevo modelo de cámara que se usa en unos cascos que les
hicimos ingeniería inversa (los de Windows Mixed Reality) y que Basalt no
soportaba anteriormente:
\url{https://gitlab.com/VladyslavUsenko/basalt-headers/-/merge_requests/21}.

Así que sí, me gustaría detallar más todo esto en el trabajo, pero el tiempo se
está acabando.
\end{mdframed}

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

\begin{mdframed}[backgroundcolor=shadecolor]
TODO: En el último punto hablo de una sección “DLT con SVD” que no existe en el
trabajo.
Estoy todavía viendo si agregarla o simplemente referenciar el capítulo del libro
de Multiple View Geometry de la bibliografía.

DLT es direct linear transform y SVD es single value decomposition.
Esto se usa para triangular puntos 3D dadas dos vistas 2D.
Pero los detalles no necesité profundizarlos.
\end{mdframed}

<!-- TODO@high: ese último punto hablo de SVD, y DLT y referencio una sección que no existe. -->

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
de 5 cm.

Como se ve en la definición de `Landmark`, la posición 3D de estos puntos de
interés no se almacena exactamente de la misma forma que la triangulación los
produce. En particular, no se almacena el bearing vector directamente, sino que
se utiliza un punto 2D más compacto `direction` que lo codifica (para esto se
utiliza una _proyección estereográfica_ como se explica en la
\figref{fig:stereographic-projection}) junto a `inverse_distance`, la distancia inversa
a este punto producto de la triangulación, de esta forma la posición de la
landmark queda ligada al keyframe que la aloja.

<!-- TODO@high@fig: rehacer esta fig -->

\fig{fig:stereographic-projection}{source/figures/stereographic-projection.pdf}{Proyección estereográfica}{%
Interpretación geométrica de la proyección estereográfica utilizada para
representar bearing vectors. Las coordenadas definidas por la propiedad \mono{Vector2
direction} en \mono{Landmark} definen un punto en el plano $XY$ ($Z=0$) mostrado en azul. Para
obtener el vector unitario correspondiente, se traza una línea desde el punto
$(0,\ 0,\ -1)^T$ hacia \mono{direction} en el plano $XY$. El vector en el que esta línea
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

<!-- TODO@high: escribir -->

\begin{mdframed}[backgroundcolor=shadecolor]
TODO: Esta última parte es un poco
compleja y me ha estado costando terminar de cerrar como explicarla. Basicamente
lo que se hace es plantear la función de error a optimizar $E(x)$ que combina un
montón de términos de error. Y se le quiere aplicar gauss newton. El problema es
que al haber tantos términos que optimizar, el cálculo de los jacobianos se hace muy rebuscado
y se arma un callstack de funciones muy profundo que lo único que hace es
computar valores parciales de estos jacobianos.\\
\\
Por otro lado la idea de
“marginalización“ es importante por que habla de uno de los términos que aparece
en $E(x)$ y que es un poco la novedad que trae Basalt, ellos logran eliminar
(marginalizar) los efectos de muchas mediciones en unas pocas distribuciones
aproximadas.\\
\\
Para sumar a la complejidad de esta sección, está, un poco escondido en la
implementación, el concepto de “grafo de factores“ para armar antes de la
optimización. No lo he profundizado lo suficiente como para explicarlo pero a
grandes rasgos, es un grafo en donde se tienen nodos que son variables
aleatorias mientras que los lados son las mediciones que uno toma (los factores). Por ejemplo
un nodo puede ser la variable que representa la posición de una landmark que
quiero estimar,
mientras que un factor puede ser el vector distancia que el agente trianguló con
sus cámaras hacia esa landmark (también tiene ruido).\\
La idea de estos grafos es hacer una estimación
“máxima a posteriori“ (MAP) con todo lo que tienen adentro. MAP es un concepto
muy parecido al de estimación de máxima verosimilitud. Básicamente lo que se
tiene es que minimizar la función de error $E(x)$ lo que está haciendo es
acomodando los resultados de las variables de interés para que sean los de mayor
probabilidad (“de mayor verosimilitud“) dadas las restricciones impuestas por las mediciones tomadas (los
factores del grafo).
\end{mdframed}
