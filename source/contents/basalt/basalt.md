<!-- TODO@def: VIO habla acerca de componentes: (patch tracking, landmark
representation, first-estimate Jacobians, marginalization
scheme) que podría ser interesante discutir -->
<!-- TODO@high@ref: Checkear que los 6 papers de basalt esten siendo citados -->
<!-- TODO: I think this paper has what I need to understand the code better http://www.roboticsproceedings.org/rss09/p37.pdf -->

# Implementación de un sistema

## Basalt

<!-- #include contents/basalt/preliminaries.md -->

### Implementación

A continuación describiremos la arquitectura e implementación de Basalt de una
manera más detallada. Estas secciones surgen directamente de la lectura del código
fuente del sistema e intentan proveer detalles más bien pragmáticos que se
encuentran en el mismo, pero que pueden quedar escondidos en las publicaciones de
más alto nivel que presentan estos sistemas. A su vez, se toman ciertas licencias literarias que deberían
ayudar al entendimiento y que no son posibles a la hora de escribir código.

Cómo vimos anteriormente, el funcionamiento de Basalt se divide en dos
etapas. La primera etapa de odometría visual-inercial (VIO), en el cual se
emplea un sistema de VIO que supera a sistemas equivalentes de vanguardia.
La segunda etapa de mapeo visual-inercial (VIM), toma keyframes
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

<!-- #include contents/basalt/opticalflow.md -->

#### Procesamiento de muestras

<!-- #include contents/basalt/measurements.md -->

#### Optimización y marginalización (TODO)

<!-- #include contents/basalt/optimization.md -->
