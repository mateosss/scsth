<!-- #### Optimización y marginalización -->

<!-- TODO@high: escribir -->
<!-- TODO@license: openvslam, avoid reading ORB-SLAM3 code -->
<!-- TODO@future: punto de mejora para basalt: usar dogleg minimization en vez de levenberg-marquardt. No se si vale la pena mencionarlo -->
<!-- TODO@question: question for basalt: why are they not using gtsam/g2o/ceres for the solvers? -->
<!-- TODO@future: parallelization/vectorization of gauss newton seems very easy, levenberg marquardt not so much -->

\begin{mdframed}[backgroundcolor=shadecolor]
TODO: Esta última parte es un poco
compleja y me ha estado costando terminar de cerrar como explicarla. Basicamente
lo que se hace es plantear la función de error a optimizar $E(x)$ que combina un
montón de términos de error. Y se le quiere aplicar gauss newton. El problema es
que al haber tantos términos que optimizar, el cálculo de los jacobianos se hace muy rebuscado
y se arma un callstack de funciones muy profundo que lo único que hace es
computar valores parciales de estos jacobianos.\\
\\
Por otro lado la idea de
“marginalización“ es importante por que habla de uno de los términos que aparece
en $E(x)$ y que es un poco la novedad que trae Basalt, ellos logran eliminar
(marginalizar) los efectos de muchas mediciones en unas pocas distribuciones
aproximadas.\\
\\
Para sumar a la complejidad de esta sección, está, un poco escondido en la
implementación, el concepto de “grafo de factores“ para armar antes de la
optimización. No lo he profundizado lo suficiente como para explicarlo pero a
grandes rasgos, es un grafo en donde se tienen nodos que son variables
aleatorias mientras que los lados son las mediciones que uno toma (los factores). Por ejemplo
un nodo puede ser la variable que representa la posición de una landmark que
quiero estimar,
mientras que un factor puede ser el vector distancia que el agente trianguló con
sus cámaras hacia esa landmark (también tiene ruido).\\
La idea de estos grafos es hacer una estimación
“máxima a posteriori“ (MAP) con todo lo que tienen adentro. MAP es un concepto
muy parecido al de estimación de máxima verosimilitud. Básicamente lo que se
tiene es que minimizar la función de error $E(x)$ lo que está haciendo es
acomodando los resultados de las variables de interés para que sean los de mayor
probabilidad (“de mayor verosimilitud“) dadas las restricciones impuestas por las mediciones tomadas (los
factores del grafo).
\end{mdframed}
