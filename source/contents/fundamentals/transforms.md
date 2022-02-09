### Transformaciones

Usualmente necesitaremos manipular y referirnos a transformaciones
tridimensionales entre distintos sistemas de referencias como se muestra en la \figref{fig:transforms}. Estos sistemas surgen
de las entidades que forman parte de nuestro proceso de optimización en SLAM.
Algunos ejemplos de transformaciones en los que podríamos estar interesados son
las que describen que transformación es necesaria realizar sobre la cámara
izquierda para llegar a la cámara derecha de nuestro dispositivo, o la
transformación que le ocurrió al agente localizado entre el instante anterior y
el actual.

\fig{fig:transforms}{source/figures/transforms.pdf}{Transformaciones}{%
Intuición de lo que representa una transformación $T$ que rota y traslada el
sistema de referencia $A$ hacia $B$. En general estas transformaciones tendrán
una inversa $T^{-1}$ que puede deshacer la acción original. Notar que un
punto en el espacio $p \in \R^3$ tiene diferentes coordenadas dependiendo de que
sistema se tome como referencia.
}

<!-- #define MN_RIGID_BODY_MOVEMENT %\
No profundizaremos en la definición formal de este concepto pero, intuitivamente,
son transformaciones que al aplicarlas sobre un conjunto de puntos, preservan su volumen.
Esto implica que preservan la norma y el producto cruz.
-->

El tipo de transformación en el que estamos interesados son los _movimientos de
cuerpo rígido_\marginnote{MN_RIGID_BODY_MOVEMENT}. Estos pueden describirse
mediante _traslaciones_ y _rotaciones_.  Además, también nos gustaría poder
expresar la _ubicación_ y _orientación_ de las entidades en nuestro sistema.
Estas dos características conforman la _pose_ en el espacio de tal entidad.
Es posible describir este concepto como una transformación aplicada sobre un
sistema de referencia global fijo. Por ejemplo en la \figref{fig:transforms}
si pensamos en $A$ como este origen global, tenemos entonces que $T$ está
describiendo la pose de $B$ con respecto a $A$.
A continuación, desarrollaremos algunas definiciones que nos ayudarán a describir la
idea de transformación más formalmente, y utilizaremos este mismo concepto para
identificar las poses de nuestras entidades.

#### Preliminares del álgebra lineal {#sec:linearalg-prelim}

Comenzaremos construyendo sobre algunas ideas básicas del álgebra lineal.

Definition
: Una transformación lineal $L$ entre dos espacios vectoriales $V, W$ es una
función $L : V \rightarrow W$ tal que:
\bigbreak
\begin{itemize}
  \item $L(x + y) = L(x) + L(y) \quad \forall x, y \in V$
  \item $L(ax) = aL(x) \quad \forall a \in \R$
\end{itemize}

Property (Matriz de una transformación)
: Si $V$ tiene base canónica $e_1, ..., e_n$ con $e_i \in \R^m$ tenemos que la matriz $A =
[L(e_1), ..., L(e_n)] \in \R^{m \times n}$ cumple $Ax = L(x) \quad \forall x \in V$

Property (Matrices cuadradas)
: El conjunto de matrices en $\R^{n\times n}$, con las operaciones de adición y
multiplicación matricial usuales, forman un anillo[^ring] sobre el cuerpo de
los reales. En particular, es un conjunto que se encuentra cerrado bajo estas
operaciones.

[^ring]: <https://en.wikipedia.org/wiki/Ring_(mathematics)#Definition>

Property rmk:sqnormofsum
: Sean $a, b \in \R^n$, tenemos que $\| a + b \| ^ 2 = \|a\|^2 + \|b\|^2 + 2 a^T b$.

Proof
: Desarrollemos:
\begin{align}
\| a + b \| ^ 2 &= (a_1 + b_1)^2 + \dots + (a_n + b_n)^2 \\
&= (a_1^2 + b_1^2 + 2 a_1 b_1) + ... + (a_n^2 + b_n^2 + 2 a_n b_n) \\
&= \| a \| ^2 + \| b \|^2 + 2 \langle a, b \rangle \\
&= \| a \| ^2 + \| b \|^2 + 2 a^T b
\end{align}

#### Representación de rotaciones

Para las rotaciones, y orientaciones, existen múltiples representaciones
válidas, cada una con sus ventajas y desventajas. Veremos algunas que han sido
utilizadas en este trabajo.

##### Ángulos Euler

La representación por ángulos Euler utiliza un vector $[x, y, z]^T \in \R^3$ en donde
cada componente representa el ángulo de rotación que aplicar alrededor de tres
ejes seleccionados por convención. Es decir, el vector describe tres rotaciones
que aplicar. Esta representación tiene la principal ventaja de resultar
intuitiva cuando solo se necesita describir una rotación, pero se vuelve
inconveniente en otros contextos que necesitaremos.

<!-- #define MN_ROTATION_MADNESS %\
En la práctica, la manipulación de rotaciones y sistemas de coordenadas son
fuentes usuales de muchos dolores de cabeza. Usualmente producto del uso
no documentado de distintas convenciones.
-->

Uno de sus problemas es que existen docenas de convenciones válidas que varían
en: la elección de los tres ejes, orden de los mismos, aplicación global o local
en cada uno. Aunque en la práctica solo se utiliza un puñado de ellas, se puede
volver fácilmente un punto de confusión\marginnote{MN_ROTATION_MADNESS}. El otro
problema fundamental es el llamado _gimbal lock_[^gimbal-lock] en donde la
combinación de ciertas rotaciones puede causar la pérdida de un grado de
libertad y describir nuevas rotaciones arbitrarias se hace imposible a partir de
ese punto. Otros problemas de los ángulos Euler se detallan en
@shoemakeAnimatingRotationQuaternion1985.

En general, evitaremos esta representación.

[^gimbal-lock]: <https://en.wikipedia.org/wiki/Gimbal_lock>

##### Ángulo axial

Toda rotación puede representarse con un ángulo $\omega$ y un eje axial,
representado por un vector unitario $a \in \R^3$, sobre el cual rotar $\omega$ radianes.
La representación de ángulo axial de esta rotación queda definida por el vector
$v = \omega a$. Tenemos entonces que $a = \frac{v}{\| v \|}$ y $\omega = \|
v\|$.

Esta representación surge naturalmente del uso de giroscopios. Estos módulos,
internamente se componen de tres sensores capaces de reportar cada uno la
velocidad angular sobre un eje y se los ubica sobre tres ejes ortogonales. De
esta forma, la velocidad que reportan queda determinada por la cantidad de
rotación que ocurrió en cada eje durante el instante de la muestra capturada. Si
se ven los valores de los tres sensores como componentes de un vector
tridimensional, este coincide con la representación angular axial $v$ de
la rotación capturada.

Esta representación se utilizará para el almacenamiento de valores de velocidad
angular provistos por muestras de giroscopio, ya que no es necesaria ningún tipo
de conversión. Además, veremos más abajo que esta forma de describir
rotaciones surge naturalmente en el estudio de otras representaciones.

<!-- TODO@ref: citar algo que verifique eso -->
<!-- TODO: Mencionar torque? -->

##### Cuaterniones unitarios

Los cuaterniones están definidos sobre un álgebra $\H$. Son una construcción que
extiende a $\R$ con tres números imaginarios $i$, $j$ y $k$ que satisfacen las
siguientes propiedades:
\begin{align}
i^2 = j^2 = k^2 = -1 \label{eq:quat-imaginary-props-start} \\
i = jk, \quad -i = kj \\
k = ij, \quad -k = ji \\
j = ki, \quad -j = ik \label{eq:quat-imaginary-props-end}
\end{align}

Un cuaternión $q \in \H$ tiene la forma
\begin{align}
q = q_w + q_x i + q_y j + q_z k \quad \text{con }\  q_w, q_x, q_y, q_z \in \R
\end{align}

El producto y la adición se extienden de $\R$ naturalmente incluyendo las
propiedades de las partes imaginarias listadas en
\Crefrange{eq:quat-imaginary-props-start}{eq:quat-imaginary-props-end}

Nos interesarán tres operadores de los cuaterniones:

\bigbreak

- Conjugado: $q^* = q_w - (q_x i + q_y j + q_z k)$

- Norma: $\| q \| = \sqrt{q_w ^2 + q_x^2 + q_y^2 + q_z^2} = \sqrt{qq^*}$

- Inverso: $q^{-1} = \frac{q^*}{\|q\|^2}$

\bigbreak

Representaremos rotaciones y orientaciones con **cuaterniones unitarios**, es decir
cuaterniones $q$ tal que $\| q \| = 1$. Más aún cualquier cuaternión $q'$ puede
hacerse unitario dividiéndolo por su norma, o sea $q = q' / \|q'\|$ tiene
norma 1.

Una rotación representada en **ángulos axiales** por el vector unitario $a = [x, y,
z]^T$ y ángulo $\omega$ se representa con el siguiente cuaternión unitario $q$:
\begin{align}
q = cos\frac{\omega}{2} + x\ sin\frac{\omega}{2}\ i + y\ sin\frac{\omega}{2}\ j + z\ sin\frac{\omega}{2}\ k
\end{align}
Más aún, todo cuaternión unitario puede expresarse de esa forma.

Para **rotar un vector** $v = [x, y, z]^T \in \R^3$ con una rotación representada por
el cuaternión $q$ basta con definir el cuaternión $p = 0 + xi + yj + zk$ y
computar $p'$ de la siguiente manera:
\begin{align}
p' = qpq^{-1} = 0 + p'_x i + p'_y j + p'_z k
\end{align}

El cuaternión resultante $p'$ tendrá parte real nula y el vector $v' = [p'_x,
p'_y, p'_z]^T \in \R^3$ es el vector $v$ rotado por $q$.

La **composición de rotaciones** queda bien definida por la multiplicación de
cuaterniones. Es decir, dados los cuaterniones $q$ y $p$, el cuaternión $pq$
describe la rotación que se produce al aplicar primero $q$ y luego $p$.

La **rotación identidad** o neutra, una rotación que "no rota", coincide con $1
\in \R$, es decir no tiene parte imaginaria, es $1 + 0i + 0j + 0k$.

El **inverso multiplicativo** de un cuaternión $q^{-1}$ al
componerlo con $q$, como es de esperarse, produce la identidad, o sea:
\begin{align}
q^{-1}q = 1
\end{align}

Muchas veces necesitaremos computar el **delta de rotación** que lleva de una
orientación $p$ a otra $q$. Esto es similar a lo que obtenemos cuando restamos
vectores, así que sobrecargaremos el operador de resta de cuaterniones según el
contexto de la siguiente manera:
\begin{align}
q - p = p^{-1} q
\end{align}

<!-- TODO@high$def: menciono $lerp$ -->

Será también útil poder interpolar entre dos orientaciones $p$ y $q$ con un
factor $t \in [0, 1]$ para conseguir orientaciones intermedias de $p$ a $q$. La
interpolación lineal $lerp$ genera cuaterniones no unitarios, y por esto
utilizaremos en su lugar la operación de **interpolación esférica** $slerp$
presentada en @shoemakeAnimatingRotationQuaternion1985 y definida de la siguiente
manera:
\begin{align}
slerp(p, q, t) = p(p^{-1}q)^t
\end{align}

[^slerp-derivation]: La derivación de la fórmula de interpolación esférica para
cuaterniones se puede encontrar en @shoemakeAnimatingRotationQuaternion1985

##### Matrices de rotación {#sec:rotation-matrices}

Las rotaciones pueden representarse también como una matriz $R \in \R^{3x3}$ con
ciertas restricciones.

Definition
: Sean $v, w \in \R^3$, decimos que $v$ y $w$ son ortonormales si $\norm{v} =
\norm{w} = 1$ y son ortogonales, es decir $\dotprod{v}{w} = 0$

Sean $R^{(1)}, R^{(2)}, R^{(3)} \in \R^3$ las columnas de $R$.

Definition
: $R$ se dice ortogonal u ortonormal si sus columnas son ortonormales de a pares, es decir,
$\dotprod{R^{(i)}}{R^{(j)}} = 0$ y $\norm{R^{(i)}} = 1$ para $i \neq j; \; i, j \in \{1, 2, 3\}$.

<!-- #define MN_DETERMINANT_INTUITION %\
El hecho de que el determinante sea $+1$, intuitivamente, quiere decir que la
transformación lineal de $R$ no escala los vectores en $\R^3$,
o sea preserva volúmenes.
-->

<!-- #define MN_IMPROPER_ROTATION %\
Las transformaciones representadas por $R$ con $det(R) = -1$ suelen llamarse
rotaciones impropias o rotorreflexiones ya que además de rotar, permiten la reflexión
de vectores en $\R^3$.
-->

Las matrices ortonormales pueden tener determinante $\pm 1$. Llamaremos **matrices de
rotación** solo a las $R$ tal que $det(R) = +1$
\marginnote{MN_DETERMINANT_INTUITION} \marginnote{MN_IMPROPER_ROTATION}. El
conjunto  estas matrices se denomina $SO(3)$ y veremos en la sección siguiente
el por qué de este nombre. Estas matrices presentan propiedades agradables para ser manipuladas como rotaciones
en el álgebra matricial usual:

\bigbreak

- $R$ es la transformación lineal que rota vectores $v \in \R^3$, es decir $Rv$
  es el vector $v$ rotado por la rotación representada en $R$.

- La composición de rotaciones $R, S \in SO(3)$ queda representada con la
  multiplicación de matrices usual $RS$.

- La inversa de $R$ es $R^{-1} = R^T$, más aún esta propiedad define a las
  matrices ortogonales.

\bigbreak

Proof
: Tenemos por la ortonormalidad de las columnas de $R$ y definición de $R^T$ que
\begin{align}
  & R^T R = I_{3 \times 3} \\
  & \Leftrightarrow \begin{bmatrix}
  \dotprod{R^{(1)}}{R^{(1)}} & \dotprod{R^{(1)}}{R^{(2)}} & \dotprod{R^{(1)}}{R^{(3)}} \\
  \dotprod{R^{(2)}}{R^{(1)}} & \dotprod{R^{(2)}}{R^{(2)}} & \dotprod{R^{(2)}}{R^{(3)}} \\
  \dotprod{R^{(3)}}{R^{(1)}} & \dotprod{R^{(3)}}{R^{(2)}} & \dotprod{R^{(3)}}{R^{(3)}} \\
  \end{bmatrix} = \begin{bmatrix}
    1 & 0 & 0 \\
    0 & 1 & 0 \\
    0 & 0 & 1 \\
  \end{bmatrix} \\
  & \Leftrightarrow \| R^{(i)} \| = 1 \text{ y } \dotprod{R^{(i)}}{R^{(j)}} = 0 \quad \forall i \neq j \in \{1,2,3\} \\
  & \Leftrightarrow \text{R es ortogonal}
\end{align}

\bigbreak

#### Representación de transformaciones

Tener rotaciones expresadas como matrices, o equivalentemente como
transformaciones lineales, prueba ser muy útil en la práctica, ya que podemos
recurrir al arsenal de funcionalidad preexistente para estas estructuras.
A continuación, desarrollaremos una serie de definiciones que nos permitirán
extender esta idea de utilizar matrices para cubrir el concepto de
transformación en su totalidad, con traslaciones incluidas.

##### Grupos

Vimos en la \Cref{sec:linearalg-prelim} que $\Rnn$ forma un anillo con
multiplicación y suma cerradas bajo $\R$. Además, mostramos que las matrices en
$\Rnn$ corresponden a transformaciones lineales. Veremos ahora una serie de
entidades que restringen a las transformaciones en $\Rnn$ con el objetivo de
llegar a describir las transformaciones de cuerpo rígido sobre $\R^3$ que nos
interesan.

Definition
: Un grupo es un conjunto $G$ con una operación binaria \newline
$\circ : G \times G \rightarrow
G$ tal que $\forall a, b, c \in G$:
\bigbreak
\begin{enumerate}
  \item Es cerrada: $a \circ b \in G$
  \item Es asociativa: $(a \circ b) \circ c = a \circ (b \circ c)$
  \item Tiene neutro: $\exists!\ e \in G: e \circ a = a \circ e = a$
  \item Tiene inverso: $\exists a^{-1} \in G: a \circ a^{-1} = a^{-1} \circ a = e$
\end{enumerate}

Es posible empezar a intuir que _tanto las rotaciones como las transformaciones_
que describimos al principio del capítulo _coinciden con esta idea de grupo_.
"Mezclar" transformaciones debería dar como resultado otra transformación
(cerrada) y no debería importar el orden de mezcla (asociativa). Debería existir
una transformación neutra que no haga nada, y una transformación inversa que
deshagan la transformación original. Si además pudiésemos describir estas
transformaciones con matrices, seríamos capaces de recurrir a todas las
herramientas preexistentes. Veamos como hacer eso ahora.

Definition
: El conjunto de matrices invertibles en $\Rnn$ con la operación de
multiplicación matricial forman un grupo denominado Grupo Lineal General
$GL(n)$. Es decir:
\begin{align}
  GL(n) = \{ A \in \Rnn : det(A) \neq 0 \}
\end{align}

Definition
: El subconjunto de matrices de GL(n) con determinante 1 se denomina el Grupo
Linea Especial $SL(n)$. Es decir:
\begin{align}
  SL(n) = \{ A \in GL(n) : det(A) = 1 \}
\end{align}

Remark
: $A \in SL(n) \Rightarrow A^{-1} \in SL(n)$ ya que $det(A^{-1}) = \frac{1}{det(A)}$.

Definition
: Un grupo $G$ tiene una representación matricial si existe un homomorfismo
inyectivo $F:G \rightarrow GL(n)$. Es decir, una función inyectiva
para la cual la multiplicación matricial preserva la estructura del operador
$\circ$. En símbolos, $\forall a, b \in G$:
\begin{align}
  F(e) &= I_{n \times n} \\
  F(a \circ b) &= F(a)F(b)
\end{align}

Definition
: El subconjunto de matrices ortogonales de $GL(n)$ se denomina el Grupo Ortogonal
$O(n)$. Es decir:
\begin{align}
O(n) = \{ R \in GL(n) : R^T R = I \}
\end{align}

Property
: Una matriz ortogonal $R \in \Rnn$ preserva el producto interno.

Proof
: $\forall x, y \in \R^{n}$ tenemos:
\begin{align}
\dotprod{Rx}{Ry} = (Rx)^T Ry = x^T R^T R y = x^T y = \dotprod{x}{y}
\end{align}

Property
: Una matriz ortogonal $R \in O(n)$ tiene $det(R) = \pm 1$

Proof
: \begin{align}
& 1 = det(I) = det(R^T R) = det(R^T) det(R) = det(R)^2 \\
& \Leftrightarrow det(R) = \pm 1
\end{align}

Definition
: El subconjunto de matrices ortogonales de $O(n)$ con determinante $+1$ se
denomina el Grupo Ortogonal Especial $SO(n)$. Es decir:
\begin{align}
  SO(n) = \{ R \in O(n) : det(R) = +1 \} = O(n) \cap SL(n)
\end{align}

Como vimos en la \Cref{sec:rotation-matrices}, este grupo es el que define a
las **matrices de rotación**. Y se corresponde a la representación matricial que
presentamos allí. Continuemos ahora con las transformaciones.

##### Transformaciones como grupos

Definition
: Uns transformación lineal afín $L : \R^n \rightarrow \R^n$ es tal que existe $B
\in GL(n)$ y $b \in \R^n$ que determinan $L(x) = Bx + b$.

Definition
: El grupo de tales transformaciones se denomina Grupo Afín de dimensión $n$
$A(n)$.

En general, una transformación afín $L(x) = Bx + b \in A(n)$ no es una transformación lineal a menos
que $b = 0$. Introduciremos las llamadas _coordenadas homogéneas_ para expresar
transformaciones afínes en $A(n)$ como transformaciones lineales en $GL(n + 1)$.
Extenderemos $L$ de la siguiente manera:
\begin{align}
L': \R^{n+1} &\rightarrow \R^{n+1} \\
L' \begin{pmatrix}\begin{bmatrix}x \\ 1\end{bmatrix}\end{pmatrix} &= \begin{bmatrix}
B & b \\
0 & 1
\end{bmatrix}
\begin{bmatrix}x \\ 1\end{bmatrix}
= \begin{bmatrix} Bx + b \\ 1 \end{bmatrix}
= \begin{bmatrix} L(x) \\ 1 \end{bmatrix}
\end{align}

Notar que hay un isomorfismo entre $L$ y $L'$ ya que $0$ y $1$ son constantes y
por esto diremos que son la misma transformación. La matriz $\begin{bmatrix} B &
b \\ 0 & 1 \end{bmatrix}$ se dice una matriz afín y pertenece a $GL(n + 1)$.
Tenemos entonces que las matrices afines forman un subgrupo de $GL(n + 1)$

Definition
: Una transformación euclídea $L: \R^n \rightarrow \R^n$ se define con una
matriz ortogonal $R \in O(n)$ y un vector $t \in \R^n$ como $L(x) = Rx + t$.

Definition
: El grupo de tales transformaciones se denomina Grupo Euclídeo $E(n)$ y es un
subgrupo de $A(n)$. Es decir
\begin{align}
  E(n) = \begin{Bmatrix} \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix} \in
  \R^{(n+1) \times (n+1)} : R \in O(n), t \in \R^n \end{Bmatrix}
\end{align}

Definition
: El subconjunto de transformaciones euclídeas con $R \in SO(n)$ se denomina el
Grupo Euclídeo Especial $SE(n)$, es decir:
\begin{align}
  E(n) = \begin{Bmatrix} \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix} \in
  \R^{(n+1) \times (n+1)} : R \in SO(n), t \in \R^n  \end{Bmatrix}
\end{align}

Y es este el grupo que buscábamos ya que $SE(3)$ es capaz de representar las
transformaciones de cuerpo rígido en $\R^3$ que necesitábamos. Tenemos entonces
que representaremos rotaciones con matrices cuadradas $3x3$ $R \in SO(3)$ y
representaremos transformaciones con matrices cuadradas $4x4$ $T \in SE(3)$.
Estos grupos también funcionan con dos dimensiones en $\R^2$ de la misma manera
para $SO(2)$ y $SE(2)$. Finalmente, se pueden visualizar los conjuntos definidos
en esta sección en la \figref{fig:hasse-groups}.

\fig{fig:hasse-groups}{source/figures/hasse-groups.pdf}{Árbol de grupos}{%
Diagramas de Hasse de los grupos desarrollados con el orden parcial
$\subset$ (\italic{``es subconjunto propio de''}).
}


<!-- #if 0 -->

-------------

1. Linear transforms and operators (skew symetric, cross product)
2. Rotation representations: euler, axis/angle, quaternion, 3x3 intro
3. Groups
4. Exponential coordinates
  1. Infinitesimal approximation
  2. Mention Lie group/algebra (dont dive)
  3. Exponential Map / Logarithm (and mention of rodrigues formula)
  4. Same for SE(3): twist, exp, log, hat, vee
  5. Pro: unconstrained optimization!!!!!!!

<!-- TODO@high: aclarar que dependiendo del contexto vamos a interpretar rotaciones y orientaciones con la representacion adecuada -->

#### Operadores útiles

Definición: Producto punto
Observación: producto punto es x^t x (mover lo que está en least squares acá referenciarlo allá)
Definición: Producto cruz
Definición: Hat operator

#### Transformaciones lineales

Definición: Transformación lineal

#### Transformaciones lineales y operadores

#### Representraciones de rotaciones
hat operator aca?

#### Grupos

#### Coordenadas exponenciales

Groups:

- General Linear Group: GL(n) = {invertible mats, @} = {A / det(A) != 0}
- Special Linear Group: SL(n) = {A in GL(n) / det(A) = 1}
- Orthogonal Group: O(n) = R orthogonal in M(n) = { R in M(n)/ RtR=I} (=> det(R) = +-1)
- Special Orthogonal Group: SO(n) = {R in O(n) / det(R) = +1} (rotation matrices)
- Affine Group: A(n) = L:Rn->Rn / L(x) = Ax + b con A in GL(n), b in Rn
- Euclidean Group: E(n) = L:Rn->Rn / L(x) = Rx + T con R in O(n), T in Rn
- Special Euclidean Group: SE(n) = {L(x) = Rx + T in E(n) / R in SO(n)}

GL(n) in M(n)
SL(n) in GL(n)
SO(n) in SL(n)
SO(n) in O(n)
A(n) in GL(n + 1)
E(n) in A(n)
SE(n) in E(n) with R(n) in SO(n)


- citar https://ethaneade.com/lie_groups.pdf (o https://ethaneade.com/lie.pdf)
- citar multiple view geometry zisserman
- citar state estimation barfoot
<!-- #endif -->
