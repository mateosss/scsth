<!-- Posibles valores de MODE: DRAFT, RELEASE -->


# Resumen (TODO) {.unnumbered .unlisted}



\pagenumbering{roman}
\setcounter{page}{1}

# Agradecimientos (TODO) {.unnumbered .unlisted}



\newpage

\pagenumbering{gobble}

\tableofcontents

\newpage

\listoffigures

\newpage

\listoftables

\newpage

# Abbreviations {.unnumbered .unlisted}

\begin{tabbing}
\textbf{API}~~~~~~~~~~~~ \= \textbf{A}pplication \textbf{P}rogramming \textbf{I}nterface \\
\textbf{JSON} \> \textbf{J}ava\textbf{S}cript \textbf{O}bject \textbf{N}otation \\
\end{tabbing}

\newpage

\setcounter{page}{1}
\pagenumbering{arabic}
\doublespacing
\setlength{\parindent}{0.5in}

<!-- TODO: list of listings, list of algorithms, list of theorems/defs/obs? -->

\hypersetup{linkcolor=cyan}


# Introducción (TODO)






<!-- TODO@ref:
Books used:
nocedalNumericalOptimization2006a: solucion mas de calculo, con tema de funciones convexas
IntroductionAppliedLinear: lo que use mas que nada
linear algebra done right?: aca ver si esta el teorema que uso sin demo si lo puedo sacar de ahí
-->

<!-- TODO@def: outlier -->
<!-- TODO@def: debería aclarar de alguna forma que los vectores son verticales -->

<!-- TODO@def: definir una función afín cuando explique SE(2)/SE(3) estaría bueno -->

# Optimización por cuadrados mínimos

Como se verá más adelante, muchos de los problemas fundamentales de SLAM son
problemas de optimización. Querremos minimizar una _función de error_ o
_energía_ no-lineal que integre las múltiples mediciones que contienen
información conflictiva, ruido, outliers, y demás problemáticas propias de la
toma de datos mediante sensores físicos. Se utiliza como algoritmo principal
para la optimización de estos sistemas el algoritmo de Gauss-Newton, y es el que
explicaremos en esta sección. Cabe aclarar que existen algoritmos ligeramente
más sofisticados como _Levenberg-Marquardt_ o el _método dogleg_ que pueden
aplicarse; no nos explayaremos en ellos en este trabajo, pero serán mencionados
cuando sea pertinente.

## Cuadrados mínimos lineales

Comencemos con el caso lineal que será necesario para luego aproximar el
no-lineal.

Querremos encontrar algún punto $x \in \R^n$ que cumpla una serie de $m$
restricciones **lineales** $f_i(x) = b_i$ con $f_i \in \R^n \rightarrow \R$
combinación lineal de los componentes $x$; $\ b \in \R^m$ y con $i = 1, ..., m$.
Además definimos $f(x) = [f_1(x) \dots f_m(x)]^T$ y al ser $f_i$ combinaciones
lineales de $x$, tenemos que existe una transformación lineal $A \in \R^{m
\times n}$ tal que $f(x) = Ax$. De esta forma podemos replantear nuestras
ecuaciones como el sistema $Ax = b$.

Será usual que $m > n$ y que $A$ tenga columnas linealmente independientes así
que solo consideraremos este caso. Al tener más ecuaciones que incógnitas
tenemos un sistema _sobre-determinado_ en el cual, para valores usuales de $b$,
no tendremos solución. Buscaremos entonces el $x$ que “mejor” cumpla con estas
restricciones en algún sentido de la palabra. Utilizaremos el criterio de
minimizar los _residuales_ $r_i(x) = f_i(x) - b_i$ y definimos al vector
residual como $r(x) = [r_1(x) \dots r_m(x)]^T$. Querremos encontrar un $x$ que
minimice la siguiente función de _error_ o _energía_ $E(x)$ basada en los
residuales.
<!-- $$ -->
\begin{align}
E(x) = \sum_{i=1}^m{r_i(x) ^ 2} = \| r(x) \| ^ 2
\end{align}
<!-- $$ -->

Notar que la definición de $E(x)$ coincide con la de la _norma euclídea_ al
cuadrado de $r(x)$. Encontrar $x$ que minimice $E(x)$ con residuales lineales
es el _problema de los cuadrados mínimos lineales_; a $x$ le decimos _solución_
de tal problema. Notar que $r_i = (Ax - b)_i$, o sea el componente $i$ del
vector $Ax - b \in \R^m$, y por ende $r(x) = Ax - b$.
<!-- $$ -->
\begin{align}
E(x) = \sum_{i=1}^m{(Ax - b)_i^2} = \| Ax - b \| ^ 2
\end{align}
<!-- $$ -->

Lo que queremos minimizar es entonces equivalente a la norma cuadrada del vector
residual $Ax - b$. Introduciremos a continuación una serie de conceptos y
teoremas necesarios para poder presentar una forma sucinta de minimizar esta
norma.

<!-- TODO@ref: citar linear algebra done right (va encontrar primero el teorema ahí) -->

Aceptaremos el siguiente teorema sin demostración.

Theorem thm:li1inv2nots3
: Son equivalentes:
\begin{enumerate}
  \item Las columnas de $A$ son linealmente independientes.
  \item $A$ es invertible.
  \item $Ax = 0 \Leftrightarrow x = 0$.
\end{enumerate}

Otras definiciones y resultados que necesitaremos a continuación.

Definition def:grammat
: La matriz de Gram de $A$ es $A^T A \in \R^{n \times n}$.

Theorem thm:aligraminv
: La matriz de Gram de $A$ es invertible si y solo si $A$ tiene columnas
linealmente independientes.

<!-- TODO@def: Uso (AB)^T = B^T A^T -->
<!-- TODO@def: Uso |A|^2 = A^T A -->

Proof
: Como $A$ tiene columnas linealmente independientes, por
[](#thm:li1inv2nots3) (3) tenemos que $x = 0 \Leftrightarrow Ax = 0$, nos basta
con ver que $Ax = 0 \Leftrightarrow A^T A x = 0$.
\begin{itemize}
  \item $\Rightarrow)$ Si $Ax = 0$ entonces $A^T A x = A^T (A x) = A^T 0 = 0$
  \item $\Leftarrow)$ Si $A^T A x = 0$ entonces $0 = x^T A^T A x = (x^T A^T) A x =
    (A x)^T (Ax) = \| Ax \|^2 = 0$ y esta norma es $0$ si y solo si $Ax = 0$
\end{itemize}

Definition def:pseudoinverse
: Sea $A$ con columnas linealmente independientes. La matriz pseudo-inversa de
$A$ es $A^{\dagger} = (A^T A)^{-1} A^T$

Notar que $(A^T A)^{-1}$ existe por [](#thm:aligraminv). Finalmente, la
siguiente observación:

Remark rmk:sqnormofsum
: Sean $a, b \in \R^k$ para algún $k \in \N$, tenemos que $\| a + b \| ^ 2 =
\|a\|^2 + \|b\|^2 + 2 a^T b$.

Proof
: Desarrollemos:
<!-- $$ -->
\begin{align}
\| a + b \| ^ 2 &= (a_1 + b_1)^2 + \dots + (a_k + b_k)^2 \\
&= (a_1^2 + b_1^2 + 2 a_1 b_1) + ... + (a_k^2 + b_k^2 + 2 a_k b_k) \\
&= \| a \| ^2 + \| b \|^2 + 2 \langle a, b \rangle \\
&= \| a \| ^2 + \| b \|^2 + 2 a^T b
\end{align}
<!-- $$ -->

Con estas herramientas, estamos en posición de presentar la solución directa al
problema de los cuadrados mínimos lineales.

Theorem thm:linleastsquaresol
: $\hat{x} = A^{\dagger} b$ es **la** solución del problema de los cuadrados mínimos
lineales. Es decir $\forall x \in \R^n: E(\hat{x}) = \| A\hat{x} - b \| ^ 2
\leq \| Ax - b \| ^ 2 = E(x)$.

Proof
: Tenemos primero que
<!-- $$ -->
\begin{align}
  & \hat{x} = A^\dagger b \\
  &\Leftrightarrow \hat{x} = (A^T A)^{-1} A^T b \\
  &\Leftrightarrow A^T A \hat{x} = A^T b \\
  &\Leftrightarrow A^T (A \hat{x} - b) = 0 \label{eq:ataxmbis0}
\end{align}
<!-- $$ -->
Las últimas dos ecuaciones reciben nombres particulares [^normalequations]
[^orthogonalityprinciple]. Veamos ahora para un $x \in \R^n$ cualquiera.
<!-- $$ -->
\begin{align}
  \| Ax - b \|^2 &= \| (Ax - A\hat{x}) + (A\hat{x} - b) \|^2 \\
  \text{(\cref{rmk:sqnormofsum})}\quad
  &= \| A(x - \hat{x}) \|^2 +  \| A\hat{x} - b \|^2 + 2 (A(x - \hat{x}))^T
  (A\hat{x} - b) \\
  &= \| A(x - \hat{x}) \|^2 +  \| A\hat{x} - b \|^2 + 2 (x - \hat{x})^T A^T
  (A\hat{x} - b) \\
  \text{(\cref{eq:ataxmbis0})}\quad
  &= \| A(x - \hat{x}) \|^2 +  \| A\hat{x} - b \|^2 \\
  &\therefore \|Ax-b\|^2 \geq \|A\hat{x}-b\|^2
\end{align}
<!-- $$ -->
Más aún, esta solución es única ya que la igualdad en la última ecuación solo se
da si $\|A(x-\hat{x})\|^2 = 0$, y como $A$ es no-singular, esto solo pasa
cuando $x=\hat{x}$.

[^normalequations]: La expresión $A^T A x = A^T b$ suele ser referida como
_ecuaciones normales_. La derivación de la solución de cuadrados mínimos
presentada en este trabajo no es la única. De hecho, es común encarar el
problema mediante cálculo diferencial. En ese contexto, las ecuaciones normales
surgen naturalmente a la hora de optimizar $E(x)$ igualando su gradiente a $0$.
Para una demostración mediante cálculo referirse a
[@nocedalNumericalOptimization2006, cap. 10].

[^orthogonalityprinciple]: La expresión $A^T (A\hat{x} - b) = 0$ es interesante,
ya que muestra que las columnas de $A$ son ortogonales al residual óptimo
$A\hat{x} - b$ al ser su producto interno $0$. Esto suele llamarse el _principio
de ortogonalidad_.

## Cuadrados mínimos no lineales

Generalizaremos el problema anterior para que también considere funciones no
lineales. Reutilizaremos la notación introducida en la sección anterior.

En este caso permitimos ahora que las $f_i$ sean no lineales, aunque requerimos
que continúen siendo diferenciables. Además, ignoraremos el vector $b$ haciendo
que $f(x) = r(x)$. Es decir querremos que $f(x) = 0$ en lugar de $f(x) = b$. En
el caso de necesitar la segunda restricción, podemos construir nuevas
funciones $\tilde{f}_i(x) = f_i(x) - b_i$ y utilizar estas en su lugar. Nuestra
función de error es entonces:
<!-- $$ -->
\begin{align}
E(x) = \sum_{i=1}^m{f_i(x)^2} = \| f(x) \| ^ 2
\end{align}
<!-- $$ -->

<!-- TODO@def: creo que estoy "introduciendo" con _cursivas_ el término
funcion afín, funciones afines, etc en una banda de lugares -->

Encontrar $x$ solución que minimice tal error es el _problema de los cuadrados
mínimos no lineales_. En este caso, al no ser necesario que los residuales sean
_funciones afines_ (lineales más un escalar), no podemos dar una matriz $A$ y
utilizar ideas como las de la pseudo inversa $A^{\dagger}$. Más aún, en el caso
lineal, si bien no lo mostramos, se cumple que la solución no solo es única,
sino que es el único punto con gradiente $\nabla f(x) = 0$, es decir, el único
punto optimizador, es un mínimo global. Para una demostración de esto, se
utilizan argumentos de _convexidad_ sobre $E(x)$; referirse a
[@nocedalNumericalOptimization2006, cap. 10]. En el caso no lineal sin embargo,
no tenemos ninguna de estas garantías, pueden existir infinitos máximos y
mínimos globales, locales y cualquier combinación de estos.

Lo que se hace entonces es utilizar algoritmos heurísticos; en nuestro caso el
algoritmo de _Gauss-Newton_ que busca un mínimo de forma iterativa comenzando
desde un punto que, si se encuentra lo suficientemente cerca a la solución,
convergerá a ella. Como veremos más adelante, este requerimiento de proveer un
punto inicial adecuado es muy razonable en sistemas de SLAM/VIO, ya que
usualmente contaremos con dicha información.

Gauss-Newton genera la secuencia de puntos $x^{(1)},\ x^{(2)}, ...$ al ser un
algoritmo iterativo. Es posible juzgar cada iteración $k$ evaluando $E(x^{(k)})
= \| f(x^{(k)})\|^2$. Como es usual existen varios criterios de terminación
apropiados: se alcanza un cierto número fijo de iteraciones $k^{max}$, el error
del último iterando $E(x^{(k)})$ es suficientemente cercano a $0$, o las últimas
dos iteraciones tienen un error muy similar a los fines prácticos $E(x^{(k)})
\sim E(x^{(k + 1)})$.

En cada iteración $k$ el algoritmo cuenta con dos etapas. La etapa de
**linealización** aproxima a $f(x)$ linealmente con su expansión de Taylor de
primer orden centrada en el iterando actual $x^{(k)}$; llamaremos a esta
aproximación $f^{(k)}(x)$. En la etapa de **actualización** utilizamos el hecho
de que $f^{(k)}(x)$ es una función afín para encontrar una solución al problema
de cuadrados mínimos _lineales_ sobre ella. Esta solución será el valor de
nuestro próximo iterando $x^{(k+1)}$ y, por ende, la estimación que damos como
solución del problema no-lineal. Es decir, como sabemos que $x^{(k+1)}$ minimiza
a $f^{(k)}$, esperaríamos que sea una buena aproximación al mínimo de $f$
sabiendo que comenzamos el algoritmo cerca de su mínimo.

**Linealización**. Definimos $f^{(k)}(x)$ como la expansión de Taylor de $f(x)$
centrada en $x^{(k)}$. Es decir:
<!-- $$ -->
\begin{align}
f^{(k)}(x) = f(x^{(k)}) + A(x^{(k)}) (x - x^{(k)})
\end{align}
<!-- $$ -->

con $A: \R^n \rightarrow \R^{m \times n}$ la matriz jacobiana de $f$.
<!-- $$ -->
\begin{align}
A = \begin{bmatrix}
  \frac{\partial f_1}{\partial x_1} & \dots & \frac{\partial f_1}{\partial x_n} \\
  \vdots & \ddots & \vdots \\
  \frac{\partial f_m}{\partial x_1} & \dots & \frac{\partial f_m}{\partial x_n}
\end{bmatrix}
\end{align}
<!-- $$ -->

Notar que $f^{(k)}$ es afín; una transformación lineal $A(x^{(k)})$ aplicada
sobre $x$, más un vector. Reacomodemos los términos para dejarlo explícito
e introduzcamos la notación $A_k = A(x^{(k)})$.
<!-- $$ -->
\begin{align}
f^{(k)}(x) = f(x^{(k)}) + A_k (x - x^{(k)}) \\
f^{(k)}(x) = A_k x - (A_k x^{(k)} - f(x^{(k)}))
\end{align}
<!-- $$ -->

**Actualización**. Teniendo en mente que queremos encontrar el mínimo de $\|
f(x) \| ^ 2$, lo aproximamos con el mínimo (y próximo iterando) $x^{(k+1 )}$ de
$\| f^{(k)}(x) \| ^ 2$ pero como $f^{(k)}$ es afín, esto se reduce a buscar la
solución del problema de cuadrados mínimos _lineales_. Sabemos por
[Teorema](#thm:linleastsquaresol) la solución exacta para este caso en base a la
matriz pseudo-inversa $A_k^{\dagger} = (A_k^T A_k)^{-1} A_k^T$.
<!-- $$ -->
\begin{align}
\| f^{(k)}(x) \| ^ 2 = \| A_k x - (A_k x^{(k)} - f(x^{(k)})) \|^2
\end{align}
<!-- $$ -->

Se minimiza por [Teorema](#thm:linleastsquaresol) cuando
<!-- $$ -->
\begin{align}
x &= A_k^{\dagger} (A_k x^{(k)} - f(x^{(k)})) \\
&=A_k^{\dagger} A_k x^{(k)} - A_k^{\dagger} f(x^{(k)}) \\
&= x^{(k)} - A_k^{\dagger} f(x^{(k)})
\end{align}
<!-- $$ -->

Entonces el algoritmo de Gauss-Newton queda definido de la siguiente manera:

\begin{algorithm}
\caption{Algoritmo Gauss-Newton para cuadrados mínimos no lineales}

Dada $f : \R^n \rightarrow \R^m$ diferenciable y un punto inicial $x^{(1)}$.
Con $k = 1, 2, ..., k^{max}$. \newline

1. Linealizar $f$ alrededor de $x^{(k)}$ computando el jacobiano $A_k$ y definiendo:
\begin{align}
f^{(k)}(x) = f(x^{(k)}) + A_k (x - x^{(k)})
\end{align}

2. Actualizar el iterador a $x^{(k+1)}$ como el mínimo de $\| f^{(k)}(x) \|^2$
utilizando la solución al problema de cuadrados mínimos lineales dada en el
\cref{thm:linleastsquaresol}. Se necesitará computar $A_k^{\dagger}$ con
la inversa de la matriz de Gram de $A_k$:
\begin{align}
x^{(k+1)} = x^{(k)} - A_k^{\dagger} f(x^{(k)}) =
x^{(k)} - (A_k^T A_k)^{-1} A_k^T f(x^{(k)})
\end{align}

\end{algorithm}

<!-- TODO@def: uso el término bundle adjustment -->

Gauss-Newton y minimización lineal con la pseudo-inversa serán de gran utilidad
para expresar numerosos tipos de problemas de optimización. Se utilizará para
problemas como ajustar la posición de un punto de interés tri-dimensional que es
observado por múltiples cámaras, desproyectar puntos de cámaras con modelos de
proyección que no tienen expresiones cerradas para su inversa, incluso veremos
que la optimización central de los sistemas de SLAM/VIO, el bundle adjustment,
son usualmente expresados y resueltos como una minimización de cuadrados no
lineales. El desarrollo de esta sección está basada en
[@nocedalNumericalOptimization2006, cap. 1, 2 y 10] y
[@boydIntroductionAppliedLinear2018, cap. 11, 12, 15 y 18]; en esos trabajos se
puede encontrar derivaciones alternativas e información de alternativas a
Gauss-Newton más sofisticadas como Levenberg-Marquardt o el método dogleg.

<!-- TODO@ref: el tema de las citas con capítulos se ve bastante feo en el estilo ACM -->

<!-- TODO: Acá se habla de weighted least squares: https://www.vectornav.com/resources/inertial-navigation-primer/math-fundamentals/math-leastsquares -->


<!-- TODO@def: explicar bundle adjustment -->
<!-- TODO@def: que es motion blur, (quizás usar nota al pie). EDIT: Very easy con pandoc footnote [^1] o inline_notes ^[nota] -->
<!-- TODO@def: Estoy implicitamente hablando de un optimizador, cuando hablo de factor graphs? -->
<!-- TODO@def: Explicar factores no-lineales, o almenos decir que no se explican -->
<!-- TODO@def: Que son features? -->
<!-- TODO@def: Que es loop closing? -->
<!-- TODO@def: Que es OpenCV -->
<!-- TODO@def: Que son grafos de poses, factor graphs, y factores -->
<!-- TODO@def: VIO habla acerca de componentes: (patch tracking, landmark
representation, first-estimate Jacobians, marginalization
scheme) que podría ser interesante discutir -->
<!-- TODO: Mencionar que TUM lo desarrolla y las personas que lo mantienen -->
<!-- TODO@def: Que es cuadrados minimos -->
<!-- TODO@def: Que es gauss newton -->
<!-- TODO@def: levenverg-marquard is also in use (see vio_lm_lambda_initial), I might need to explain it -->
<!-- TODO@def: que son SE(2), SO(3) etc: ver https://ethaneade.com/ -->
<!-- TODO@ref: Checkear que los 6 papers de basalt esten siendo citados -->
<!-- TODO@ref: Los papers de orbslam y kimera deberían estar citados -->

# Basalt

## Problemáticas preliminares

Un problema central en este tipo de sistemas es el de poder generar un mapa y
una trayectoria que sea _globalmente consistente_. Con esto nos referimos a que
nuevas mediciones tengan en cuenta todas las mediciones anteriores en el
sistema. Una forma ingenua de encarar este problema sería realizando _bundle
adjustment_ sobre todas las imágenes capturadas a lo largo de una corrida,
integrando de alguna forma todas las mediciones provenientes de la IMU.
Desafortunadamente, este método excede rápidamente cualquier capacidad de
cómputo de la que dispongamos, y aún más teniendo en cuenta que nuestro objetivo
es localizar en tiempo real al dispositivo de XR.

Por esta razón, es usual recurrir a distintas formas de reducir la complejidad
del problema. Para realizar _odometría visual-inercial (VIO)_, es común que
se ejecute la función de optimización sobre una _ventana local_ de cuadros y
muestras recientemente capturadas, ignorando muestras históricas y acumulando
error en las estimaciones a lo largo del tiempo. Además, este enfoque tiene la
problemática añadida de que una porción significativa de los fotogramas
capturados tienen posiciones similares que no añaden información al estimador, o
incluso que algunos fotogramas puedan ser de baja calidad por contener _motion
blur_ u otro tipo de anomalías. Por otro lado, soluciones que intenta realizar
_mapeo visual-inercial_ realizan el bundle adjustment sin utilizar todas las
imágenes capturadas, si no que se limitan a la utilización de algunos fotogramas
clave, o _keyframes_ elegidos mediante criterios que priorizan cuadros nítidos y
con distancias (_baselines_) prudenciales entre ellos.

Como las muestras de IMU vienen a altas frecuencias, es común que estas se pre
integren de forma tal de combinar muestras simultáneas entre dos keyframes en
una única entrada del optimizador. Sin embargo, un problema en el que esta
integración incurre, es que las mediciones de las IMU son altamente ruidosas, y
acumularlas durante tiempos prolongados acumula también cantidades
significativas de error. Este factor nos limita el tiempo que puede transcurrir
entre dos keyframes; como ejemplo en [@mur-artalVisualInertialMonocularSLAM2017]
se habla de keyframes que no pueden tener más de 0.5 segundos entre sí. A su
vez, tener keyframes a muy bajas frecuencias afecta la calidad de las
estimaciones de velocidad y biases; estos últimos son offsets de medición
inherentemente variables de los acelerómetros y giroscopios a los que es
necesario estimar para compensar por ellos en la medición final.

## Propuesta

La novedad de Basalt es que formula el mapeo visual-inercial como un problema de
bundle adjustment con mediciones visuales e inerciales a altas frecuencias.
Utiliza un _grafo de factores_ similarmente a otros sistemas, también llamado
_grafo de poses_ en este contexto por contener poses a estimar como nodos. En
lugar de utilizar todos los fotogramas se propone realizar la optimización en
dos capas. La capa de VIO, emplea un sistema de odometría visual-inercial, que
ya de por sí supera a otros sistemas del mismo tipo, proveyendo estimaciones de
movimiento a la misma frecuencia que el sensor de la cámara provee imágenes.
Luego, se seleccionan keyframes y se introducen _factores no-lineales_
entre estos que estiman la diferencia de posición relativa entre estos.
Estos dos factores, keyframes y poses relativas, se utilizan en la capa de
bundle-adjustment global.

La capa de VIO, utiliza features que son rápidas y buenas para tracking
(_optical flow_), mientras que en la capa de mapeo se usan features adecuadas
para _loop closing_ que son indiferentes a las condiciones de luz o al punto de
vista de la cámara. De esta forma tenemos un sistema que es capaz de utilizar
las mediciones a alta frecuencias de los sensores y al mismo tiempo tiene la
capacidad de detectar a frecuencias más bajas cuando se está en ubicaciones ya
visitadas, obteniendo así un mapa que es globalmente consistente. Además, el
problema de optimización se reduce, ya que a diferencia de otros sistemas, no es
necesario estimar velocidades ni biases.

## Implementación

A continuación se describe la arquitectura e implementación de Basalt de una
manera más detallada. Esta sección surge directamente de la lectura del código
fuente del sistema e intenta proveer detalles más bien pragmáticos que se
encuentran en el mismo, pero que pueden quedar escondidos en publicaciones de
más alto nivel. A su vez, se toman ciertas licencias literarias que deberían
ayudar al entendimiento y que no son posibles a la hora de escribir código.

### Odometría visual-inercial

Cómo vimos en la introducción, el funcionamiento de Basalt se divide en dos
etapas. La primera etapa de odometría visual-inercial (VIO), en el cual se
emplea un sistema de VIO que supera a sistemas equivalentes de vanguardia
mientras que la segunda etapa de mapeo visual-inercial (VIM), toma keyframes
producidos por la capa de VIO y ejecuta un algoritmo de _bundle adjustment_ para
obtener un mapa global consistente. Algo que no se mencionó en la introducción
es que estas dos capas son completamente independientes. En una corrida usual de
un dataset, lo que se realiza es la ejecución pura y exclusiva del sistema VIO y
es este el que decide y almacena persistentemente qué cuadros y con qué
información el sistema de VIM, de ejecutarse, debería utilizar al realizar el
proceso de _bundle adjustment_.

Esta sección explora los componentes fundamentales de la capa de VIO: _optical
flow_, _bundle adjustment visual-inercial_ y finalmente el proceso de
_optimización y de marginalización parcial_.

#### Optical flow

<!-- TODO@fig: algún gráfico que represente lo que le entra al módulo y lo que
sale, lo mismo para todo el pipeline de VIO, y lo mismo para todo Basalt -->

El módulo de VIO toma dos tipos de entrada, una de ellas son las muestras raw de
la IMU; y la otra, contra intuitivamente, no son las imágenes raw provenientes
de las cámaras, sino que son los _keypoints_ resultantes de ellas. Recordemos
que los keypoints no son más que la ubicación y rotación en dos dimensiones
sobre el plano de la imagen de las _features_ detectadas. Las features a su vez
son la representación de los puntos de interés o _landmarks_ de la escena
tri-dimensional proyectados sobre las imágenes. El proceso de detectar features,
computar su transformación entre distintos cuadros, y producir los keypoints de
entrada para el módulo de VIO, está a cargo del módulo de _optical flow_ (o
_flujo óptico_). Cabe aclarar que optical flow es el nombre que recibe tanto el
campo vectorial que representa el movimiento aparente de puntos entre dos
imágenes, como el proceso de estimarlo. Este puede ser denso, si se considera el
flujo de todos los píxeles, o no (_sparse_) si solo se computa el flujo de
algunos keypoints como en el caso que veremos.

El [módulo][`frametoframeopticalflow`] de optical flow corre en un thread
individual y es por donde las muestras del par de cámaras estéreo ingresan al
pipeline de Basalt. Inicialmente se genera una representación piramidal de las
imágenes, o también llamada de _mipmaps_, esta es una forma tradicional
[@williamsPyramidalParametrics1983] de almacenar una imagen en memoria junto a versiones
reescaladas de la misma (Fig. @fig:mipmap). Los mipmaps tienen múltiples utilidades en
computación gráfica (e.g., _filtrado trilineal_, _LODs_, reducción de
_patrones moiré_) pero en el caso de Basalt serán utilizados para darle robustez
al algoritmo de seguimiento de features (_feature tracking_).

[`frametoframeopticalflow`]: TODO

![
Representación piramidal (mipmaps) de un cuadro del conjunto de datos EuRoC.
](source/figures/mipmap.jpg "Mipmaps"){#fig:mipmap width=100%}

Posteriormente se realiza la detección de features nuevas sobre las imágenes
utilizando el algoritmo _FAST_ para detección de esquinas
[@rostenFasterBetterMachine2010a] implementado sobre OpenCV. Aquí es notable
aclarar que Basalt es uno de los sistemas que menos depende de OpenCV, ya que
tiende a re implementar muchas de las técnicas y algoritmia de forma
especializada y, como veremos en otros módulos, otras tareas razonablemente
complejas como la optimización de grafos de poses se implementan también dentro
del proyecto y sin recurrir a librerías externas. Esta es una de las varias
razones por las que este sistema logra tan buen rendimiento, ya que las
librerías externas suelen tener campos y comprobaciones dedicadas al caso
general del problema que intenta solucionar, mientras que Basalt puede
prescindir de todas las que no apliquen al problema de VIO. Siguiendo con la
detección de features, una heurística particular de Basalt es la división del
cuadro completo en celdas de tamaño configurable (por defecto 50 por 50 píxeles)
en donde se detectan las nuevas features, por celda solo se conserva la feature
de mejor calidad o con mejor _respuesta (response)_ (aunque la cantidad a
conservar es también configurable), y siempre que la celda tenga alguna feature
localizada de frames anteriores, no se intenta detectar nuevas. Esto contrasta
con sistemas como Kimera-VIO que corren la detección FAST sobre el cuadro entero
y evitan la redetección mediante el uso de _máscaras_ que le instruyen al
algoritmo a obviar esas secciones. Desafortunadamente la construcción de tales
máscaras suele ser costosa y la heurística de Basalt, a pesar de desperdiciar
espacio por no permitir la detección de nuevas características entre celdas, es
más eficiente ya que en situaciones comunes se logran detectar una cantidad
razonable de features sin problemas. Esta detección de features nuevas se
realiza unicamente sobre la primera cámara (usualmente la izquierda), mientras
que en la otra cámara se reutiliza el método de seguimiento de keypoints que se
describe a continuación.

<!-- TODO@fig: Agregar imágenes de los parches, de la detección de features, del optical flow -->

En cada instante de tiempo que entran un nuevo par de imágenes se tiene acceso a
toda la información recolectada del instante anterior, en particular a sus
keypoints. Una suposición razonable es que las imágenes correspondientes a este
nuevo instante van a compartir mucho de los keypoints con las imágenes
anteriores y en posiciones similares. En base a esa suposición Basalt logra
ahorrarse tener que volver a detectar features de la imagen con FAST y en cambio
el problema se transforma en, dado una imagen anterior (inicial), sus keypoints
y una imagen nueva (objetivo), estimar donde ocurren esos mismos keypoints en la
imagen nueva. Para esto, por cada keypoint anterior, se genera un parche
$\Omega$ alrededor de su ubicación de, por defecto, 52 coordenadas de píxeles
(i.e., un círculo rasterizado en un bloque de 8 por 8 píxeles). Considerando
entonces que este parche debería estar en la imagen nueva en coordenadas
cercanas a las del keypoint anterior, queremos encontrar la transformación $T
\in SE(2)$ que le ocurrió al parche, y por ende al nuevo keypoint que se
encontraría en el centro de este nuevo parche. Basalt emplea entonces
optimización por cuadrados mínimos mediante el algoritmo iterativo de
Gauss-Newton para encontrar $T$ utilizando un residual $r$ con:

<!-- TODO@correct: Realmente es gauss newton lo que se hace? ver optical_flow_max_iterations -->
<!-- TODO@correct: Not quite, es inverse-compositional method, que es un gauss newton
sobre algo un poco distinto: https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0910/zhao.pdf
por eso aparece el hessiano y cosas de esa pinta -->
<!-- TODO: Mencionar ZNCC como norma no utilizada: https://martin-thoma.com/zero-mean-normalized-cross-correlation/ -->

$$
r_i =
  \frac{I_{t + 1}(\mathbf{T} \mathbf{x}_i)}{\overline{I_{t + 1}}} -
  \frac{I_{t}(\mathbf{x}_i)}{\overline{I_{t}}}
  \ \ \ \ \forall \mathbf{x}_i \in \Omega
$$

con $I_t(\mathbf{x})$ la intensidad de la imagen anterior en el pixel ubicado en
las coordenadas $\mathbf{x}$ (análogamente $I_{t + 1}(\mathbf{x})$ para la
imagen objetivo); y $\overline{I_{t}}$ siendo la intensidad media del parche
$\Omega$ en la imagen inicial (análogamente $\overline{I_{t + 1}}$ para la
imagen objetivo y el parche transformado $\mathbf{T}\Omega$). Notar que al
normalizar las intensidades obtenemos un valor que es invariante incluso ante
cambios de iluminación.

Los detalles del cálculo de gradientes y jacobianos están basados en el método
de Lucas-Kanade para tracking de features (_KLT_)
[@lucasIterativeImageRegistration1981]. El uso adicional de mipmaps sobre KLT
fue originalmente expuesto en [@bouguetPyramidalImplementationLucas1999].

<!-- TODO@def: "asegurar que la estimacion fue exitosa" == outlier filtering.
Quizás hablar un poco de eso -->

Para asegurar que la estimación fue exitosa, se invierte el problema y se
intenta trackear desde la imagen nueva hacia la inicial y, si el resultados está
muy alejado de la posición inicial, el nuevo keypoint se considera inválido y se
descarta. Otro detalle a aclarar es que, recordando que la detección de features
con FAST solo ocurre en las imágenes de una de las cámaras, es posible ahora
entender que las features en la segunda cámara son "detectadas" con este método,
es decir, simplemente se considera la imagen de la segunda cámara en el mismo
instante de tiempo como la imagen objetivo.

Finalmente, el último de los pasos que ocurre cuando el módulo de optical flow
procesa un cuadro es el de filtrado de keypoints, en el cual se desproyectan los
keypoints a posiciones en la escena tri-dimensional y en caso de que el error
epipolar supere cierto umbral, estos keypoints serán descartados.

<!-- TODO@def: Que es la desproyección -->
<!-- TODO@def: Qué es el error epipolar -->

#### Bundle adjustment visual-inercial

<!-- Cosas que tienen que estar:
- [ ] pi es estático (no autocalibration comparado a openvins)
- [ ] se estima la pose del IMU
- [ ] el estado es sk (frame_poses?), sf (frame_states), sl (lmdb)
- [ ] "representation of unit vectors in 3D" stereographic projection
- [ ] "reprojection error"
 -->

<!-- TODO@def: Qué es bundle adjustment -->

En un hilo separado al módulo de optical flow, corre el estimador de VIO
encargado de realizar en bundle adjustment sobre los cuadros y muestras de la
IMU recientes para estimar la pose. Este toma como entrada las muestras de la
IMU junto a los keypoints 2D detectados para cada imagen, o sea la salida del
módulo de optical flow. Este módulo es el que efectivamente realizará la
integración y optimización con toda la información recibida y producirá como
salida en una cola, la estimación de los estados del agente a localizar.

##### Inicialización y pre-integración {#basalt-preintegration}

<!-- TODO@def: referencia a la sección "Calibración de IMU", escribirla, referenciarla -->

Para comenzar, el hilo de procesamiento de este módulo espera a que la primera
muestra de la IMU arribe. Estas muestras son recibidas de forma raw y antes de
tratarlas, Basalt utiliza los parámetros de calibración estáticos provistos por
archivos de configuración para corregirlas. La corrección, o calibración, ocurre
como se explica en la sección de "Calibración de IMU" sin considerar todavía los
parámetros de los procesos aleatorios detallados en la misma. Una particularidad
de Basalt, es que el acelerómetro es utilizado como origen del agente localizado
y, fundándose en esto, se fija su orientación. Es decir, no se aplica ningún
tipo de corrección de orientación al calibrar las muestras del acelerómetro.
Esto hace que la matriz de alineamiento para el acelerómetro tenga ceros en su
triángulo superior (ver [@schubertBasaltTUMVI2018 secc. IV.B] y _discusión
relacionada [^basalt-headers-issue8]_).

<!-- TODO@style: Make footnotes clickeable -->
<!-- TODO@style: También hacer que "discusion relacionada" se marque y sea clickeable quizas? -->

[^basalt-headers-issue8]: <https://gitlab.com/VladyslavUsenko/basalt-headers/-/issues/8>

Luego de recibir esta primer muestra de la IMU se comienza la ejecución del
bucle principal, el cual espera indefinidamente por resultados encolados por el
módulo de optical flow para realizar una iteración. El primer par de muestras de
cámara junto a la primera muestra de la IMU posterior al par estéreo son
utilizados para inicializar el estado del agente en el primer cuadro. Esto es ya
que a cada cuadro se le asigna un estado que se compone de la posición,
orientación, velocidad y biases del giroscopio y acelerómetro que se estimaron
para tal cuadro. Notar que en Basalt, hablar de cuadros es equivalente a hablar
de instantes de tiempo, ya que los únicos puntos en el tiempo considerados son
las timestamps del par estéreo de imágenes recibidas.

Para inicializar el primer estado se toman varias suposiciones. En particular,
se asume que el dispositivo comienza en la posición $(0, 0, 0)$ y sin
aceleración ni velocidad, esto permite utilizar el vector de aceleración
reportado por la muestra del acelerómetro como el vector de gravedad y computar
así la inclinación del agente. Notar que esta inclinación no es capaz de
informar la orientación de forma completa al no poder contemplar uno de los ejes
de rotación del cuerpo. Por esta razón es recomendable iniciar la corrida con el
agente rotado con su eje $+\mathbf{Z}$ paralelo al vector gravedad, esto hará
que Basalt compute la orientación identidad. Tal rotación suele corresponder con
la posición de reposo pensada por el fabricante, o al menos este ha sido el caso
en los dispositivos utilizados en este trabajo. Además, es conveniente
posicionar el agente mirando hacia “adelante” (ajustar el _yaw_), como el
usuario considere apropiado según su entorno.

<!-- TODO@correct: No supe explicar la inicialización de marg_data en este punto por que todavía no la había leído -->

<!-- TODO@def: explicar pitch, roll, yaw -->
<!-- TODO@maybe: explicar por qué no basta con el acelerómetro para definir la orientación completa con un grafico,
hablar del producto cruz entre g y +Z, tilt vs orientación -->

En instantes posteriores (i.e., al recibir nuevas imágenes), se realiza la
llamada pre-integración de muestras consecutivas de la IMU. Considerando que
estas muestras arriban a mayores frecuencias que las de las cámaras,
pre-integrarlas es un proceso que intenta resumir las muestras entre los cuadros
a una única pseudo-muestra que sucede en los mismos instantes de tiempo que los
cuadros como se muestra en el ejemplo de @fig:sample-frequencies.

![
Frecuencia de distintos eventos para un ejemplo con cámaras a 30fps y muestras
de la IMU a 240hz.
](source/figures/sample-frequencies.pdf "Ejemplo de
frecuencias"){#fig:sample-frequencies width=100%}

El proceso de pre-integración es el siguiente. Dado el cuadro previo $i$ con
timestamp $t_i$ y el cuadro posterior $j$ con timestamp $t_j$, se intenta
computar una pseudo-muestra $\Delta \mathbf{s} = (\Delta \mathbf{R}, \Delta \mathbf{v},
\Delta \mathbf{p})$ que representa cambios de orientación, velocidad y posición
respectivamente según las mediciones de la IMU que ocurrieron desde $t_i$ hasta
$t_j$. Para cada timestamp $t$ de la IMU tal que $t_i < t \leq t_j$ tenemos la
muestra de aceleración lineal $\mathbf{a}_t$ y de velocidad angular
$\mathbf{\omega}_t$. Definimos entonces de forma recursiva la pseudo-muestra
$\Delta \mathbf{s}$ de la siguiente manera:

<!-- TODO@def: entender este conjunto de ecuaciones requiere:
- saber que R es 3x3. Y que es lo que significa multiplicar por R
- qué es Exp
 -->

<!-- $$ -->

\begin{align}
\label{eq:imu-preintegration}
(\Delta \mathbf{R}_{t_i}, \Delta \mathbf{v}_{t_i}, \Delta
\mathbf{p}_{t_i}) & := (\mathbf{I}, \mathbf{0}, \mathbf{0})
\\
\Delta \mathbf{R}_{t+1} & := \Delta \mathbf{R}_t Exp(\mathbf{\omega}_{t+1} \Delta t)
\\
\Delta \mathbf{v}_{t+1} & := \Delta \mathbf{v}_t + \Delta{\mathbf{R}_t}
\mathbf{a}_{t+1} \Delta t
\\
\Delta \mathbf{p}_{t+1} & := \Delta \mathbf{p}_t + \Delta \mathbf{v}_t \Delta t
\\
\Delta \mathbf{s}_{t} & := (\Delta \mathbf{R}_{t}, \Delta \mathbf{v}_{t}, \Delta
\mathbf{p}_{t})
\\
\Delta \mathbf{s} & := \Delta \mathbf{s}_{t_j}
\end{align}

<!-- $$ -->

Es destacable mencionar que este tipo de pre-integración es también utilizado
por los otros sistemas estudiados Kimera y ORB-SLAM3. La ventaja que presenta es
que sus características son bien conocidas gracias al trabajo de
[@forsterOnManifoldPreintegrationRealTime2017] y las expresiones necesarias para
el cómputo de residuales, como sus jacobianos, son cerradas y fueron derivadas
de forma ejemplar en dicho trabajo.

Entonces, con esta muestra pre-integrada junto a los datos del nuevo cuadro (sus
keypoints), se procede a la etapa de `measure` del módulo de VIO. Aquí lo
primero que se hace es predecir que el estado de este nuevo instante estará
basado en el estado del instante anterior más la adición de las muestras
pre-integradas de la IMU. El resto de la etapa de `measure` se basa en el manejo
y actualización de la base de datos de los puntos de interés en 3D, o
_landmarks_, y sus observaciones, junto a algo que, en Basalt, está fuertemente
ligado: la toma de cuadros clave, o _keyframes_.

##### Base de datos de landmarks

Recordemos que el módulo de optical flow encuentra keypoints en cada cuadro,
esto es, una landmark o punto de interés en la escena 3D proyectada sobre el
plano de la imagen 2D. Más aún este módulo era capaz de hacer el seguimiento de
keypoints similares mediante optical flow, es decir, de keypoints que observan a
la misma landmark. Parte de nuestro objetivo entonces será triangular las
posiciones de estas landmarks considerando las observaciones tomadas.
Consideremos además la naturaleza altamente ruidosa de estas observaciones, con
landmarks que aparecen y desaparecen de la visión de los cuadros por múltiples
razones como: ser ocluidas por objetos de escena, ser distorsionadas por el
ángulo del observador, artefactos intrínsecos de los sensores ópticos como el
motion blur o el ruido introducido por la ganancia del amplificador de señal
digital, o simplemente porque dejan de estar en el campo de visión de las
cámaras. Por estas razones entonces, será fundamental la correcta gestión de la
información de las landmarks y sus observaciones. En Basalt, la clase que se
encarga de esto es la `LandmarkDatabase` con la siguiente estructura.

```C++
class LandmarkDatabase {
  map<LandmarkId, Landmark> landmarks;
  map<FrameId, map<FrameId, Keypoint>> observations;
}

class Landmark {
 FrameId keyframe;
 Vector2 direction;
 double inverse_distance;
}

class Keypoint {
  LandmarkId landmark_id;
  Vector2 position;
}
```

En la implementación de este Módulo, los términos de keypoint y landmark tienden
a utilizarse de forma intercambiable, significando keypoint algo distinto a lo
que era en el módulo de optical flow. Para evitar confusión, se han diferenciado
los términos de manera explícita en el pseudo código anterior. `Landmark` se
utilizará para referirse al punto de interés en la escena tridimensional,
mientras que `Keypoint` será un punto 2D que observa la proyección de una
landmark definida por `landmark_id`. Entonces la `LandmarkDatabase` es
simplemente una colección de todas las `landmarks` de interés y de los keypoints
que la observaron en `observations`.

Una `Landmark` surge de un keypoint observado en el módulo de optical flow en
algún cuadro y comparte el mismo identificador. Explicaremos los campos
`direction` e `inverse_distance` que determinan la posición en 3D de la misma
más adelante. Un cuadro se identifica tanto por la timestamp en el que fue
tomado como por cuál de las dos cámaras lo tomó; `FrameId` tiene esta
información. Una landmark existe en referencia a un cuadro, y un cuadro que es
referenciado por landmarks debe ser un keyframe por la implementación; decimos
que el keyframe aloja estas landmarks. Una observación en `observations` tiene
entonces un mapeo de keyframes a los `Keypoints` que observan a las landmarks
alojadas en el keyframe. Un `Keypoint` es reconocido en un cuadro particular, y
solo tiene sentido como coordenadas en ese cuadro, es esto lo que representa el
segundo `FrameId` de la definición de `observations`.

Habiendo dicho esto, al recibir un nuevo cuadro `measure` simplemente recorre
todas las observaciones o `Keypoint`s que este trae y se añaden a la base de
datos las observaciones de landmarks ya existente en la misma. Observaciones de
landmarks no registradas en la base de dato se guardan para poder determinar si
el módulo amerita la toma de un nuevo keyframe.

##### Keyframes

En contraste con sistemas como Kimera y ORB-SLAM3 que tienen condiciones más
intrincadas, en Basalt, la heurística para decidir si el cuadro actual será un
keyframe es muy sencilla: si _más del 30% de las observaciones del cuadro actual
corresponden a landmarks no registradas y han sucedido más de, por defecto, 5
cuadros consecutivos que no fueron keyframes_, el cuadro actual será tomado como
un keyframe. La toma de keyframes es lo que registra nuevas landmarks a la base
de datos y realiza la estimación inicial de su posición.

En primer lugar, todas las observaciones _“desconectadas”_ correspondientes al
30% o más anterior que no correspondían a ninguna landmark, intentarán ser
registradas en la base de datos. Para esto es necesario poder encontrar una
segunda observación con la que realizar la triangulación y poder así estimar la
posición tridimensional de la landmark al registrarla.

Se tiene entonces que para cada observación desconectada $\mathbf{p}_h \in \R^2$
producida por la cámara $h$ del keyframe se recorrerán todos los cuadros desde
el último keyframe, buscando por una segunda observación $\mathbf{p}_t \in \R^2$
de esta landmark producida en alguna cámara $t$. En caso de encontrarla se sigue
considerando lo siguiente.

<!-- LTeX: language=es-AR -->

- La cámara $h$ dels keyframe tiene una pose estimada para la IMU en esa timestamp
  que denominaremos $\mathbf{T}_{i_h} \in SE(3)$. Similarmente tendremos
  $\mathbf{T}_{i_t}$ para la cámara $t$.

- A su vez como los parámetros de calibración son estáticos y conocidos,
  conocemos la función de proyección $\pi_h$, sus parámetros intrínsecos
  $\mathbf{i}_h$ y la pose relativa de la cámara $h$ respecto a la IMU. Llamaremos
  a esta transformación fija $\mathbf{T}_{i_h c_h} \in SE(3)$. Similarmente con
  $\pi_t$, $\mathbf{i}_t$ y $\mathbf{T}_{i_t c_t}$ para la cámara $t$.

- Podemos ahora desproyectar $\mathbf{p}_h$ y $\mathbf{p}_t$ a sus respectivas
  posiciones 3D estimadas $\mathbf{p}'_h := \pi^{-1}_h(\mathbf{p}_h, \mathbf{i}_h)$
  y $\mathbf{p}'_t := \pi^{-1}_t(\mathbf{p}_t, \mathbf{i}_t)$ con $\mathbf{p}'_h,
\mathbf{p}'_t \in \R^3$.

- Computamos ahora la transformación de la IMU de $h$ a la IMU de $t$ dada por
  $\mathbf{T}_{i_h i_t} := \mathbf{T}_{i_h}^{-1} \mathbf{T}_{i_t}$

- Luego podemos tener la transformación de la cámara $h$ a $t$ con
  $\mathbf{T}_{c_h c_t} := \mathbf{T}_{i_h c_h}^{-1} \mathbf{T}_{i_h i_t}
\mathbf{T}_{i_t c_t}$

- Finalmente con estos tres datos $\mathbf{p}'_h$, $\mathbf{p}'_t$ y
  $\mathbf{T}_{c_h c_t}$ es posible realizar la triangulación utilizando DLT con
  SVD como se explicó en la sección "DLT con SVD" para obtener un punto en
  coordenadas homogéneas en $\R^4$ con el cuarto componente representando el
  inverso de la distancia entre la cámara y el punto de interés, mientras que
  los tres primeros componentes corresponden al _bearing vector_, es decir, un
  vector unitario que determina la dirección desde la cámara hacia la landmark.

<!-- TODO@def: distancia inversa: ver paper referenciado en basalt [6]: Inverse depth parametrization
for monocular SLAM -->
<!-- TODO@def: Este último punto está raro por que no entendía bien de lo que
estaba hablando -->
<!-- TODO@def: bearing vector -->
<!-- TODO@def: la sección "DLT con SVD" no existe. Buscar DLT triangulation with SVD,
quizás ver el apendix de multiple view geometry que se veía bueno -->
<!-- TODO@def: que son coordenadas homogéneas. Supongo que se explicaría casi por
su cuenta en la sección "DLT con SVD" cuando se explicar el resultado de la triangulación -->

Un detalle a considerar es que Basalt comprueba que la distancia relativa entre
los dos cuadros, la baseline, sea lo suficientemente grande para considerar la
triangulación exitosa, de lo contrario se busca un nuevo cuadro para comparar
con el keyframe. Esta comprobación se reduce a revisar que la norma del vector
de traslación contenido en $\mathbf{T}_{c_h c_t}$ sea de, por defecto, más
de 5cm.

Como se ve en la definición de `Landmark`, la posición 3D de estos puntos de
interés no se almacena exactamente de la misma forma que la triangulación los
produce. En particular, no se almacena el bearing vector directamente, sino que
se utiliza un punto 2D más compacto `direction` que lo codifica (para esto se
utiliza una proyección estereográfica como se explica en la Figura
@fig:stereographic-projection) junto a `inverse_distance`, la distancia inversa
a este punto producto de la triangulación, de esta forma la posición de la
landmark queda ligada al keyframe que la aloja.

![
Interpretación geométrica de la proyección estereográfica utilizada para
representar bearing vectors. Las coordenadas definidas por la propiedad `Vector2
direction` definen un punto en el plano $XY$ ($Z=0$) mostrado en azul. Para
obtener el vector unitario correspondiente, se traza una línea desde el punto
$(0 0 -1)^T$ hacia `direction` en el plano $XY$. El vector en el que esta línea
interseca a la esfera unitaria será el bearing vector codificado. Se muestran
tres ejemplos en rojo, verde y amarillo, con lineas punteadas que representan
las líneas trazadas y flechas representando los bearing vectors obtenidos.
](source/figures/stereographic-projection.png "Stereographic Projection"){#fig:stereographic-projection width=100%}

Si todos los procedimientos relacionados a la triangulación de estos dos cuadros
fueron correctos, se almacena la landmark nueva en la base de datos. De haber
otras observaciones de esta landmark no se utilizan todavía para añadir
información a su posición, si no que simplemente se añaden las observaciones
para uso futuro.

<!-- TODO@license: openvslam, avoid reading ORB-SLAM3 code -->
<!-- TODO@future: punto de mejora para basalt: usar dogleg minimization en vez de levenberg-marquardt. No se si vale la pena mencionarlo -->
<!-- TODO@question: question for basalt: why are they not using gtsam/g2o/ceres for the solvers? -->
<!-- TODO@future: parallelization/vectorization of gauss newton seems very easy, levenberg marquardt not so much -->


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

<!-- TODO@fig: Reemplazar figura manuscrita por diagrama final -->

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

[^openxr-time-limits]: La especificación de OpenXR tiene una sección dedicada a
las restricciones y condiciones a los que el runtime está sujeto respecto a
solicitudes en el pasado y en el futuro por parte del usuario.
<https://www.khronos.org/registry/OpenXR/specs/1.0-khr/html/xrspec.html#prediction-time-limits>

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

![ Ejemplo de predicción para tiempos $t \in \{1,45; 1,75; 1.95\}$ ignorando las
muestras de IMU y utilizando unicamente el historial de poses con `A` y `B` como
últimas muestras (esto es antes de que llegue `C`). De vuelta, asumimos que las
estimaciones y no contienen error por simplicidad.
](source/figures/prediction-without-imu.pdf "Predicción sin uso de muestras IMU"){#fig:prediction-without-imu width=100%}

<!-- TODO@ref: la especificación de openxr debería aparecer en la bibliografía -->


<!-- TODO:
explicar los 4 tipos de predicción
-->

#### Filtrado de poses

<!-- NOW:
1. commitear
3. grafico mas poses con problemas de ruido
 -->

 <!-- snapping por ruido de prediccion, snapping por funcionamiento del sistema de SLAM , ejemplo del snap que hace orb slam3  -->

<!-- TODO: "On averaging rotations" para justificar la interpolación de los quaternions? -->
TODO: Explicaría los distintos tipos de filtros en uso para reducir el jittering
en las poses: moving average, exponential smoothing, one-euro filter

<!-- grafico de como funciona la predicción y los problemas que trae? dos streams de estimaciones -->

### Recapitulando

TODO: Resumiría todas las partes describiendo el flujo de datos como
se vió en la imagen con la que arranca esta sección.

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




# References {.unnumbered}
