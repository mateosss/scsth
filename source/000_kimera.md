<!-- TODO: Uso de la palabra agente/casco/robot/HMD/headset/dispositivo -->

<!-- TODO:
- que esa acrónimo VIO?
- que es odometria visual-inercial?
- que es la licencia BSD-2
- que es una malla
- que es el frontend de slam
- que es el backend de slam
- que es loop closure
-->

# Kimera

[Kimera][kimera-paper], es una solución de SLAM con una licencia permisiva
([BSD-2]) desarrollada en C++ por el [SPARK Lab][sparklab] del Massachusetts
Institute of Technology (MIT). Uno de los grandes atractivos que presenta esta
solución, además de su licencia, es su capacidad de reconstruir la geometría de
la escena en la que el agente se encuentra. Esta representación posee, en su
forma más detallada, cierto entendimiento semántico sobre los objetos presentes
en el espacio gracias a técnicas de aprendizaje profundo logrando etiquetarlos y
delimitar su geometría. Para este trabajo sin embargo nos enfocaremos
exclusivamente en los módulos relevantes a SLAM, en particular Kimera-VIO y
Kimera-RPGO.

<!-- TODO: chequear que lo que digo de aprendizaje profundo es cierto  -->

Kimera-VIO es la solución de odometría visual-inercial que por sí sola no
intenta conseguir consistencia global en la trayectoria. Para esto último es el
módulo de Kimera-RPGO (_Robust Pose Graph Optimization_) que emplea
[técnicas][kimera-rpgo-pcm-paper] especializadas en un contexto de múltiples
robots realizando SLAM de forma distribuida. Este módulo va a procurar mantener
la consistencia global tanto del mapa como de la trayectoria, realizando
apropiadamente acciones de loop closure, un proceso altamente ruidoso que
necesita buenas formas de rechazo de valores atípicos (_outliers_).

## Frontend

## Backend

[sparklab]: http://web.mit.edu/sparklab/
[kimera-paper]: https://arxiv.org/abs/1910.02490
[bsd-2]: https://opensource.org/licenses/BSD-2-Clause
[kimera-rpgo-pcm-paper]: http://robots.engin.umich.edu/publications/jmangelson-2018a.pdf
