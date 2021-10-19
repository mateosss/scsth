<!--
- que es odometria visual-inercial?
- que es la licencia BSD-2
- que es una malla
-->

# Kimera-VIO

[Kimera-VIO][kimera-paper], o simplemente Kimera, es una solución de SLAM con
una licencia permisiva ([BSD-2]) desarrollada en C++ por el [SPARK
Lab][sparklab] del Massachusetts Institute of Technology (MIT).

Uno de los grandes atractivos que presenta esta solución, además de su licencia,
es su capacidad de reconstruir una malla de la escena en la que el agente se
encuentra. Esta representación además, posee cierto entendimiento semántico
sobre los objetos presentes en el espacio gracias a técnicas de aprendizaje
profundo. Sin embargo, para este trabajo no será necesario utilizar esta
característica.

[sparklab]: http://web.mit.edu/sparklab/
[kimera-paper]: https://arxiv.org/abs/1910.02490
[BSD-2]: https://opensource.org/licenses/BSD-2-Clause
