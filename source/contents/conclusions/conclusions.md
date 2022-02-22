# Conclusiones

## Resultados (TODO)

\begin{mdframed}[backgroundcolor=shadecolor]
Estuve con esto toda la semana pasada pero tuve un problema en como tomé las
mediciones y tengo que arreglarlo. En general como es algo bastante particular
no es que hay resultados de cosas “definitivas”, es más bien mostrar un poco
cualitativamente con números que tal andan las cosas.

Las medidas que me van a importar son de performance, de precisión de la
trayectoria absoluta y relativa (esta ultima no es comun que se mida pero es muy
importante en XR!).
Ya hice todos los datasets y los scripts para generar los gráficos, pero por un
error que cometí voy a necesitar hacer todas las corridas de vuelta (y eso ahora es un
proceso bastante manual desgraciadamente).

El resumen de los resultados creo que va a ser: Basalt debería dar buenos resultados en
performance y en precisión de movimientos relativos. Mientras que orb-slam3
debería dar mejores resultados en precisión absoluta de la trayectoria por que
hace full SLAM. Kimera-VIO está de adorno.

Como no tengo MoCaps para medir la trayectoria absoluta y comparar (salen unos 10k USD un setup basico \url{https://www.optitrack.com/systems/}),
planeo usar un software que se
llama COLMAP que se toma su tiempo (unas horas de procesamiento) para integrar todas las mediciones en lugar
de ser en tiempo real. Mi esperanza es que esa trayectoria debería ser bastante
razonable como groundtruth, al menos para dar una idea cualitativa de como anda
el sistema.

Si no también está el video \url{https://youtu.be/g1o2xADr5Fw}
\end{mdframed}

## Conclusiones y trabajo futuro

En este trabajo se estudiaron distintos sistemas de SLAM/VIO en el contexto de
localización en tiempo real para XR. Vimos algunos de los conceptos
fundamentales que estos utilizan como el algoritmo de Gauss Newton para resolver
problemas de optimización no lineal, de los cuales el área de visión por
computadora está plagado, y SLAM no es la excepción. También vimos las distintas
formas de representar transformaciones y rotaciones en dos y tres dimensiones:
ángulos euler, cuaterniones, ángulo axial, matrices de rotación y una mirada
práctica sobre los grupos de Lie $SO(n)$ y $SE(n)$ junto a sus álgebras de Lie
$\so(n)$ y $\se(n)$.

Posteriormente nos adentramos en la implementación de la capa de odometría
visual-inercial de Basalt. Esto permitió ver de primera mano los distintos tipos
de algoritmos que se reúnen en este tipo de sistemas. Se integró Kimera-VIO,
ORB-SLAM3 y Basalt a Monado, el runtime OpenXR de código libre. Para esto hizo
falta diseñar una interfaz eficiente que generaliza de forma razonable estos
sistemas. Se analizaron los problemas de implementación particulares a considerar
para XR como la predicción y filtrado de poses, o como lidiar con la
imperfección de los sensores de cámara e IMU. Se contribuyeron a Monado todas
estas mejoras, incluyendo la extensión de dos controladores de dispositivos que
ahora son capaces de aprovechar este tipo de tracking. Uno de ellos es una
plataforma VR de producción comercial que ahora puede ser utilizada por usuarios
entusiastas que deseen utilizar este tipo de hardware en GNU/Linux con un stack
de software completamente libre.

Este proyecto plantea las bases de infraestructura en Monado para este tipo de
sistemas, pero aún hay mucho por hacer y por mejorar para lograr tracking con
calidades similares a las que se encuentran en productos comerciales. Se plantea
como trabajo futuro:\newline

- Mejorar la experiencia de usuario para al utilizar el SLAM tracker en Monado.
  El trabajo realizado actualmente puede resultar un poco complejo de instalar y
  configurar para un usuario inexperto.

- Permitir el uso de múltiples implementaciones de SLAM/VIO de forma dinámica.
  Es decir, poder tener distintas implementaciones corriendo en simultáneo y
  localizando a distintos dispositivos.

- Hay espacio de mejora en el rendimiento de las implementaciones. En general,
  en este trabajo nos limitamos a hacer lo justo y necesario para que el
  tracking funcione a tiempos razonables y no retrase el pipeline de Monado. Más
  aún, parece existir poca cantidad de trabajos que apliquen unidades de cómputo
  masivamente paralelas, como lo son las GPU, al problema de localización
  visual-inercial. Creemos que existen posibles ganancias de eficiencia en esta
  línea de trabajo.

- Sería bueno extender Basalt para soportar algún tipo de mapeo global en tiempo
  real que permita tener trayectorias consistentes que no tiendan a moverse
  lentamente con el tiempo. Discusiones de esto referenciada en una nota al
  pie[^basalt-issue-vim].

- Sería bueno mejorar las formas de testeo y evaluación de sistemas SLAM en
  Monado, poder automatizarlas e integrarlas en los procesos de integración
  continua del proyecto. Esto permitiría el impacto que nuevos cambios traen al
  rendimiento y la precisión del sistema.

- Existen pocos conjuntos de datos para SLAM aptos para XR (p. ej. TUM-VI
  [@schubertBasaltTUMVI2018]), y ante la dificultad de producirlos, sería ideal
  aprovecharse de las herramientas fotorrealistas que son fácilmente accesibles
  en la actualidad para la generación de datos sintéticos.

- Existen métodos de predicción más eficientes que podrían adaptarse a Monado en
  lugar del método ad hoc desarrollado en este trabajo. En particular el mismo
  trabajde preintegración de muestras de IMU utilizado en Basalt
  [@forsterOnManifoldPreintegrationRealTime2017] puede ser un muy buen punto de
  partida para un método de predicción más preciso.

- Finalmente, muchos de los módulos que forman parte de estos sistemas son
  útiles de manera individual. La integración de estos en Monado podría
  beneficiar a distintos controladores que quieran hacer uso de algoritmia de
  visión por computadora específica en otros contextos.

[^basalt-issue-vim]: <https://gitlab.com/VladyslavUsenko/basalt/-/issues/69>
