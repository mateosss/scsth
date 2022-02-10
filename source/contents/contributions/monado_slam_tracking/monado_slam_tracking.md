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
se muestra en la \figref{fig:monado-arch}. Una aplicación que hace uso de OpenXR
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

<!-- TODO@high@fig: Tiene que estar en español y agregar "Filtrado" arriba de "Prediction" -->
<!-- TODO@fig: Podría usar los nombres `TrackerSlam` y `slam_tracker` me
parece por que los referencio bastante -->
\fig{fig:monado-arch}{source/figures/monado-arch.pdf}{Arquitectura de Monado}{%
Arquitectura de Monado.
}

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

<!-- TODO@high@nico: Lo que le digo "slam tracker implementation" nico pensó que
debería ser una "interface", implementación/interfaz/adaptador son bastante
ambiguos así que deberí revisar que los uso de forma consistente -->
<!-- TODO@high@fig: Del TODO de arriba, viene que tengo que modificar fig:slam-tracker-dataflow -->

La implementación de un pipeline en Monado que permita la comunicación entre
dispositivos, sistemas de SLAM y la aplicación OpenXR requirió desarrollar la
infraestructura y herramientas necesarias dentro de Monado. El pipeline en
cuestión está esquematizado en la \figref{fig:slam-tracker-dataflow}. Este,
requiere un gran nivel de modularidad, ya que sus componentes fundamentales
necesitan poder ser intercambiables: dispositivos, aplicaciones y el sistema que
provee el SLAM en sí. El resto de esta subsección está dedicada a explicar la
infraestructura y los distintos componentes que se necesitaron implementar y
adaptar para obtener un pipeline de SLAM modular corriendo en Monado como se
intenta mostrar en la \figref{fig:slam-tracker-dataflow}.

<!-- TODO@high@fig: Agregar a esta figura la caja del filtrado de poses -->
<!-- TODO@high@fig: Hacer versión final -->

\fig{fig:slam-tracker-dataflow}{source/figures/slam-tracker-dataflow.pdf}{Flujo de datos de la implementación}{%
Diagrama esquemático de como ocurre el flujo de los datos desde que se generan
las muestras en los dispositivos XR hasta que la aplicación OpenXR obtiene una
pose utilizable. Notar que las flechas esconden múltiples hilos de ejecución,
colas de procesamiento, y desfasajes temporales con los que hay que lidiar en la
implementación.
}

\FloatBarrier

### Interfaz externa

<!-- #include contents/contributions/monado_slam_tracking/external_interface.md -->

### Implementaciones de la interfaz

<!-- #include contents/contributions/monado_slam_tracking/interface_implementations.md -->

### Clase adaptadora

Para interactuar con la interfaz que detallamos en la sección anterior, se
implementa en Monado una clase adaptadora en el módulo auxiliar de tracking
(recordar \figref{fig:monado-arch}) y que sirve de nexo entre los
controladores de dispositivos de hardware y la interfaz `slam_tracker`. Este
adaptador recibe el nombre, un poco confuso, de `TrackerSlam` siguiendo las
convenciones de Monado para con los trackers ya existentes.

El funcionamiento de `TrackerSlam` es sencillo, los controladores que quieran
ser localizados por SLAM y puedan proveer imágenes y muestras de IMU deben
instanciar este adaptador e inicializarlo. Por detrás, esto simplemente llama a
los métodos adecuados de la interfaz `slam_tracker` con el sistema externo.
Ahora bien, se aprovecha esta clase adaptadora[^adapter-class-remark] para
proveer dos funcionalidades fundamentales que escapan al alcance de los sistemas
de SLAM/VIO y serán explicados a continuación: **predicción** y **filtrado** de
poses.

<!-- TODO@high: Hago las "Notas" así? hay una mejor manera? quizás a un
costado de la página o con un recuadro tcolorbox como vi en un video. EDIT: USE MARGINNOTE -->

[^adapter-class-remark]: Es debatible si el añadido de estas funcionalidades
haría que `TrackerSlam` deje de ser considerada una clase adaptadora, ya que
como veremos, ambas pueden ser deshabilitadas en tiempo de ejecución._

#### Predicción de poses

<!-- #include contents/contributions/monado_slam_tracking/prediction.md -->

#### Filtrado de poses

<!-- #include contents/contributions/monado_slam_tracking/filtering.md -->

### Recapitulando

Con la \figref{fig:slam-tracker-dataflow} vista al principio de la sección en
mente, hemos visto que se ha implementado una clase adaptadora `TrackerSlam` en
Monado que funciona como punto central de comunicación con los sistemas de
SLAM/VIO integrados. Esta clase además implementa funcionalidades de predicción
y filtrado de poses que son configurables en runtime.

Los controladores de dispositivos físicos serán los encargados de instanciar y
comunicarse con esta clase. Veremos en la siguiente sección los dos
controladores (y por ende dispositivos) que necesitaron ser expandidos para este
trabajo y que constituyen una contribución importante al runtime.
