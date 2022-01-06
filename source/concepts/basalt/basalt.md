<!-- TODO: explicar bundle adjustmente -->
<!-- TODO: que es motion blur, (quizás usar nota al pie) -->
<!-- TODO: maybe? cuando menciono preintegración citar el paper On-Manifold preintegration -->
<!-- TODO: Estoy implicitamente hablando de un optimizador, cuando hablo de factor graphs? -->
<!-- TODO: Explicar factores no-lineales, o almenos decir que no se explican -->
<!-- TODO: Que son features? -->
<!-- TODO: Que es loop closing? -->
<!-- TODO: VIO habla acerca de componentes: (patch tracking, landmark
representation, first-estimate Jacobians, marginalization
scheme) que podría ser interesante discutir -->
<!-- TODO: Citar bien la cita -->
<!-- TODO: Mencionar que TUM lo desarrolla y las personas que lo mantienen -->

# Basalt

## Problemáticas Preliminares

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
entre dos keyframes; como ejemplo en [1] se habla de keyframes que no pueden
tener más de 0.5 segundos entre sí. A su vez, tener keyframes a muy bajas
frecuencias afecta la calidad de las estimaciones de velocidad y biases; estos
últimos son offsets de medición inherentemente variables de los acelerómetros y
giroscopios a los que es necesario estimar para compensar por ellos en la
medición final.

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

<!-- TODO@style: títulos con mayúscula cada letra o no? -->

### Odometría Visual-Inercial

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

#### Optical Flow

<!-- TODO@graph: input/output graph de VIO -->

El módulo de VIO toma dos tipos de entrada, una de ellas son las muestras raw de
la IMU; y la otra, contra intuitivamente, no son las imágenes raw provenientes
de las cámaras, sino que son los _keypoints_ resultantes de ellas. Recordemos
que los keypoints no son más que la ubicación y rotación en dos dimensiones
sobre el plano de la imagen de las _features_ detectadas. Las features a su vez
son la representación de los puntos de interés o _landmarks_ de la escena
tri-dimensional proyectados sobre las imágenes. El proceso de detectar features,
computar su transformación entre distintos cuadros, y producir los keypoints de
entrada para el módulo de VIO, está a cargo del módulo de _optical flow_ (o
_flujo óptico_). Cabe aclarar que optical flow es el nombre que recibe tanto el
campo vectorial que representa el movimiento aparente de puntos entre dos
imágenes, como el proceso de estimarlo. Este puede ser denso, si se considera el
flujo de todos los píxeles, o no (_sparse_) si solo se computa el flujo de
algunos keypoints.

El [módulo][`FrameToFrameOpticalFlow`] de optical flow corre en un thread
individual y es por donde las muestras del par de cámaras estéreo ingresan al
pipeline de Basalt. Inicialmente se genera una representación piramidal de las
imágenes, o también llamada de _mipmaps_, esta es una forma tradicional
[@williams_pyramidal_1983] e almacenar una imagen en memoria junto a versiones
re-escaladas de la misma. Los mipmaps tienen tienen múltiples utilidades en
computación gráfica (e.g., _filtrado trilinear_, _LODs_, reducción de
_patrones moiré_) pero en el caso de Basalt serán utilizados para darle robustez
al algoritmo de localización de features (_feature tracking_).

[`FrameToFrameOpticalFlow`]: TODO

La versión de este módulo en la que nos enfocaremos, será la implementada en la
clase  derivada de [`OpticalFlowBase`], las otras
alternativas que derivan de `OpticalFlowBase` son esencialmente el mismo tipo de
algoritmo con variaciones mínimas. Este módulo ejecuta en un thread individual
el método [`processingLoop`] que se encarga de recibir el par de imágenes
estéreo y procesarlas con [`processFrame`]. `processFrame` por su parte realiza
tres o cuatro procedimientos fundamentales. Genera _representaciones
piramidales_ para cada frame recibido, detecta nuevas features con
[`addPoints`], filtra puntos de mala calidad con [`filterPoints`] y, salvo para
el primer frame, intenta localizar (trackear) el desplazamiento de keypoints del cuadro
anterior con [`trackPoints`]. Cabe aclarar que este último punto, el tracking de
features entre dos imágenes, es al que usualmente se asocia el término optical
flow o _feature tracking_.

Se intenta detectar en cada nuevo cuadro nuevos keypoints mediante el metodo
[`addPoints`]. En este

La representación piramidal, también llamada de _mipmaps_, es una forma
tradicional [@williams_pyramidal_1983] de almacenar una imagen en memoria junto a
versiones re-escaladas de la misma.  y en el caso de Basalt, se utilizan para aplicar el tracker
Lucas-Kanade piramidal presentado en [@pyramidal-lk-paper].

Para la detección de nuevas features,

<!-- TODO: Add grafico ejemplo de un mipmap, quizas el del mismo williams
lawrence, o sino el de basalt -->

La detección de nuevas features en [`addPoints`] es peculiar. Se detectan
unicamente en el nivel

[@pyramidal-lk-paper]: TODO

#### Bundle Adjustment Visual-Inercial
