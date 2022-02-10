<!-- TODO@def: outlier -->
<!-- TODO@def: debería aclarar de alguna forma que los vectores son verticales -->

### Optimización por cuadrados mínimos

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

#### Cuadrados mínimos lineales

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
\begin{align}
E(x) = \sum_{i=1}^m{r_i(x) ^ 2} = \| r(x) \| ^ 2
\end{align}

Notar que la definición de $E(x)$ coincide con la de la _norma euclídea_ al
cuadrado de $r(x)$. Encontrar $x$ que minimice $E(x)$ con residuales lineales
es el _problema de los cuadrados mínimos lineales_; a $x$ le decimos _solución_
de tal problema. Notar que $r_i = (Ax - b)_i$, o sea el componente $i$ del
vector $Ax - b \in \R^m$, y por ende $r(x) = Ax - b$.
\begin{align}
E(x) = \sum_{i=1}^m{(Ax - b)_i^2} = \| Ax - b \| ^ 2
\end{align}

Lo que queremos minimizar es entonces equivalente a la norma cuadrada del vector
residual $Ax - b$. Introduciremos a continuación una serie de conceptos y
teoremas necesarios para poder presentar una forma sucinta de minimizar esta
norma.

Aceptaremos el siguiente teorema sin demostración (ver
@shoresAppliedLinearAlgebra2007, teoremas 2.7 y 3.7).

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

Proof
: Como $A$ tiene columnas linealmente independientes, por
[](#thm:li1inv2nots3) (3) tenemos que $x = 0 \Leftrightarrow Ax = 0$, nos basta
con ver que $Ax = 0 \Leftrightarrow A^T A x = 0$.
\bigbreak
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

Con estas herramientas, estamos en posición de presentar la solución directa al
problema de los cuadrados mínimos lineales.

Theorem thm:linleastsquaresol
: $\hat{x} = A^{\dagger} b$ es **la** solución del problema de los cuadrados mínimos
lineales. Es decir $\forall x \in \R^n: E(\hat{x}) = \| A\hat{x} - b \| ^ 2
\leq \| Ax - b \| ^ 2 = E(x)$.

Proof
: Tenemos primero que
\begin{align}
  & \hat{x} = A^\dagger b \\
  &\Leftrightarrow \hat{x} = (A^T A)^{-1} A^T b \\
  &\Leftrightarrow A^T A \hat{x} = A^T b \\
  &\Leftrightarrow A^T (A \hat{x} - b) = 0 \label{eq:ataxmbis0}
\end{align}
Las últimas dos ecuaciones reciben nombres particulares [^normalequations]
[^orthogonalityprinciple]. Veamos ahora para un $x \in \R^n$ cualquiera.
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
Más aún, esta solución es única ya que la igualdad en la última ecuación solo se
da si $\|A(x-\hat{x})\|^2 = 0$, y como $A$ es no-singular, esto solo pasa
cuando $x=\hat{x}$.

[^normalequations]: La expresión $A^T A x = A^T b$ suele ser referida como las
_ecuaciones normales_. La derivación de la solución de cuadrados mínimos
presentada en este trabajo no es la única. De hecho, es común encarar el
problema mediante cálculo diferencial. En ese contexto, las ecuaciones normales
surgen naturalmente a la hora de optimizar $E(x)$ igualando su gradiente a $0$.
Para una demostración mediante cálculo referirse a
@nocedalNumericalOptimization2006, cap. 10.

[^orthogonalityprinciple]: La expresión $A^T (A\hat{x} - b) = 0$ es interesante,
ya que muestra que las columnas de $A$ son ortogonales al residual óptimo
$A\hat{x} - b$ al ser su producto interno $0$. Esto suele llamarse el _principio
de ortogonalidad_.

#### Cuadrados mínimos no lineales

Generalizaremos el problema anterior para que también considere funciones no
lineales. Reutilizaremos la notación introducida en la sección anterior.

En este caso permitimos ahora que las $f_i$ sean no lineales, aunque requerimos
que continúen siendo diferenciables. Además, ignoraremos el vector $b$ haciendo
que $f(x) = r(x)$. Es decir querremos que $f(x) = 0$ en lugar de $f(x) = b$. En
el caso de necesitar la segunda restricción, podemos construir nuevas
funciones $\tilde{f}_i(x) = f_i(x) - b_i$ y utilizar estas en su lugar. Nuestra
función de error es entonces:
\begin{align}
E(x) = \sum_{i=1}^m{f_i(x)^2} = \| f(x) \| ^ 2
\end{align}

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
@nocedalNumericalOptimization2006, cap. 10. En el caso no lineal sin embargo,
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
\begin{align}
f^{(k)}(x) = f(x^{(k)}) + A(x^{(k)}) (x - x^{(k)})
\end{align}

con $A: \R^n \rightarrow \R^{m \times n}$ la matriz jacobiana de $f$.
\begin{align}
A = \begin{bmatrix}
  \frac{\partial f_1}{\partial x_1} & \dots & \frac{\partial f_1}{\partial x_n} \\
  \vdots & \ddots & \vdots \\
  \frac{\partial f_m}{\partial x_1} & \dots & \frac{\partial f_m}{\partial x_n}
\end{bmatrix}
\end{align}

Notar que $f^{(k)}$ es afín; una transformación lineal $A(x^{(k)})$ aplicada
sobre $x$, más un vector. Reacomodemos los términos para dejarlo explícito
e introduzcamos la notación $A_k = A(x^{(k)})$.
\begin{align}
f^{(k)}(x) = f(x^{(k)}) + A_k (x - x^{(k)}) \\
f^{(k)}(x) = A_k x - (A_k x^{(k)} - f(x^{(k)}))
\end{align}

**Actualización**. Teniendo en mente que queremos encontrar el mínimo de $\|
f(x) \| ^ 2$, lo aproximamos con el mínimo (y próximo iterando) $x^{(k+1 )}$ de
$\| f^{(k)}(x) \| ^ 2$ pero como $f^{(k)}$ es afín, esto se reduce a buscar la
solución del problema de cuadrados mínimos _lineales_. Sabemos por
[Teorema](#thm:linleastsquaresol) la solución exacta para este caso en base a la
matriz pseudo-inversa $A_k^{\dagger} = (A_k^T A_k)^{-1} A_k^T$.
\begin{align}
\| f^{(k)}(x) \| ^ 2 = \| A_k x - (A_k x^{(k)} - f(x^{(k)})) \|^2
\end{align}

Se minimiza por [Teorema](#thm:linleastsquaresol) cuando
\begin{align}
x &= A_k^{\dagger} (A_k x^{(k)} - f(x^{(k)})) \\
&=A_k^{\dagger} A_k x^{(k)} - A_k^{\dagger} f(x^{(k)}) \\
&= x^{(k)} - A_k^{\dagger} f(x^{(k)})
\end{align}

Entonces el algoritmo de Gauss-Newton queda definido de la siguiente manera:

\begin{algorithm}[H]
\caption{Gauss-Newton para cuadrados mínimos no lineales}

Dada $f : \R^n \rightarrow \R^m$ diferenciable y un punto inicial $x^{(1)}$.
Con $k = 1, 2, ..., k^{max}$. \newline

1. Linealizar $f$ alrededor de $x^{(k)}$ computando el jacobiano $A_k$:
\begin{align}
f^{(k)}(x) &= f(x^{(k)}) + A_k (x - x^{(k)})
\end{align}

1. Actualizar el iterador a $x^{(k+1)}$ con el minimizador de $\| f^{(k)}(x) \|^2$
descripto en el \cref{thm:linleastsquaresol}. Se necesitará computar $A_k^{\dagger}$
con la inversa de la matriz de Gram de $A_k$:
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
@nocedalNumericalOptimization2006, cap. 1, 2 y 10 y
@boydIntroductionAppliedLinear2018, cap. 11, 12, 15 y 18; en esos trabajos se
puede encontrar derivaciones alternativas e información de alternativas a
Gauss-Newton más sofisticadas como Levenberg-Marquardt o el método dogleg.

<!-- TODO@low: Acá se habla de weighted least squares: https://www.vectornav.com/resources/inertial-navigation-primer/math-fundamentals/math-leastsquares -->
