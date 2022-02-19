<!-- TODO@high: en algún lado voy a tener que hablar y explicar las métricas, quizás acá? sino directamente en la sección de evaluation.md -->

### Conjuntos de Datos

Los sistemas de SLAM y VIO que estudiaremos son sistemas que reciben como
entrada una secuencia de muestras IMU y de cámaras (usualmente estéreo) con
marcas del tiempo en el que fueron capturadas (_timestamps_), mientras que
devuelven como salida una secuencia de poses con una timestamp asociada (una
trayectoria) que el sistema computa como la mejor estimación dados los datos de
entrada.

Para medir el desempeño de estos algoritmos se emplean métricas y conjuntos de
datos (_datasets_) estándar que son regularmente utilizadas en las publicaciones
de estos nuevos sistemas como punto de comparación. Estos conjuntos de datos
tienen que ser capaces de proveer, además de las muestras de sensores, medidas
muy precisas de las trayectorias (_ground truth_) para poder ser utilizadas como
punto de referencia del error en el que una implementación pueda estar
incurriendo.

Considerando que las aplicaciones de SLAM pueden ser muy distintas, existen
multitud de conjuntos de datos con características muy diferentes para la
evaluación en estos contextos. Propiedades como las frecuencias de muestreo,
resoluciones, modelos de calibración, calidad de los sensores, tipos de cámaras,
son algunas de las tantas que pueden referirse a la hora de comparar conjuntos
de datos. Existen datasets enfocados al uso en vehículos automóviles autónomos,
entre ellos el conjunto KITTI [@geigerVisionMeetsRobotics2013] es uno de los más
populares. Otros por su parte centrados en la navegación autónoma de _vehículos
micro aéreos_ (MAV o drones) como lo es el conjunto EuRoC MAV
[@burriEuRoCMicroAerial2016]. El dataset TUM-VI presentado en
@schubertTUMVIBenchmark2018 presenta secuencias capturadas por un camarógrafo
humano que pueden ayudar a aproximar los movimientos que uno esperaría encontrar
en entornos de XR.

Una de las principales dificultades que se presenta a la hora de fabricar uno de
estos datasets, es la calidad de la trayectoria ground truth. En conjuntos como
KITTI, se utilizan sistemas de navegación GNSS (p. ej. GPS) que tienen
precisiones en el orden de centímetros y no resultan adecuadas para XR. Para
lograr precisiones milimétricas, EuRoC y TUM-VI utilizan sistemas de captura de
movimiento (_mocap_) como los ofrecidos por OptiTrack[^optitrack] o
Vicon[^vicon]. Los sistemas de mocap requieren la preparación de habitaciones
especializadas con constelaciones de sensores dispuestos de forma
adecuada[^optitrack-builder], y cada uno de estos sensores tiene costos
significativos. Esto hace que sean pocos los conjuntos de datos con ground
truths tan precisas. En la práctica, EuRoC resulta el más utilizado mientras que
TUM-VI está ganando popularidad.

[^optitrack]: <https://optitrack.com/>
[^vicon]: <https://www.vicon.com/>
[^optitrack-builder]: Simulador de compra de OptiTrack: <https://www.optitrack.com/systems/>

<!-- #if 0 -->
#### Características de los sensores

Nos enfocaremos ahora en describir algunas de las características presentes en
estos datasets y problemas que deben solucionarse para poder ser útiles para un
sistema de SLAM. Estas características no solo hacen referencia a los datasets
pero a cualquier conjunto de cámaras e IMU que utilicemos para generar entradas
a los sistemas de SLAM visuales-inerciales que veremos más adelante.

Para un análisis más profundo de alternativas
de conjuntos de datos referimos al lector al artículo de TUM-VI
[@schubertTUMVIBenchmark2018].
<!-- #endif -->
