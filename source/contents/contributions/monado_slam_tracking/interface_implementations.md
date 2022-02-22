<!-- ### Implementaciones de la interfaz -->

A la hora de implementar la interfaz `slam_tracker` se documentan los tres
métodos principales `push_imu_sample`, `push_frame` y `try_dequeue_pose`
con las precondiciones que el usuario de la interfaz, Monado en este caso, y su
implementación deben cumplir:

1. Debe haber un único hilo productor llamando a los métodos `push_*`
2. Las muestras deben tener marcas de tiempo (_timestamps_) monótonas
   crecientes.
3. La implementación de los métodos `push_*` no debe ser bloqueante.
4. Del punto anterior se desprende que las muestras deben ser procesadas en
   un hilo consumidor separado.
5. Las muestras de imágenes estéreo deben tener la misma timestamp.
6. Las muestras de imágenes estéreo deben ser enviadas de forma intercalada
   en orden izquierda-derecha.
7. Debe haber un único hilo consumidor llamando a `try_dequeue_pose`.

Estas condiciones fueron desarrollándose mientras la interfaz evolucionaba y
nuevos sistemas se iban adaptando. Intentan ser indicaciones que evitarían
implementaciones deficientes mientras que son lo suficientemente generales
como para que todas las soluciones estudiadas puedan cumplirlas.

La precondición $\mathbf{1}$ para el usuario le permite a la implementación utilizar
colas enfocadas al caso de un único productor, de las cuales puede obtenerse
mayor rendimiento comparado a las versiones que no tienen esta limitación. Más
aún, se suelen utilizar colas libres de _locks_ (primitiva de sincronización,
también conocido como _mutex_). El punto $\mathbf{2}$ facilita el trabajo a la
implementación mientras que suele ser trivial de cumplir para el usuario, ya que
los dispositivos tienden a reportar las muestras del mismo tipo en orden
temporal creciente. El punto $\mathbf{3}$ obliga a la implementación de los métodos
`push_*` a terminar lo antes posible sin realizar ningún tipo de procesamiento
en esas funciones. Esto es fundamental, ya que Monado también recibe muestras de
dispositivos mediante colas y simplemente las redirige al `slam_tracker`, y
demorarse en estos métodos hace que las colas internas de Monado se llenen y
muestras se pierdan. El inciso $\mathbf{4}$ aclara en dónde
se procesarían las muestras; dado que no pueden procesarse en los métodos
`push_*` se necesita un hilo consumidor que esté esperando por muestras nuevas
en las distintas colas de la implementación para procesar. El punto $\mathbf{5}$ es un
requerimiento razonable de algunos sistemas, ya que es común que cámaras estéreo
pensadas para SLAM tengan sincronización por hardware de sus timestamps. El
punto $\mathbf{6}$ facilita algunos procedimientos y chequeos en la implementación. Y
finalmente, la precondición $\mathbf{7}$ es similar al punto 1 en donde se le permite a
la implementación utilizar colas de un único consumidor que sean de mayor
rendimiento comparado a otras colas concurrentes.

<!-- TODO@high: Debería haber links a todos los repos en algún lado de la tesis -->

La interfaz `slam_tracker` se implementó en los tres forks presentados en este
trabajo; Kimera, ORB-SLAM3 y Basalt. La idea general de las implementaciones es
similar: permitir a Monado, el usuario de la interfaz, utilizar el sistema de
SLAM/VIO realizando las conversiones adecuadas para poder comunicarse con la
solución subyacente. Sin embargo hay algunas consideraciones a remarcar en cada
versión.

<!-- TODO@def: necesito haber definido el dataset TUM-VI, quizás
referenciarlo una vez que lo haya definido -->

Respecto al manejo de muestras entrantes, Kimera y Basalt encolan las muestras
directamente a las colas de entrada de sus respectivos pipelines que corren en
hilos separados. Para ORB-SLAM3, al ser necesario ejecutar explícitamente el
paso de estimación con el par de imágenes estéreo y muestras IMU nuevas, se
necesitó implementar colas dedicadas para muestras de cámara izquierda, derecha
e IMU, junto a un hilo consumidor que ejecuta la estimación cuando llegan cuadros
nuevos. Cabe mencionar que Basalt no utiliza el tipo `cv::Mat` de OpenCV
como contenedor para sus imágenes a diferencia de los otros sistemas. Más aún,
espera imágenes con intensidad de píxeles de 16 bits para soportar conjuntos de
datos como TUM-VI que provee imágenes de este tipo. Sin embargo, las imágenes
monocromáticas usadas comúnmente en estas aplicaciones suelen utilizar un rango
de 8 bits y por ende los dispositivos generan imágenes de este tipo. Al no haber
una forma sencilla de utilizar 8 bits en Basalt, es necesario realizar una copia
a un tipo de imagen de 16 bits cada vez que se presentan nuevos cuadros. Este es
un punto a mejorar en el futuro sobre Basalt que no se trató de resolver en este
trabajo, ya que no se encontraron problemas de performance incluso con esta
copia innecesaria.

<!-- TODO@def: definir callbacks? -->

Respecto a la cola de poses estimadas, Kimera implementa un sistema de
_callbacks_ que llaman a una función encargada de encolar los resultados del
pipeline tan pronto como estén listos. Basalt por otra parte, expone una cola
que se va llenando con los resultados de la estimación; la implementación de
`slam_tracker` la utiliza directamente, ya que también expone una interfaz de
cola mediante el método `try_dequeue_pose`. ORB-SLAM3 difiere de los dos
anteriores ya que el procesamiento sucede en una llamada a una función
bloqueante que al terminar devuelve la pose estimada. Por lo tanto, nuestra
implementación se encarga de armar la maquinaria necesaria de hilos productores,
hilos consumidores y colas de entrada y salida para hacer que Monado no sea
bloqueado al enviar nuevas muestras de los dispositivos.

Respecto al archivo de configuración referenciado por el parámetro
`config_file`, Basalt por defecto utiliza dos archivos, uno para parámetros de
calibración y el otro para configuraciones del sistema en sí; se necesitó
entonces crear un tipo de archivo nuevo que referencie a estos dos y sea
utilizado como `config_file`. La misma idea se utilizó para Kimera que también
posee múltiples archivos de configuración. ORB-SLAM3 por su parte utiliza un
único archivo por defecto y no necesito de mayores cambios.

Respecto a las interfaces gráficas, todos estos sistemas presentan la
posibilidad de visualizar, al menos, la trayectoria estimada junto a las
features detectadas en los cuadros entrantes como se muestra en la
\figref{fig:trackers-ui}. En todos los casos, siempre se intenta permitir la posibilidad
de utilizar estas herramientas de visualización de forma opcional al utilizar la
clase `slam_tracker`. Para Kimera y ORB-SLAM3 las interfaces funcionan
automáticamente al habilitarlas en los archivos de configuración, mientras que
Basalt utiliza sus herramientas de visualización de manera más ad hoc y por lo
tanto fue necesario implementar una clase de visualización dedicada para el
`slam_tracker`.

<!-- TODO@maybe: No hablo de stereorectify necesario para orb-slam3, esto daría
pie para explicar lo que es ese proceso.
<!-- TODO@maybe: Tampoco hablo de las problematicas con las que hubo que
lidiar respecto a shared libraries (https://www.akkadia.org/drepper/dsohowto.pdf) -->

\fig{fig:trackers-ui}{source/figures/trackers-ui.pdf}{Visualizadores de SLAM trackers}{%
Las distintas interfaces gráficas y formas de visualizar presentadas por cada
uno de los sistemas adaptados. Arriba a izquierda Kimera, ORB-SLAM3 a derecha;
abajo Basalt.
}

\FloatBarrier
