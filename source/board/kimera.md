<!-- TODO@low: Fill all references/cites to example.com domain -->
<!-- TODO@low: Probably split how mention url references and citations -->

# Kimera

<!-- TODO@low: chequear que lo que digo de aprendizaje profundo es cierto  -->

Kimera [@kimera-paper], es una solución de SLAM con una licencia permisiva
(_BSD-2 [@bsd-2]_) desarrollada en C++ por el _SPARK Lab_ [@sparklab] del Massachusetts
Institute of Technology (MIT). Uno de los grandes atractivos que presenta esta
solución, además de su licencia, es su capacidad de reconstruir la geometría de
la escena en la que el agente se encuentra. Esta representación posee, en su
forma más detallada, cierto entendimiento semántico sobre los objetos presentes
en el espacio gracias a técnicas de aprendizaje profundo logrando etiquetarlos y
delimitar su geometría. Para este trabajo sin embargo nos enfocaremos
exclusivamente en los módulos relevantes a SLAM, en particular Kimera-VIO y
Kimera-RPGO.

Kimera-VIO es la solución de _odometría visual-inercial_ (_VIO_) que por sí sola no
intenta conseguir consistencia global en la trayectoria. Para esto último es el
módulo de Kimera-RPGO (_Robust Pose Graph Optimization_) que emplea
técnicas [@kimera-rpgo-pcm-paper] especializadas para contextos de múltiples
robots realizando SLAM de forma distribuida. Este módulo va a procurar mantener
la consistencia global tanto del mapa como de la trayectoria, realizando
apropiadamente acciones de _loop closure_, un proceso altamente ruidoso que
necesita buenas formas de rechazo de _outliers_ (valores atípicos).

Como muchas otras soluciones de SLAM, la arquitectura de Kimera es un
_pipeline_, en donde sus módulos presentan, en mayor o menor medida, un
almacenamiento de estado que se utiliza y actualiza en cada pasada (en cada
_spin_). A continuación se detallarán los distintos módulos y procedimientos que
son realizados en el pipeline de Kimera. Estos se estructuran de la
siguiente manera:

1. VIO frontend: procesa los datos directamente de los sensores.
   1. Muestras de la IMU: _Preintegración on-manifold_ [@on-manifold-paper]
      entre _keyframes_.
   2. Muestras de Cámaras:
      1. Detección de _esquinas Shi-Tomasi_ [@shi-tomasi-paper].
      2. _Rastreo_ (_tracking_) de estas esquinas a través del _rastreador
         Lukas-Kanade_ [@lukas-kanade-paper].
      3. Si se utiliza el pipeline con dos cámaras, es decir en modo _stereo_,
         es necesario encontrar las correspondencias entre ambas cámaras
         (_stereo matches_).
      4. _Verificación geométrica_ con distintas variantes de _RANSAC_
         [@ransac-paper].
         - Para _mono_ (una cámara): RANSAC de cinco puntos.
         - Para stereo (dós cámaras): RANSAC de tres puntos.
         - Adicionalmente, se pueden utilizar las muestras de rotación de la IMU
           para reducir la dimensionalidad del modelo estimado con RANSAC para
           mono y stereo a dos y uno respectivamente.
2. VIO backend: administra el _grafo de factores_.
   1. Actualización del grafo de factores

## Frontend

El _frontend_...

## Backend

El _backend_...

[@ransac-paper]: https://example.com
[@on-manifold-paper]: https://arxiv.org/pdf/1512.02363.pdf
[@sparklab]: http://web.mit.edu/sparklab/
[@kimera-paper]: https://arxiv.org/abs/1910.02490
[@bsd-2]: https://opensource.org/licenses/BSD-2-Clause
[@kimera-rpgo-pcm-paper]: http://robots.engin.umich.edu/publications/jmangelson-2018a.pdf
