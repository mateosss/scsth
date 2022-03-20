<!-- #### Optimización y marginalización -->

<!-- TODO@license: openvslam, avoid reading ORB-SLAM3 code -->
<!-- TODO@future: punto de mejora para basalt: usar dogleg minimization en vez de levenberg-marquardt. No se si vale la pena mencionarlo -->
<!-- TODO@question: question for basalt: why are they not using gtsam/g2o/ceres for the solvers? -->
<!-- TODO@future: parallelization/vectorization of gauss newton seems very easy, levenberg marquardt not so much -->

Finalmente, la optimización central o _bundle adjustment_ que ocurre en Basalt
se centra en minimizar con cuadrados mínimos una función de error que combina
residuales introducidos por las observaciones de las landmarks y la
preintegración de la IMU. En la versión original se aplicaba Gauss Newton, pero
luego de la actualización introducida en @demmelBasaltSquareRoot2021 se utiliza
Levenberg-Marquardt como algoritmo de minimización por defecto.

No nos adentraremos en los detalles de implementación de estos métodos por su
complejidad, pero basta con aclarar que una buena parte de esta se debe al el
cómputo explícito de los jacobianos para la linealización. En la práctica
existen formas de calcular estos jacobianos con técnicas de diferenciación
automática en tiempo de compilación como lo hace el optimizador
Ceres[^ceres-nlls] pero estas pueden incurrir en algunas pérdidas de
rendimiento[^ceres-analytical].

[^ceres-nlls]: <http://ceres-solver.org/nnls_solving.html>
[^ceres-analytical]: <http://ceres-solver.org/analytical_derivatives.html#when-should-you-use-analytical-derivatives>

Vale la pena aclarar, que la minimización de la función de error es equivalente
a realizar una estimación _máxima a posteriori (MAP)_
[@camposORBSLAM3AccurateOpenSource2021] que a su vez se desprende de ideas
similares a las encontradas en los estimadores de _máxima verosimilitud_[^map] pero
con probabilidades condicionales de por medio.

[^map]: <https://en.wikipedia.org/wiki/Maximum_a_posteriori_estimation>
