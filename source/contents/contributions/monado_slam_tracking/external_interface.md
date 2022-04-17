<!-- ### Interfaz externa -->
<!-- TODO@low@automation: It would be awesome to be able to use just h1 headings
(H1) and then be the parent that appends # to all headings -->

<!-- TODO: mencionar que ORB-SLAM3 está en un fork separado de monado por GPL -->

Desde un principio se entendió que se necesitaría utilizar sistemas ya
desarrollados como punto de partida. Estos sistemas son complejos y suelen
utilizar conceptos teóricos de significativa profundidad, por lo que su
creación suele estar limitado a grupos de investigación expertos que toman gran
tiempo de desarrollo. Los tres sistemas estudiados por ejemplo,
promedian las 25.000 líneas de código (o 25 _KLOC_) cada uno.

Ahora bien, en muchos casos, haber intentado integrar el código del sistema
directamente dentro de un componente de Monado no era una opción. Dejando de
lado las dificultades técnicas, los problemas de compatibilidad de licencia
fueron de particular interés. La gran mayoría de sistemas SLAM producidos en la
academia son liberados bajo licencias abiertas “virales” como _GPL_ [@GNUGeneralPublic] que
obligan a desarrolladores que utilizan código del sistema a liberar y licenciar
su código de la misma manera. Esto contrasta con la licencia abierta y
permisiva de Monado, la _BSL-1.0_ [@BoostSoftwareLicensea], que no impone restricciones sobre como los
usuarios deben licenciar su código.

Estas fueron algunas razones para intentar desacoplar el sistema a utilizar lo
más que se pueda de Monado. Además, considerando la naturaleza experimental de
este trabajo, la posibilidad de que más de un sistema necesitase ser
integrado era razonable.

Monado está desarrollado principalmente en C, pero gran parte de su
código de tracking está implementado en C++ al igual que todos los sistemas de
SLAM contemplados. Adicionalmente tanto Monado como estos sistemas suelen hacer
un uso extensivo de la biblioteca _OpenCV_, y en particular su clase contenedora
de imágenes y matrices `cv::Mat`. Es por esto que se terminó optando por el uso de
un archivo _header_ C++, en el cual se declara la clase `slam_tracker`[^slam-tracker-file] que será
utilizada por Monado como punto de comunicación con sistemas de SLAM arbitrarios
y se utilizan `cv::Mat` como contenedor de imágenes. Luego de varias iteraciones de diseño,
la clase `slam_tracker` tiene una interfaz que, quitando detalles de tipos de
C++, se puede resumir en algo como lo que se muestra en el \Cref{lst:slam-tracker-def}.

[^slam-tracker-file]: <https://gitlab.freedesktop.org/monado/monado/-/blob/2d9c1b2b11373f707b990e5b8a28b15bc1454b83/src/external/slam_tracker/slam_tracker.hpp#L95-167>

<!-- TODO: linkear la clase slam_tracker en gitlab? -->

<!-- TODO@high@end: hacer que esto esté sin cortes en su propia página o algo, lo mismo para todos los fragments -->
\clearpage
``` {#lst:slam-tracker-def .cpp caption="Interfaz a implementar por sistemas de SLAM"}
class slam_tracker {
public:
  // (1) Constructor y funciones de inicio/fin
  slam_tracker(string config_file);
  void start();
  void stop();

  // (2) Métodos principales de la interfaz
  void push_imu_sample(timestamp t, vec3 accelerometer, vec3 gyroscope);
  void push_frame(timestamp t, cv::Mat frame, bool is_left);
  bool try_dequeue_pose(timestamp &t, vec3 &position, quat &rotation);

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
ver \figref{fig:slam-tracker-hpp}.

<!-- TODO@fig: La parte de basalt está mal, no hay hilo consumidor de muestras,
el hilo ese estaría en las "Partes Internas de Basalt". Otros problemas es que
no se relaciona las colas dibujadas con nada, ni con Monado ni con la copia de slam_tracker.hpp -->

\fig{fig:slam-tracker-hpp}{source/figures/slam-tracker-hpp.pdf}{Interfaz de SLAM tracker}{%
Interacción entre Monado y sistemas SLAM mediante la interfaz en C++.
Enlaces a estos forks pueden verse en las \Cref{app:kimera-fork,app:orbslam3-fork,app:basalt-fork}.
}

La versión actual de esta clase es el
resultado de varias iteraciones y generaliza adecuadamente los tres sistemas
en uso. Algunas consideraciones de los puntos marcados en el código:

1. El parámetro `config_file` del constructor es necesario, ya que todos los sistemas
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

3. Algo que surge del desarrollo de una interfaz a un tipo de sistemas que aún se desconocen,
   es que va a haber varios cambios en la misma durante su creación. Si además
   esta interfaz es compartida por múltiples sistemas y repositorios, mantener
   todas las versiones sincronizadas se vuelve insostenible. Una
   forma de aliviar este problema fue la implementación de características
   dinámicas en la \Cref{app:slamtracker-dynamic-features}. En ellas, Monado evalúa si el sistema implementa alguna
   característica específica en tiempo de ejecución antes de utilizarla.
   Uno de sus usos, fue la automatización del envío de datos de calibración sin pasar
   por el archivo `config_file`. La forma de añadir nuevas características de
   este tipo se debe reservar un entero `feature_id` que la identifique en una
   nueva versión del header `slam_tracker` de Monado y del fork que la va a
   implementar. En Monado tenemos cuidado de
   solo utilizarla si el sistema la reporta como disponible en tiempo de
   ejecución, ya que otros forks podrían no implementarla. De esta forma
   permitimos la extensión de sistemas específicos sin tener que adaptar la
   versión de la interfaz en todos ellos.

4. El miembro `impl` es una forma de ligar la definición compacta de
   `slam_tracker` con una clase que implementa el estado y métodos privados
   necesarios para proveer la funcionalidad requerida. Este patrón de desarrollo
   es usualmente conocido como _pointer to implementation_ (o _PIMPL_), a `impl`
   se lo denomina un _puntero opaco_ [@lakosLargeScaleSoftwareDesign1996].

<!-- #define MN_ILLIXR_INTERFACE %\
ILLIXR \autocite{HuzaifaDesai2020} es un proyecto de XR de código libre desarrollado
por la Universidad de Illinois, que también formó recientemente el Consorcio ILLIXR
para intentar mejorar el ecosistema de código libre para XR. Ha habido discusiones entre ILLIXR y Monado
para plantear una interfaz a sistemas de SLAM que le sirva a ambos proyectos y que quizás en un
futuro pueda transformarse en un estándar que los sistemas implementen por elección propia.
Para esta nueva interfaz, se tomarán ideas basadas en la experiencia obtenida desarrollando el header \mono{slam_tracker}.
-->

\clearpage

Esta interfaz no es perfecta: no contempla magnetómetros, asume una
configuración de a lo sumo dos cámaras, asume que el sistema utiliza OpenCV y es
difícil de extender con cambios no contemplados por el concepto de
características dinámicas. A pesar de estos problemas, ha sido suficientemente
buena para generalizar todos los sistemas propuestos y correrlos con una
performance adecuada \marginnote{MN_ILLIXR_INTERFACE}.

\FloatBarrier
