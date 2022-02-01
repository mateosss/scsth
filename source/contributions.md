<!-- TODO: Qué es XR -->

# Contribuciones

## Contexto

Por su naturaleza, el área de XR involucra una gran cantidad de partes
interconectadas y de dispositivos muy diversos con configuraciones difíciles de
generalizar, y más aún de predecir. Por esta razón hasta hace muy poco tiempo no
existían estándares razonables en el área lo cual agravaba la situación con un
ecosistema altamente fragmentado en soluciones propietarias que causaban a los
desarrolladores de aplicaciones finales grandes problemas. En el mejor de los
casos, la carga de soportar los distintos SDK propietarios recaía sobre
frameworks y motores de juegos (p. ej. _Unreal Engine_, _Unity_, _Godot_) y esto
forzaba a los desarrolladores a elegir alguna de estas soluciones para realizar
su aplicación de XR. En caso de no querer hacerlo, se vería obligado a realizar
un esfuerzo no trivial para portar su aplicación a cada uno de estos SDK,
y eso sin considerar el manejo de características especiales que algunas
plataformas exponen y otras no.

Luego de unos años de sufrir esta fragmentación, en julio de 2019 se presenta la
primera versión de _OpenXR_ de la mano del _Khronos Group_. El Khronos Group es
un consorcio abierto y sin fines de lucro compuesto de 170 organizaciones que
desarrolla estándares en distintas áreas de la industria como computación
gráfica, (_OpenGL_, _Vulkan_), computación paralela (_OpenCL_, _SYCL_) y, con
OpenXR, realidad virtual y aumentada entre otras. OpenXR por su parte, provee
una API estandarizada con soporte para extensiones de fabricante que permiten
añadir características peculiares de ser necesitadas por algún fabricante en
particular. El estándar ha tenido un gran éxito al haber sido adoptado por una
gran cantidad de fabricantes (Fig. @fig:openxr-companies) como reemplazo a sus
antiguos SDK propietarios. De esta forma, los motores de juego y desarrolladores
solo necesitan interactuar con una única API (Fig. @fig:openxr) que además les
permite aprovechar cualquier característica peculiar ofrecida por alguna
extensión.

![
**Antes de OpenXR (izquierda)** aplicaciones y motores necesitaban código
propietario separado para cada dispositivo en el mercado. **OpenXR (derecha)**
provee una única API multiplataforma de alta performance entre las aplicaciones
y todos los dispositivos compatibles
](source/figures/openxr.png "OpenXR"){#fig:openxr width=100%}

![
Compañías respaldando públicamente el estándar OpenXR
](source/figures/openxr-companies.png "Compañías OpenXR"){#fig:openxr-companies
width=100%}

OpenXR es exclusivamente la [especificación][openxr-spec] de una API y por lo
tanto requiere una implementación, o _runtime_, sobre el que ser ejecutado. Las
implementaciones son provistas por los distintos fabricantes interesados en
soportar el estándar, en la Figura @fig:openxr-companies vemos algunas de las
implementaciones ya desarrolladas. En este trabajo nos enfocaremos en una de
ellas, _Monado_. Monado es un runtime (por ahora el único) de la especificación
OpenXR de código abierto, licenciada bajo la _Boost Software License 1.0
([BSL-1.0])_. La plataforma principal sobre la que Monado corre y se desarrolla
es GNU/Linux, pero es capaz de ser ejecutarse en otras como Android y Windows.
Su desarrollo está soportado por _Collabora Ltd._, quien es parte del grupo de
trabajo de OpenXR desde sus inicios. Las contribuciones a Monado listadas en
esta sección fueron hechas durante una pasantía en Collabora.

Además de proveer una implementación de OpenXR, Monado es altamente modular e
implementa distintos componentes reutilizables para XR como un compositor
especializado para realidad virtual; controladores para una gran variedad de
dispositivos, incluyendo hardware propietario y de consumo masivo sobre los que
la comunidad ha realizado ingeniería inversa para poder utilizar; herramientas
varias de calibración y configuración de hardware; así como también distintos
sistemas de fusión de sensores para tracking; y recientemente incluso un módulo
de localización de manos mediante visión por computadora y aprendizaje
automático.

Una característica faltante en Monado era la posibilidad de realizar
localización visual-inercial mediante sistemas de SLAM/VIO. Este tipo de
tracking ha cobrado gran popularidad en los últimos años por resultar sumamente
convenientes al no requerir sensores externos al dispositivo de XR. Sistemas de
este tipo son empleados en productos como el _Meta Quest_, los cascos _Windows
Mixed Reality_ o incluso los SDK _ARCore_ y _ARKit_ presentes en dispositivos
móviles. Desafortunadamente, todas estas soluciones son privativas y, por lo
tanto, no es posible obtener acceso a sus códigos fuentes para reusarlos,
modificarlos o simplemente estudiarlos sin obtener licencias especiales de sus
fabricantes. Más aún, existen compañías que se especializan en desarrollar
soluciones comerciales de SLAM como _SLAMCore_, _Arcturus_ y _Spectacular AI_
entre otras.

Este trabajo se concentró entonces en el estudio de implementaciones de código
abierto de sistemas de tracking visual-inercial (ya sea mediante SLAM o
solamente VIO) y en la integración de estos sobre Monado. Se necesitó armar la
infraestructura para soportar una interacción modular con los sistemas mediante
el desarrollo de interfaces, herramientas, controladores, y mejoras
principalmente en Monado, pero también en los sistemas a integrar o en sus
_forks_ (clones específicos de las implementaciones de SLAM/VIO para uso en
Monado).

<!-- TODO@def: Ya expliqué qué es el acrónimo VR? -->
<!-- TODO@def: Ya expliqué que es XR no es un acrónimo para "extended"? -->
<!-- TODO@def: SDK, API -->

<!-- TODO: Todavía no se como referenciar links en la tesis -->

[openxr-spec]: TODO
[bsl-1.0]: TODO

<!-- TODO@def: Ya explqué que es tracker, tracking? uso esos terminos o me voy a localizar/rastrear/seguir/ubicar/posicionar -->

## Tracking por SLAM para Monado

En esta sección explicaremos los distintos módulos y funcionalidad implementada
en Monado para permitirle proveer tracking mediante SLAM/VIO a distintos
controladores de dispositivos y de esta forma, a las aplicaciones OpenXR que
utilizan estos dispositivos como medios de interacción y corren sobre Monado.
Cabe aclarar que a partir de ahora usaremos de forma intercambiable los términos
SLAM y VIO, ya que, a pesar de ser distintos, para los fines prácticos de la
implementación son equivalentes: piezas de software que consumen imágenes y
muestras de IMU y devuelven poses estimadas como resultado. Es por esto que
hablaremos de un localizador SLAM o _SLAM tracker_ que se ha implementado para
referirnos a una única funcionalidad que soporta tanto sistemas externos de SLAM
y como de VIO.

Antes de comenzar, vale la pena entender la arquitectura general de Monado como
se muestra en la Figura @fig:monado-arch. Una aplicación que hace uso de OpenXR
mediante Monado puede ser corrida en dos modalidades dependiendo de como se
compiló el runtime. De la forma tradicional, se compila como una librería de
manera **autónoma**, significando que cuando la aplicación intenta cargar
dinámicamente alguna implementación de OpenXR provista por el sistema, se enlaza
la librería compartida (o _shared library_) de Monado, y al interactuar con cualquier
interfaz a OpenXR, se correría tal procedimiento en el mismo hilo que la
aplicación consumidora. Esta modalidad puede tener ciertos beneficios para
depuración de código, pero el modo más usual de compilar y correr Monado es
mediante _Inter-Process Communication_ o _IPC_. De esta manera el runtime se
corre en un proceso independiente que debe ser lanzado con anterioridad a
cualquier aplicación OpenXR. Lo que se termina enlazando a la aplicación final
es simplemente un cliente IPC que es capaz de comunicarse con Monado. Esto
ofrece ventajas como la posibilidad de correr múltiples aplicaciones
sobre la misma instancia del runtime. Además, se quita la necesidad de ejecutar
ambos procesos sobre el mismo nodo de cómputo, lo cual facilita la posibilidad
de tener realidad virtual renderizada en la nube.

<!-- TODO@fig: Tiene que estar en español y agregar "Filtrado" arriba de "Prediction" -->
<!-- TODO@fig: Podría usar los nombres `TrackerSlam` y `slam_tracker` me
parece por que los referencio bastante -->
![
Arquitectura de Monado.
](source/figures/monado-arch.pdf "Arquitectura de Monado"){#fig:monado-arch width=100%}

\FloatBarrier

No interiorizaremos en los aspectos de comunicación con la _plataforma_ ni del
_compositor_ de Monado, pero es bueno saber que estos son partes significativas
del runtime. Son los _controladores_ (o _drivers_) específicos en Monado los que
interactúan con el hardware especializado como cascos, controles, cámaras, entre
otros dispositivos que quieran utilizarse para la experiencia de XR. Sensores
como las IMU y cámaras sobre los que adquirir las muestras necesitarán ser
implementados en este nivel. Finalmente, hay una gran variedad de módulos
auxiliares reutilizables que exponen funcionalidades matemáticas, de interacción
con el sistema operativo, con OpenGL o Vulkan, entre otras. Es en estos módulos
auxiliares en donde encontramos componentes relacionados exclusivamente al
problema tracking y a tipos específicos de tracking. Se implementan herramientas
de calibración de cámaras, de depuración, filtros de distinto tipo (p. ej.
_Kalman_ y _low-pass_), entre otra algoritmia genérica de fusión de sensores.
Conforman este módulo también sistemas completos de tracking para _PlayStation
Move_, _PlayStation VR_, y tracking de manos en general. Es aquí entonces en
donde se comienza la implementación del SLAM tracker presentado en este
trabajo.

La implementación de un pipeline en Monado que permita la comunicación entre
dispositivos, sistemas de SLAM y la aplicación OpenXR requirió desarrollar la
infraestructura y herramientas necesarias dentro de Monado. El pipeline en
cuestión está esquematizado en la Figura @fig:slam-tracker-dataflow. Este,
requiere un gran nivel de modularidad, ya que sus componentes fundamentales
necesitan poder ser intercambiables: dispositivos, aplicaciones y el sistema que
provee el SLAM en sí. El resto de esta subsección está dedicada a explicar la
infraestructura y los distintos componentes que se necesitaron implementar y
adaptar para obtener un pipeline de SLAM modular corriendo en Monado como se
intenta mostrar en la Figura @fig:slam-tracker-dataflow.

<!-- TODO@fig: Agregar a esta figura referencia al filtrado de poses -->
<!-- TODO@fig: Hacer versión final -->

![
Diagrama esquemático de como ocurre el flujo de los datos desde que se generan
las muestras en los dispositivos XR hasta que la aplicación OpenXR obtiene una
pose utilizable. Notar que las flechas esconden múltiples hilos de ejecución,
colas de procesamiento, y desfasajes temporales con los que hay que lidiar en la
implementación.
](source/figures/slam-tracker-dataflow.pdf "Flujo de datos de la implementación"){#fig:slam-tracker-dataflow width=100%}

\FloatBarrier

### Interfaz externa

<!-- TODO: mencionar que ORB-SLAM3 está en un fork separado de monado por GPL -->

Desde un principio se entendió que se necesitaría utilizar sistemas ya
desarrollados como punto de partida. Estos sistemas son complejos y suelen
utilizar conceptos teóricos de significativa profundidad, por lo que su
creación suele estar limitado a grupos de investigación expertos durante
tiempos significativos de desarrollo. Los tres sistemas estudiados por ejemplo,
promedian las 25.000 líneas de código (o 25 _KLOC_) cada uno.

Ahora bien, en muchos casos, haber intentado integrar el código del sistema
directamente dentro de un componente de Monado no era una opción. Dejando de
lado las dificultades técnicas, los problemas de compatibilidad de licencia
fueron de particular interés. La gran mayoría de sistemas SLAM producidos en la
academia son liberados bajo licencias abiertas “contagiosas” como _GPL_ que
obligan a desarrolladores que utilizan código del sistema a liberar y licenciar
su código con la misma licencia. Esto contrasta con la licencia abierta y
permisiva de Monado, la _BSL-1.0_, que no impone restricciones sobre como los
usuarios deben licenciar su código.

Estas fueron algunas razones para intentar desacoplar el sistema a utilizar lo
más que se pueda de Monado. Además, considerando la naturaleza experimental de
este trabajo, la posibilidad de que más de un sistema necesitase ser
integrado era razonable.

<!-- TODO@def: que es OpenCV -->

Monado está desarrollado principalmente en el lenguaje C, pero gran parte de su
código de tracking está implementado en C++ al igual que todos los sistemas de
SLAM contemplados. Adicionalmente tanto Monado como estos sistemas suelen hacer
un uso extensivo de la librería _OpenCV_, y en particular su clase contenedora
de imágenes/matrices `cv::Mat`. Es por esto que se terminó optando por el uso de
un archivo _header_ C++, en el cual se declara la clase `slam_tracker` que será
utilizada por Monado como punto de comunicación con sistemas de SLAM arbitrarios
y se utilizan `cv::Mat` como contenedor de imágenes. Luego de varias iteraciones
la clase `slam_tracker` tiene una interfaz que, quitando detalles de tipos de
C++, se puede resumir en algo como esto:

<!-- TODO: linkear la clase slam_tracker en gitlab? -->

``` {#lst:slam-tracker-def .cpp caption="Interfaz a implementar por sistemas de SLAM"}
class slam_tracker {
public:
  // (1) Constructor y funciones de inicio/fin
  slam_tracker(string config_file);
  void start();
  void stop();

  // (2) Métodos principales de la interfaz
  void push_imu_sample(
     long timestamp, vec3 accelerometer, vec3 gyroscope);
  void push_frame(long timestamp, cv::Mat frame, bool is_left);
  bool try_dequeue_pose(
    long &out_timestamp, vec3 &out_position, quat &out_rotation);

  // (3) Características dinámicas opcionales
  bool supports_feature(int feature_id);
  void* use_feature(int feature_id, void* params);

private:
  // (4) Puntero a la implementación (patrón PIMPL)
  void* impl;
}
```

Este header está presente en Monado, pero su implementación no. Esta debe ser
provista por el sistema externo, lo cual implica tener que mantener una copia, o
_fork_, levemente modificado de los distintos sistemas que se quieran utilizar,
ver Figura @fig:slam-tracker-hpp.

<!-- TODO@fig: La parte de basalt está mal, no hay hilo consumidor de muestras,
el hilo ese estaría en las "Partes Internas de Basalt". Otros problemas es que
no se relaciona las colas dibujadas con nada, ni con Monado ni con la copia de slam_tracker.hpp -->

![
Interacción entre Monado y sistemas SLAM mediante la interfaz en C++.
](source/figures/slam-tracker-hpp.pdf "Interfaz de SLAM tracker"){#fig:slam-tracker-hpp width=100%}

La versión actual de esta clase es el
resultado de varias iteraciones y generaliza adecuadamente los tres sistemas
actualmente en uso. Algunas consideraciones de los puntos marcados en el código:

1. El parámetro `config_file` del constructor surge, ya que todos los sistemas
   con los que se trató requieren proveer información de calibración y puesta a
   punto de parámetros previo a la corrida mediante un archivo de configuración.
   Además estos sistemas suelen tener etapas de creación e inicialización de
   recursos, así como de liberación de los mismos que quedan representados en el
   par de métodos `start()`/`stop()`.

2. Los sistemas corren en hilos separados de Monado y es por esto que es
   fundamental implementar colas concurrentes a la hora de intercambiar datos.
   Monado ingresa muestras mediante los métodos `push_imu_sample` y `push_frame`
   mientras que sondea si hay poses ya estimadas por el sistema y las obtiene
   mediante `try_dequeue_pose`.

3. Algo natural del desarrollo de una interfaz de algo que no se conoce del todo
   es que va a haber varios cambios en la misma durante su creación. Si además
   esta interfaz es compartida por múltiples sistemas y repositorios, mantener
   todas las versiones sincronizadas se vuelve rápidamente insostenible. Una
   forma de aliviar este problema fue la implementación de características
   dinámicas. En ellas, Monado evalúa antes de utilizar alguna característica
   específica si el sistema la implementa. El ejemplo para el que esto fue
   utilizado fue la automatización del envío de datos de calibración sin pasar
   por el archivo `config_file`. Se reserva una `feature_id` para tal característica en
   la nueva versión de `slam_tracker.hpp` de Monado y del fork particular, se
   implementa tal característica en este último, y en Monado tenemos cuidado de
   solo utilizarla si el sistema la reporta como disponible. De esta forma nos
   evitamos tener que actualizar la versión del header de otros forks en los
   que, o la característica no tenga sentido, o simplemente no se desee
   implementar de momento.

4. El miembro `impl` es una forma de ligar la definición compacta de
   `slam_tracker` con una clase que implementa el estado y métodos privados
   necesarios para proveer la funcionalidad requerida. Este patrón de desarrollo
   es usualmente conocido como _pointer to implementation_ (o _PIMPL_), a `impl`
   se lo denomina un _puntero opaco_ [@lakosLargeScaleSoftwareDesign1996].

Esta interfaz no es perfecta: no contempla magnetómetros, asume una
configuración de a lo sumo dos cámaras, asume que el sistema utiliza OpenCV y es
difícil de actualizar con cambios no contemplados por el concepto de
características dinámicas. A pesar de estos problemas, ha sido suficientemente
buena para generalizar todos los sistemas propuestos y correrlos con una
performance adecuada.

\FloatBarrier

### Implementaciones de la interfaz

A la hora de implementar la interfaz `slam_tracker` se documentan en los tres
métodos principales `push_imu_sample`, `push_frame` y `try_dequeue_pose`
precondiciones que el usuario de la interfaz, Monado en este caso, y su
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
como para que todas las soluciones estudiadas puedan acatarlas.

La precondición **1** para el usuario le permite a la implementación utilizar
colas enfocadas al caso de un único productor, de las cuales puede obtenerse
mayor rendimiento comparado a las versiones que no tienen esta limitación. Más
aún, se suelen utilizar colas libres de _locks_ (primitiva de sincronización,
también conocido como _mutex_). El punto **2** facilita el trabajo a la
implementación mientras que suele ser trivial de cumplir para el usuario, ya que
los dispositivos tienden a reportar las muestras del mismo tipo en orden
temporal creciente. El punto **3** obliga a la implementación de los métodos
`push_*` a terminar lo antes posible sin realizar ningún tipo de procesamiento
en esas funciones. Esto es fundamental, ya que Monado también recibe muestras de
dispositivos mediante colas y simplemente las redirige al `slam_tracker`, y
demorarse en estos métodos hace que las colas internas de Monado se llenen y
muestras se pierdan. El inciso **4** es simplemente una aclaración de en dónde
se procesarían las muestras; dado que no pueden procesarse en los métodos
`push_*` se necesita un hilo consumidor que esté esperando por muestras nuevas
en las distintas colas de la implementación para procesar. El punto **5** es un
requerimiento razonable de algunos sistemas, ya que es común que cámaras estéreo
pensadas para SLAM tengan sincronización por hardware de sus timestamps. El
punto **6** facilita algunos procedimientos y chequeos en la implementación. Y
finalmente, la precondición **7** es similar al punto 1 en donde se le permite a
la implementación utilizar colas de un único consumidor que sean de mayor
rendimiento comparado a otras colas concurrentes.

<!-- TODO: Debería haber links a todos los repos en algún lado de la tesis -->

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
e IMU, junto a un hilo consumidor que ejecuta la estimación cuando cuadros
nuevos arriban. Cabe mencionar que Basalt no utiliza el tipo `cv::Mat` de OpenCV
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
_callbacks_ en el cual una función que encola los resultados del pipeline es
llamada tan pronto como estén listos. Basalt por su parte ya expone una cola con
las estimaciones computadas que la implementación de `slam_tracker` simplemente
utiliza. ORB-SLAM3 devuelve la estimación de la misma llamada explícita al
estimador, y nuestra implementación se encarga de encolar esos resultados que
luego serán consultados por Monado mediante `try_dequeue_pose`.

Respecto al archivo de configuración referenciado por el parámetro
`config_file`, Basalt por defecto utiliza dos archivos, uno para parámetros de
calibración y el otro para configuraciones del sistema en sí; se necesitó
entonces crear un tipo de archivo nuevo que referencie a estos dos y sea
utilizado como `config_file`. Kimera a su vez también posee múltiples archivos
que son referenciados por uno central. ORB-SLAM3 por su parte tiene un único
archivo de configuración.

<!-- TODO: fotos de las UIs, links a los videos? -->

Respecto a las interfaces gráficas, todos estos sistemas presentan la
posibilidad de poder visualizar, al menos, la trayectoria estimada junto a las
features detectadas en los cuadros entrantes como se muestra en la Figura
@fig:trackers-ui. En todos los casos, siempre se intenta permitir la posibilidad
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

<!-- TODO@fig: Varias figuras están ocupando toda una página por si solas y
dejando una banda de espacio en blanco. -->

![
Las distintas interfaces gráficas y formas de visualizar presentadas por cada
uno de los sistemas adaptados. Arriba a izquierda Kimera, ORB-SLAM3 a derecha;
abajo Basalt.
](source/figures/trackers-ui.pdf "Visualizadores de SLAM trackers"){#fig:trackers-ui width=100%}

\FloatBarrier

### Clase adaptadora

Para interactuar con la interfaz que detallamos en la sección anterior, se
implementa en Monado una clase adaptadora en el módulo auxiliar de tracking
(recordar Figura @fig:monado-arch) y que sirve de nexo entre los
controladores de dispositivos de hardware y la interfaz `slam_tracker`. Este
adaptador recibe el nombre, un poco confuso, de `TrackerSlam` siguiendo las
convenciones de Monado para con los trackers ya existentes.

El funcionamiento de `TrackerSlam` es sencillo, los controladores que quieran
ser localizados por SLAM y puedan proveer imágenes y muestras de IMU deben
instanciar este adaptador e inicializarlo. Por detrás, esto simplemente llama a
los métodos adecuados de la interfaz `slam_tracker` con el sistema externo.
Ahora bien, se aprovecha este adaptador para proveer dos funcionalidades
fundamentales que escapan al alcance de los sistemas de SLAM/VIO y serán
explicados a continuación: **predicción** y **filtrado** de poses.

<!-- TODO: Hago las "Notas" así? hay una mejor manera? quizás a un
costado de la página o con un recuadro tcolorbox como vi en un video -->

_Nota: es debatible si el añadido de estas funcionalidades haría que
`TrackerSlam` deje de ser considerada una clase adaptadora, ya que como veremos,
ambas pueden ser deshabilitadas en tiempo de ejecución._

#### Predicción de poses

##### El problema

Las aplicaciones XR requieren poder localizar constantemente a los distintos
dispositivos de entrada y salida soportados que son utilizados por el usuario.
En la especificación de OpenXR las dos principales funciones que le permiten a
la aplicación pedirle al runtime las poses de estos dispositivos son
`xrLocateSpace` y `xrLocateViews`. La primera se utiliza para solicitar poses de
dispositivos “comunes” (suelen ser distintos tipos de mandos) mientras que la
segunda es un poco más compleja, ya que concierne a la ubicación de las pantallas
que renderizan la escena (p. ej. la ubicación de las pantallas de un casco VR).
Para nuestro propósito, podemos resumir las signaturas de ambas funciones a:

```C++
XrPosef xrLocateSpace(XrSpace id, XrTime time);
XrPosef xrLocateViews(XrSpace id, XrTime time);
```

Ambas devuelven una pose a un tiempo `time` para el “_espacio_” identificado por
`id`. Un espacio o _espacio de referencia_ es un término utilizado en la
especificación para diferenciar cualquier punto que nos interese trackear desde
la aplicación y que en definitiva identifica a un sistema de referencia inercial
con rotaciones.

<!-- TODO: Acá cuando menciono un mando quizás estaría bueno tener una imagen de un mando de WMR o algo así? -->

Para obtener estos espacios, la aplicación solicita las características que
desea. Si se solicitara el espacio de un control o mando el runtime, Monado en
este caso, intentará conseguir el más adecuado dentro de los disponibles en el
sistema. Entonces, la aplicación OpenXR es indiferente a qué dispositivos están
siendo utilizados, ni siquiera se asumen que estos espacios sean dispositivos,
podrían ser cualquier otro objeto de interés que está siendo localizado por
mecanismos externos (por visión por computadora por ejemplo) o incluso
dispositivos emulados por software[^qwerty-driver]. Los espacios que
aplican a nuestro caso son aquellos que representaran dispositivos que posean
sensores IMU y cámaras que puedan utilizarse en nuestros sistemas de SLAM/VIO.

<!-- TODO@ref: Todos los MR importantes deberían estar listados y referenciados
en alguna parte del trabajo -->

[^qwerty-driver]: Una de las primeras contribuciones realizadas para
familiarizarse con el código fuente de Monado fue la implementación del
controlador `qwerty` que le permite a los usuarios emular de forma modular un
casco y/o mandos mediante teclado y ratón.
<https://gitlab.freedesktop.org/monado/monado/-/merge_requests/714>

Otro importante aspecto a considerar es que el punto en el tiempo `time` para la
cual la pose debe ser estimada es provisto por el usuario, y como tal, resulta
arbitrario para el runtime. Sin embargo los sistemas de SLAM/VIO suelen ser
sistemas de tiempo discreto, es decir solo dan estimaciones para puntos en el
tiempo para los cuales tienen muestras. En el mejor de los casos esto implica
que pueden dar una estimación por cada muestra de IMU, las cuales vienen a altas
frecuencias (p. ej. 200hz); Kimera cumple con esto. En el caso más usual sin
embargo, y el que más nos afecta en este trabajo, las estimaciones vienen a la
misma frecuencia que los cuadros de las cámaras. Esta frecuencia suele ser al
menos un orden de magnitud menor (p. ej. 20hz); ORB-SLAM3 y Basalt funcionan de
esta manera.

Para complicar más las cosas, los tiempos en los que el programador solicita las
poses suelen estar ligados a momentos en los cuales hay que renderizar un nuevo
cuadro en la pantalla del usuario. Al ser este un proceso que (en el caso usual)
ocurre enteramente en el mismo nodo de cómputo, suelen ser tiempos muy cercanos
al presente. Para el pipeline de SLAM sin embargo, siempre nos encontramos
levemente en el pasado por tener que lidiar con las demoras inherentes a la
captura de muestras, las transmisiones de datos y los tiempos de cómputo
significativos de los sistemas de SLAM.

##### Análisis de un ejemplo

![
Línea de tiempo con timestamps normalizadas. El evento `REQUEST_TO_PREDICTION`
significa algo.
](source/figures/prediction-timeline.png "Línea de tiempo de predicción"){#fig:prediction-timeline width=100%}


En la Figura @fig:prediction-timeline se puede apreciar una captura de pantalla
de la interfaz de *Perfetto* [^perfetto-web] que, en conjunto con *Percetto*
[^percetto-web], son herramientas de medición de tiempos preferidas para Monado.
Esta captura es sobre una corrida en tiempo real con Monado, Basalt y una cámara
RealSense D455 con imágenes estéreo de resolución 640x480 a 30 cuadros por
segundo. La figura muestra un tramo de unos 35 ms con la particularidad de que
el tiempo en el que el usuario pide una predicción y el par estéreo de imágenes
son capturadas por la cámara coinciden en `[A]`. Como la tarea de renderizado
para esta captura ocurría a unos 60 cuadros por segundo, tenemos que
aproximadamente dos predicciones (en `[A]`, `[D]`) son solicitadas entre cada
muestra de la cámara (`[A]` y `[G]`).

\FloatBarrier

[^perfetto-web]: Librería de perfilación Perfetto: <https://perfetto.dev>
[^percetto-web]: Wrapper de Perfetto para C: <https://github.com/olvaffe/percetto>

A tiempo `[C]` las imágenes llegan al host luego de haber sido transferidas por
un cable USB 3.2 con una demora de unos 13.5 ms representada por la barra
`SHOT_TO_RECEIVED`. En ese momento ocurre una pequeña copia de Monado hacia
Basalt `RECEIVED_TO_PUSHED` y luego de unos 12 ms representados por
`PUSHED_TO_PROCESSED`, a tiempo `[F]`, la pose estimada para el tiempo `[A]`
está computada. Es decir, tenemos una demora de unos 25.5 ms desde que la
muestra es capturada hasta que el sistema de SLAM/VIO es capaz de estimar la
pose correspondiente al momento de captura de la muestra. Cabe aclarar que estos
tiempos son muy variables incluso en la misma corrida, al depender de la calidad
de la conexión USB, el sistema utilizado, y las propias muestras que pueden
complicar las iteraciones de los algoritmos de optimización que ocurren en el
sistema.

Por otro lado, tenemos que a tiempo `[A]`, la aplicación OpenXR solicita a
Monado una predicción de a dónde el runtime piensa que el dispositivo se va a
encontrar 7 ms en el futuro, en `[B]`. Cabe aclarar que la solicitud debe
ser respondida de forma inmediata y la barra `REQUEST_TO_PREDICTION` no implica
ninguna espera hasta `[B]`, es solo una forma de visualizar los 7 ms.
Notar que en ese punto, todavía faltan 25.5 ms para tener la predicción de
Basalt para `[A]`, más aún, una predicción dada por Basalt para el futuro
`[B]` ni siquiera existirá, ya que el sistema solo estima poses para los tiempos
de las muestras, es decir la próxima estimación correspondería al tiempo `[G]`.
Además de esto, tenemos que mientras todavía se está procesando la muestra, otra
petición a tiempo `[D]` para `[E]` debe ser respondida.

En conclusión, tenemos un **desfasaje temporal** que hace que las poses
estimadas siempre estén levemente en el pasado; en el tramo seleccionado fue de
25.5ms (más los 7 ms de predicción), pero es variable durante la corrida.
Además, las poses se estiman para **puntos discretos** de tiempo, mientras que
el usuario puede pedir una predicción para cualquier punto arbitrario. Entonces,
si queremos ser capaces de proveer al usuario una pose para el tiempo
solicitado, necesitemos implementar formas de interpolar y **_predecir_** la
ubicación de un espacio. Es decir, no utilizamos las poses devueltas por el
sistema de SLAM/VIO de forma directa, sino como parte fundamental de un
procedimiento constante de predicción que se realiza del lado de Monado. En este
se intenta utilizar todos los datos disponibles en el runtime para proveer la
pose más razonable en el punto de tiempo requerido.

##### Implementación

Se encara la solución a estos problemas de manera progresiva y haciendo uso de
algunas de las herramientas e ideas ya presentes en Monado.

Dentro de Monado, el concepto de espacio de referencia o `XrSpace` de de OpenXR,
es nombrado como una _relación espacial_ y se representa con un `struct` muy
similar al siguiente.

```c++
struct xrt_space_relation {
  struct vec3 position;
  struct quat orientation;
  struct vec3 linear_velocity;
  struct vec3 angular_velocity;
};
```

En él, no solo se guarda la información de la pose (`position` y `orientation`)
sino que además tenemos el estado de la velocidad lineal y angular de este
espacio. Esto es muy útil, ya que si sabemos que a tiempo $t_1$ tenemos cierto
espacio con pose $T_1 \in SE(3)$ y velocidades $v_1, \omega_1 \in \R^3$, podemos
predecir que a un tiempo $t_2 = t_1 + \Delta t$ tendremos el espacio con pose
$T_2 = \Delta T \ T_1$ con

<!-- TODO@def: necesito operador hat y exp acá -->

<!-- $$ -->
\begin{align}
\label{eq:predicted-space-delta}
\Delta T = \begin{bmatrix}
Exp(\Delta t \ \hat\omega) & \Delta t \ v \\
0 & 1
\end{bmatrix} \in \R^{4x4}
\end{align}
<!-- $$ -->


<!-- TODO@style: linkear lst:slam-tracker-def dice "Apartado" en vez de "Fragmento",
cuando lo intenté arreglar no pude y renegué mucho -->

Monado provee varias herramientas que facilitan tareas que suelen ser
recurrentes en diversos sistemas de tracking. La tarea de estimar espacios
futuros basándose en uno dado con sus velocidades es una de estas
funcionalidades ya incluidas. Más aún, Monado implementa una estructura de datos
que permite almacenar un “historial” de estos espacios en una cola circular y
generar las interpolaciones y extrapolaciones, tanto a futuro como a pasado,
necesarias para cualquier timestamp requerida por un usuario. Para las
interpolaciones se utiliza una simple interpolación lineal^[En el caso de la
orientación es una interpolación esférica lineal o _slerp_
<https://en.wikipedia.org/wiki/Slerp#Quaternion_Slerp>] o _lerp_ de a trozos
entre cada par de espacios del historial. Para extrapolar hacia el futuro, se
usa la pose y velocidad almacenada en el espacio más reciente del historial para
realizar el cómputo con $\Delta T$ como se definió en la
[](#eq:predicted-space-delta). Simétricamente para extrapolar hacia el pasado
lejano[^openxr-time-limits], o sea fuera del registro del historial, se utilizará el espacio más
antiguo almacenado y $\Delta T^{-1}$.

<!-- TODO@ref: la cita del autor "khronos group inc" se ve muy rara -->

[^openxr-time-limits]: La especificación de OpenXR tiene una sección dedicada a
las restricciones y condiciones a los que el runtime está sujeto respecto a
solicitudes en el pasado y en el futuro por parte del usuario. Ver
[@thekhronosgroupinc.OpenXRSpecification, secc. 2.14]

Sería razonable, como primera aproximación a nuestro problema, utilizar este
historial de espacios. Esto nos garantiza que podamos proveerle al usuario una
pose para cualquier punto arbitrario en el tiempo que solicite, basándonos en
las estimaciones del sistema de SLAM que asumimos son precisas. Sin embargo, un
leve problema que surge es que no existe ningún requerimiento para los sistemas
sobre la estimación de velocidades, ya que no todos estiman esta variable. La
interfaz `slam_tracker.hpp` solo garantizan la estimación de la posición y
orientación del dispositivo como puede verse en su definición en el
[](#lst:slam-tracker-def). Lo que haremos para solventar esto es computar las
velocidades con base a los pares de poses adyacentes que tengamos en el
historial. Estas poses tienen su timestamp correspondiente, entonces es sencillo
computar la diferencia entre las mismas respecto a la unidad de tiempo, dando
como resultado una estimación de la velocidad del espacio. La Figura
@fig:prediction-with-space-history muestra como funcionaría este tipo de
predicción en un ejemplo simplificado en 2D y en el que asumimos que las poses
estimadas por el sistema de SLAM/VIO coinciden perfectamente con la trayectoria
real del dispositivo.

![
Ejemplo de predicción con el historial de espacios. Se asume que las poses
estimadas por el sistema de SLAM son perfectas por simplicidad.
](source/figures/prediction-with-space-history.pdf "Predicción con historial de espacios"){#fig:prediction-with-space-history width=100%}

\FloatBarrier

<!-- TODO@def: Estoy caminando alrededor del tema de los cuaterniones muy fuerte. -->

Esto es una buena primera solución al problema, y es la opción más básica que la
clase adaptadora `TrackerSlam` le ofrece a los usuarios de Monado.
Desafortunadamente, si vemos el ejemplo estudiado en la Figura
@fig:prediction-timeline notaremos que la frecuencia de poses que se computan es
muy baja en comparación a la cantidad de veces que la aplicación OpenXR requiere
una nueva prdicción. En el ejemplo se tenían muestras (y por ende estimaciones)
a 30 cuadros por segundo mientras que se renderizaba a 60. En ese ejemplo se
está utilizando un monitor de computadora estándar como pantalla, pero en cascos
de realidad virtual sin embargo, las frecuencias de renderizado alcanzan
fácilmente los 90 o 120 cuadros por segundo, haciendo que la cantidad de
predicciones que hacemos entre estimación y estimación crezca. Esto empeora la
calidad de las predicciones significativamente, generando movimientos imprecisos
y ruidosos, y agravando los efectos de _motion sickness_ o
_cinetosis_[^cinetosis] que estas experiencias pueden producir.

[^cinetosis]: <https://es.wikipedia.org/wiki/Cinetosis>

Para mejorar nuestras predicciones, visto el problema de que las estimaciones
computadas se encuentran muy espaciadas, respecto a las peticiones de
predicción, vamos a utilizar las muestras de IMU. Estas vienen usualmente a
frecuencias mucho mayores que las de renderizado; 250 Hz en el caso del ejemplo
estudiado en la Figura @fig:prediction-timeline. Además, a pesar de sufrir de
severos problemas de drift, al utilizarlas en ventanas cortas de tiempo (unos
pocos milisegundos), estos se ven reducidos en gran medida y la odometría que
sus sensores proveen resulta suficientemente precisa.

La clase adaptadora tiene acceso a estas muestras, ya que las intercepta para
redirigirlas hacia los sistemas de SLAM. Utilizaremos un concepto similar al de
la pre-integración de muestras de IMU explorado en la sección
@seq:basalt-preintegration con algunas ideas relacionadas con las ecuaciones
presentadas a partir de la [](#eq:imu-preintegration). Consideremos que no vamos
a querer interferir de ninguna manera con las estimaciones generadas por los
sistemas de SLAM, ya que no querremos distorsionar dichas poses. El proceso de
pre-integración correrá de forma completamente aislada de los sistemas. Más aún,
será un proceso mayormente efímero que solo tendrá consecuencias sobre puntos de
tiempos para los cuales el sistema de SLAM todavía no tenga una estimación
posterior. En particular, nos limitaremos a refinar las estimaciones de la
velocidad lineal y angular, dejando que las herramientas de predicción de Monado
que se basan en el último espacio del historial, computen la pose adecuada para
la timestamp requerida. Acumularemos promedios de las mediciones recientes para
reducir el impacto del ruido presente en las muestras de la IMU.

Tenemos entonces que el algoritmo utilizado finalmente es similar al pseudo
código que se presenta a continuación. Cabe aclarar que la función
`predict_pose(t)` es llamada cuando el usuario quiere una predicción a tiempo
`t`. Además las herramientas de Monado son representadas por `relation_history`
(el historial de relaciones) y `predict_from_space` (la función de predicción en
base a un espacio).

<!-- TODO@end: chequear que este algoritmo no se corte en dos páginas -->

```c++
struct xrt_space_relation predict_pose(timestamp t) {
   if (relation_history.is_empty()) return {0};

   struct xrt_space_relation r = relation_history.get_latest();
   timestamp rt = timestamp_of(r);

   if (predicción deshabilitada) return r;
   if (uso de IMU deshabilitado or t < rt) relation_history.predict(t);
   if (uso de giroscopio habilitado) {
      vec3 avg_gyro = gyro_average_between(rt, t);
      vec3 world_gyro = rotate_angular_velocity(r.orientation, avg_gyro);
      r.angular_velocity = world_gyro;
   }
   if (uso de acelerómetro habilitado) {
      vec3 avg_accel = accel_average_between(rt, t);
      vec3 world_accel = rotate_linear_acceleration(r.orientation, avg_accel);
      world_accel += gravity_vector;
      double dt = last_imu_timestamp - rt;
      r.linear_velocity += world_accel * dt;
   }

   return predict_from_space(r, t);
}
```

Es interesante notar la naturaleza modular del algoritmo representada por las
condiciones de los `if`, en donde distintos componentes que proveen información
a la predicción pueden deshabilitarse. Notar que la velocidad angular provista
por el giroscopio es local y necesita ser ajustada a coordenadas globales; esto
se realiza con la orientación estimada en `r`, la pose más reciente computada
por el sistema de SLAM. Similarmente el acelerómetro debe ser corregido, y a
este además se le suma una corrección con el vector de la gravedad^[El vector de
gravedad puede computarse dinámicamente con la IMU, detectando momentos en los
que el dispositivo está quieto y registrando el vector medido por el
acelerómetro.]. A diferencia del giroscopio, el acelerómetro solo nos puede
proveer información sobre los cambios de velocidad, y no sobre la velocidad
inicial; para esta usamos la dada por `r` que es computada con la diferencia de
las dos poses en `relation_history` más recientes.

Mostramos en la Figura @fig:prediction-with-imu un ejemplo simplificado del
algoritmo implementado utilizando esta idea de promediar muestras de odometría
de la IMU para predecir puntos de tiempo posteriores a `B` cuando `C` todavía no
pertenece al historial de espacios. En el ejemplo se muestra como iría
actualizándose el vector promediado (en verde) al integrar las tres muestras (en
azul) que ocurren entre $t=1$ y $t=2$. Además, se muestra como estos vectores
promedios se utilizan para extrapolar linealmente para los tiempos requeridos
por un usuario $t \in \{1,45; 1,75; 1.95\}$ (en anaranjado). Por simplicidad, el
ejemplo asume que tanto las muestras de odometría de la IMU a tiempos $t \in
\{1,3; 1,6; 1.9\}$ como las estimaciones `B` y `C` coinciden perfectamente con
la trayectoria real del dispositivo.

<!-- TODO@end: estaríá bueno que ambas figuras aparezcan en la misma página -->

![
Ejemplo de predicción para tiempos $t \in \{1,45; 1,75; 1.95\}$ utilizando la
idea de promediar muestras de la IMU posteriores a la pose más reciente del
historial (`B` en este caso, se considera que `C` no pertenece al historial
aún). Se asume que las poses estimadas por el sistema de SLAM y las muestras de
la IMU son perfectas por simplicidad.
](source/figures/prediction-with-imu.pdf "Predicción con promediado de muestras IMU"){#fig:prediction-with-imu width=100%}

Para contrastar esto con el caso en el que se ignoran las muestras de la IMU y
solo se utiliza el historial de poses, se muestra en la Figura
@fig:prediction-without-imu los errores de esta predicción para el mismo
escenario.

![
Ejemplo de predicción para tiempos $t \in \{1,45; 1,75; 1.95\}$ ignorando las
muestras de IMU y utilizando unicamente el historial de poses con `A` y `B` como
últimas muestras (esto es antes de que llegue `C`). De vuelta, asumimos que las
estimaciones y no contienen error por simplicidad.
](source/figures/prediction-without-imu.pdf "Predicción sin uso de muestras IMU"){#fig:prediction-without-imu width=100%}

Finalmente, cabe aclarar que la trayectoria presentada en estas figuras es
particularmente desafiante. Considerando que estos dispositivos XR están
usualmente sujetos a partes como la cabeza o las manos del usuario, es
improbable encontrar trayectorias demasiado abruptas entre los tiempos de
estimación de las poses de SLAM. Estos, al coincidir con la frecuencia de
muestreo de las cámaras, suelen ser menores a 50ms (p.ej. a 30 cuadros por
segundo, tenemos ~33ms entre pose y pose). Por otro lado, es usual tener una
mayor cantidad de muestras de IMU entre estimaciones y no solo las 3 que se
muestran en las figuras (p.ej. a 30 cuadros por segundo con la IMU a 250 hz,
tenemos unas ~8 muestras de IMU entre cada par de cuadros consecutivos), lo cual
mejora la precisión de la predicción aún más.

#### Filtrado de poses

Continuando con la descripción de la funcionalidad presente en la clase
adaptadora `TrackerSlam` y luego de haber presentado el método de predicción que
se emplea en Monado, veremos ahora la siguiente funcionalidad que `TrackerSlam`
implementa: el **filtrado** de poses.

También llamado _smoothing_, alisado o suavizado, el filtro de señales, curvas
o, en este caso poses, es una forma de minimizar o _filtrar_ el ruido presente
en alguna fuente de información y suavizar los cambios abruptos en las poses.
Lo que sucede en nuestro caso es que por la naturaleza del problema en cuestión
y por algunas de las decisiones tomadas, se pueden notar la presencia de micro
movimientos de alta frecuencia que existen en la trayectoria estimada. Estas
alteraciones no son más que ruido proveniente de distintos factores.

<!-- TODO@def: uso ATE,APE,AOE, RTE,RPE,ROE y loop closure -->

Por un lado, los sistemas de SLAM/VIO en el área no necesariamente priorizan el
caso de uso de XR y suelen estar mayormente interesados en aplicaciones de
robótica. En este campo, la “sensación” que produciría el tracking no es un
factor de importancia comparado a la precisión absoluta del mismo. En
particular, las métricas más utilizadas en estos trabajos son las que evalúan el
error absoluto de la trayectoria en su totalidad (ATE, APE, AOE). Es intuitivo
ver que estas métricas, a diferencias de sus versiones relativas (RTE, RPE,
ROE), incentivan correcciones abruptas en la trayectoria cuando los sistemas
determinan que su pose actual no es la mejor posible (p. ej. en momentos de loop
closure). Más aún, minimizar el ruido en la trayectoria no es uno de sus
objetivos, ya que la aplicación artificial de filtros que suavicen la
trayectoria podría tender a empeorar el puntaje obtenido en estos conjuntos de
datos. Todo esto hace que muchas veces las trayectorias computadas por los
sistemas en condiciones no óptimas tiendan a presentar una gran cantidad de
movimientos bruscos. Estos pueden resultar particularmente notables en sistemas
VR en dónde las pantallas ocupan todo el campo de visión del usuario;
movimientos de este tipo pueden fácilmente inducir cinetosis.

Por sobre esto, el método de predicción presentado en la sección anterior en la
Figura @fig:prediction-with-imu presenta problemas que no fueron tratados. En
particular, la predicción que realizamos está basada en una única pose del
sistema SLAM y las muestras nueva de la IMU, pero no comparte ningún otro estado
en común. Entonces podría esperarse que la diferencia entre las poses que se
fueron prediciendo con la nueva pose que el sistema estimará sea significativa.
Más aún, en la realidad el error acumulado por la IMU, a pesar de verse limitado
a un intervalo corto de unas decenas de milisegundos, es un término más que
afectaría esta diferencia. Todo esto puede verse en el error marcado en la
Figura @fig:prediction-offset-jump. Este tipo de desfasaje sería reintroducido
de forma repetitiva afectando las predicciones cada vez que una nueva pose es
estimada, causando así constantes micro saltos (ruido), especialmente en los
momentos en los que la pose estimada por SLAM y la pose predicha por nuestro
método difieran significativamente.

![
Desfasaje esperado entre el método de predicción por muestras promediadas y la
pose `C` estimada de SLAM cuando `C` aún no pertenece al historial de espacios.
Se muestra la incidencia de la acumulación de errores de la IMU. Este desfasaje
causará micro saltos que serían disruptivos en una experiencia de VR.
](source/figures/prediction-offset-jump.pdf "Predicción sin uso de muestras IMU"){#fig:prediction-offset-jump width=100%}

Es entonces por estas razones, que se implementaron tres métodos sencillos de
filtrado combinables para suavizar las trayectorias estimadas y que intentan
minimizar los problemas expuestos. Se deja como trabajo futuro el uso de filtros
más elaborados como los filtros Kalman [@welchSCAATIncrementalTracking1997, ap.
B]. Cabe aclarar que en general, el uso de filtros también presenta una
desventaja fundamental. Esta es, la introducción de latencia artificial al
sistema, ya que para poder suavizar este ruido, los filtros tienden a reducir
cambios abruptos en la trayectoria, incluso cuando estos sean realmente los
movimientos que el usuario realizó físicamente.

<!-- TODO@style: estaría bueno que los links aparecieran en monospace quizás? -->

Presentaremos tres filtros, con el más sofisticado basado en
[@casiezFilterSimpleSpeedbased2012]. Además, dicho trabajo cubre el resto de
filtros presentados, muestra gráficas comparativas, y es también una buena
lectura para contextualizar el uso de filtros para tracking de movimientos
humanos. Los filtros presentados aquí y en el trabajo mencionado pueden
visualizarse interactivamente en la siguiente aplicación web:
<https://cristal.univ-lille.fr/~casiez/1euro/InteractiveDemo/>.

El funcionamiento esquemático de un filtro es muy sencillo: es un contenedor de
**estado**, con un método de **actualización** que recibe un nuevo **dato** con
una **timestamp** posterior a las provistas hasta el momento; con esto, el
filtro computa el valor de la **señal filtrada** para una timestamp requerida.
En nuestro caso, esta timestamp coincidirá con la del dato de entrada. En
Monado, ubicaremos el filtro al final del pipeline de `TrackerSlam`, justo antes
de devolverle la pose a la aplicación OpenXR, es decir luego de haber pasado por
el procedimiento de predicción. Los filtros habilitados interceptan la pose con
sus métodos de actualización respectivos y devuelven en su lugar una nueva pose
filtrada con la misma timestamp. Los tres filtros se encuentran uno detrás del
otro y son combinables.

Expresado más formalmente, lo que tendremos es un conjunto de poses $X_0, ...,
X_k \in \R^7$ que ocurren a tiempos $t_0 < ... < t_k$ respectivamente. Para $i =
0, ..., k$ definimos $X_i = (p_i, q_i)$ con $p_i \in \R^3$ definido por los
primeros tres componentes de $X_i$ para representar la posición, mientras que
definimos el cuaternión $q_i$ para representar la orientación con coeficientes
dados por los últimos cuatro componentes. Tenemos además las versiones filtradas
de las poses anteriores $\hat{X}_0, ..., \hat{X}_{k - 1}$ y querremos ahora
computar la versión filtrada de la pose actual $\hat{X}_k$.

##### Media móvil

El primer filtro es una _media móvil_. El estado de este filtro consiste de un
historial de poses de los últimos $m$ segundos. El método de actualización
registra la pose de entrada y su timestamp en este historial interno. Para
computar la pose de salida en esa timestamp, se toma el promedio de las poses de
los últimos $w < m$ segundos (por defecto 66 ms). El parámetro $w$ es
configurable por el usuario.

<!-- TODO@def: uso cuaterniones -->

Cabe aclarar, que si bien la forma de calcular el promedio para las posiciones
$p_i$ debería resultar clara, promediar las orientaciones $q_i$ expresadas
mediante cuaterniones no es trivial. En este caso, nos aprovecharemos del hecho
de que $w$ suele ser pequeño y por ende contiene orientaciones que no cambian
significativamente. Esto nos permite utilizar el resultado expuesto en
[@gramkowAveragingRotations2001] que muestra que, para rotaciones de menos de 40
grados, calcular la media usual (y posteriormente normalizarla) es una muy buena
aproximación con un error de menos del 1%.

Tenemos entonces que el filtro queda definido por la siguiente ecuación.
<!-- $$ -->
\begin{align}
\hat{X}_k &= \frac{1}{|W|} \sum_{i \in W}{X_i}
\quad \text{con} \\
W &= \{ i : t_k - w \leq t_i \leq t_k \} \quad \text{(ventana del filtro)}
\end{align}
<!-- $$ -->

Notar que podemos definir el concepto de sumatoria componente a componente en
$\R^7$ gracias a la aproximación de los cuaterniones mencionada anteriormente.

##### Suavizado exponencial

Este filtro codifica en un único valor los datos históricos e integra nuevos
datos con una intensidad dada por un _factor de suavizado_ $\alpha \in [0, 1]$
configurable por el usuario (0.1 por defecto). En el caso de tener un único
escalar $x_k$ que filtrar, el suavizado exponencial queda definido de esta
forma:
<!-- $$ -->
\begin{align}
\hat{x}_0 &= x_0 \\
\hat{x}_k &= \alpha x_k + (1 - \alpha) \hat{x}_{k-1} \label{eq:exp-smoothing-scalar}
\end{align}
<!-- $$ -->

Reformulemos la [Ecuación](#eq:exp-smoothing-scalar) de la siguiente manera:
<!-- $$ -->
\begin{align}
\hat{x}_k &= \alpha x_k + (1 - \alpha) \hat{x}_{k-1} \\
&= \alpha x_k + \hat{x}_{k-1} - \alpha \hat{x}_{k-1} \\
&= \hat{x}_{k-1} + \alpha (x_k - \hat{x}_{k-1})
\end{align}
<!-- $$ -->

Esto nos deja ver el paso de actualización del filtro como una interpolación
(lineal) de $\hat{x}_{k-1}$ hacia $x_k$ con paso $\alpha$. Utilizaremos esta
idea para interpolar esféricamente la orientación de $\hat{X}_k$. Tenemos
entonces que el paso de actualización para este filtro queda definido como:
<!-- $$ -->
\begin{align}
\hat{X}_k &= (\hat{p}_k, \hat{q}_k) \\
\hat{p}_k &= lerp(\hat{p}_{k-1}, p_k, \alpha) = \hat{p}_{k-1} + \alpha (p_k - \hat{p}_{k-1}) \\
\hat{q}_k &= slerp(\hat{q}_{k-1}, q_k, \alpha) = \hat{q}_{k-1}
(\hat{q}_{k-1}^{-1} q_k)^\alpha
\end{align}
<!-- $$ -->

<!-- TODO@def: uso lerp y slerp de pecho ahí, uso inversa, composición y exponenciación
escalar de los quaternions -->

##### Filtro 1€

<!-- TODO@fix: la referencia a la seccion de suavizado exponencial no funciona.
Hay que cambiar el template y revisar todo de vuelta, no hay otra.
El template base es muy malo. -->

El filtro 1€ [@casiezFilterSimpleSpeedbased2012] se basa en el [Suavizado
exponencial](#sec:exponential-smoothing), pero utiliza un factor $\alpha$
dinámico que se adapta automáticamente con base a la tasa de cambio de la señal.
Reusamos también la idea de interpolar esféricamente para la orientación
presentada en el filtro anterior. El filtro queda definido para la posición
$p_k$ de la siguiente manera:
<!-- $$ -->
\begin{align}
\hat{p}_0 &= p_0 \\
\hat{p}_k &= lerp(\hat{p}_{k-1}, p_k, \alpha)
\end{align}
<!-- $$ -->

Con $\alpha$ que se adapta con la velocidad de la señal:
<!-- $$ -->
\begin{align}
\alpha &= \frac{1}{1 + \frac{\tau}{\Delta t_k}} \\
\Delta t_k &= t_k - t_{k-1} \\
\tau &= \frac{1}{2 \pi f_C}
\end{align}
<!-- $$ -->

A continuación, $f_C$ es la llamada _frecuencia de corte_[^fc-lowpass] y posee
un mínimo ajustable por el usuario $f_{C_{min}}$ y un parámetro de intensidad de
actualización $\beta$ también configurable[^fc-perception].
<!-- $$ -->
\begin{align}
f_C &= f_{C_{min}} + \beta | \hat{\dot{p}}_k |
\end{align}
<!-- $$ -->

[^fc-lowpass]: Algunos lectores reconocerán que el término “frecuencia de corte”
proviene de los filtros _low-pass_ y efectivamente, notarán que el filtro 1€ es
de este tipo con la particularidad de tener una frecuencia de corte que
dinámica.

[^fc-perception]: Frecuencias de corte bajas reducen el ruido de las poses a
costa de aumentar la latencia. La forma en la que $f_c$ es definida resulta en
valores altos (y por ende con baja latencia) cuando se presentan cambios
significativos en las poses, mientras que para movimientos más suaves se reduce
$f_c$ para a su vez disminuir el ruido.

La velocidad de la señal es a su vez ajustada con otro filtro de suavizado
exponencial con factor de suavizado fijo $f_{C_d}$, también configurable por el
usuario.
<!-- $$ -->
\begin{align}
\hat{\dot{p}}_0 &= 0 \\
\hat{\dot{p}}_k &= lerp(\hat{\dot{p}}_{k-1}, \dot{p}_k, f_{C_d})
\end{align}
<!-- $$ -->

Con velocidades instantáneas.
<!-- $$ -->
\begin{align}
\dot{p}_0 &= 0 \\
\dot{p}_k &= \frac{p_k - \hat{p}_{k-1}}{\Delta t_k}
\end{align}
<!-- $$ -->

La versión del filtro utilizada para la orientación $q_k$ es análoga a la
definición anterior con algunas aclaraciones:

- En lugar de $lerp$ se utiliza $slerp$.
- Sobrecargamos el operador de resta de cuaterniones de la siguiente forma: $q_a
  - q_b = q_b^{-1} q_a$.
- La norma de un cuaternión es equivalente a la norma euclídea en $\R^4$, es
  decir $|q| = \sqrt{q_x^2 + q_y^2 + q_z^2 + q_w^2}$.

### Recapitulando

Con la Figura @fig:slam-tracker-dataflow vista al principio de la sección en
mente, hemos visto que se ha implementado una clase adaptadora `TrackerSlam` en
Monado que funciona como punto central de comunicación con los sistemas de
SLAM/VIO integrados. Esta clase además implementa funcionalidades de predicción
y filtrado de poses que son configurables en runtime.

Los controladores de dispositivos físicos serán los encargados de instanciar y
comunicarse con esta clase. Veremos en la siguiente sección los dos
controladores (y por ende dispositivos) que necesitaron ser expandidos para este
trabajo y que constituyen una contribución importante al runtime.

## Controladores en Monado

<!-- TODO: Escribí este párrafo para la parte de TrackerSlam pero va mejor en la sección de Drivers

Para permitirle a los controladores utilizar el `TrackerSlam` como forma de ser
localizados, fue necesario extender algunos conceptos ya presentes en Monado
para el manejo de datos provenientes de hardware. En particular, para
dispositivos capaces de emitir video, Monado utiliza un grafo de fuentes y
sumideros de cuadros. Las fuentes son representadas por la clase _`xrt_fs`_ (o
_frame server_) y los sumideros por la clase _`xrt_frame_sink`_. Estas entidades
son interfaces muy sencillas que distintas clases en Monado implementan cuando
desean ser capaces de emitir o de recibir cuadros.

xrt_slam_sinks, xrt_imu_sink, xrt_fs.slam_stream_start

-->

<!-- TODO: Hablar en la seccion de drivers de frame management -->
<!-- TODO: Hablar en la seccion de drivers de pose correction -->
