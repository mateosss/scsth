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
No profundizaremos en la definición formal de este concepto, pero intuitivamente,
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

Vale la pena aclarar que desarrollaremos una teoría suficientemente genérica
como para aplicar en $n = 2$ y $n = 3$ dimensiones. En el caso bidimensional
basta con tres variables independientes, también llamadas grados de libertad o
_degrees of freedom (DoF)_, para describir completamente una transformación:
dos para la traslación y uno para la rotación. Por otro lado, en el caso
tridimensional se necesitarán seis grados de libertad: tres y tres. Veremos al
final de la sección que terminaremos usando representaciones sobre-determinadas,
con más de tres o seis variables, ya que nos facilitarán su manipulación.

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
: Si $V \subseteq \R^n$ tiene base canónica $e_1, ..., e_n$ con $e_i \in \R^m$
tenemos que la matriz $A = [L(e_1), ..., L(e_n)] \in \R^{m \times n}$ cumple
$Ax = L(x) \quad \forall x \in V$

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

La **rotación identidad** o neutra, una rotación que “no rota”, coincide con $1
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

<!-- TODO@def: menciono $lerp$ -->

Será también útil poder interpolar entre dos orientaciones $p$ y $q$ con un
factor $t \in [0, 1]$ para conseguir orientaciones intermedias de $p$ a $q$. La
interpolación lineal $lerp$ genera cuaterniones no unitarios, y por esto
utilizaremos en su lugar la operación de **interpolación esférica** $slerp$
presentada en @shoemakeAnimatingRotationQuaternion1985 y definida de la siguiente
manera:
\begin{align}
slerp(p, q, t) = p(p^{-1}q)^t \label{eq:slerp-def}
\end{align}

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
rotaciones impropias o rotorreflexiones, ya que además de rotar, permiten la reflexión
de vectores en $\R^3$.
-->

Las matrices ortonormales pueden tener determinante $\pm 1$. Llamaremos **matrices de
rotación** solo a las $R$ tal que $det(R) = +1$
\marginnote{MN_DETERMINANT_INTUITION} \marginnote{MN_IMPROPER_ROTATION}. El
conjunto de estas matrices se denomina $SO(3)$ y veremos en la sección siguiente
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
“Mezclar” transformaciones debería dar como resultado otra transformación
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
Lineal Especial $SL(n)$. Es decir:
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
: Una transformación lineal afín $L : \R^n \rightarrow \R^n$ es tal que existe $B
\in GL(n)$ y $b \in \R^n$ que determinan $L(x) = Bx + b$.

Definition
: El grupo de tales transformaciones se denomina Grupo Afín de dimensión $n$
$A(n)$.

En general, una transformación afín $L(x) = Bx + b \in A(n)$ no es una transformación lineal a menos
que $b = 0$. Introduciremos las llamadas _coordenadas homogéneas_ para expresar
transformaciones afines en $A(n)$ como transformaciones lineales en $GL(n + 1)$.
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
Notar que hay un isomorfismo entre $L$ y $L'$, ya que $0$ y $1$ son constantes y
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

Y es este el grupo que buscábamos, ya que $SE(3)$ es capaz de representar las
transformaciones de cuerpo rígido en $\R^3$ que necesitábamos. Tenemos entonces
que representaremos rotaciones con $R \in SO(3)$, osea matrices cuadradas $3 \times 3$; y
representaremos transformaciones con $T \in SE(3)$, osea matrices cuadradas $4 \times 4$.
Estos grupos también funcionan con dos dimensiones en $\R^2$ de la misma manera
para $SO(2)$ y $SE(2)$. Finalmente, se pueden visualizar los conjuntos definidos
en esta sección en la \figref{fig:hasse-groups}.

\fig{fig:hasse-groups}{source/figures/hasse-groups.pdf}{Árbol de grupos}{%
Diagramas de Hasse de los grupos desarrollados con el orden parcial
$\subset$ (\italic{``es subconjunto propio de''}).
}

#### Representación de infinitesimales

Ahora nos gustaría entender como tratar cambios infinitesimales en las
rotaciones de $SO(3)$ y las transformaciones de $SE(3)$. Esto será necesario a
la hora de aplicar algoritmos de optimización que dependen de las derivadas de
estas operaciones.

##### Matrices antisimétricas

Definition (Producto cruz)
: Dados $v, w \in \R^3$ el producto cruz de $v$ y $w$ es un vector ortogonal a
ambos tal que:
\begin{align}
v \times w = \begin{bmatrix}
v_y w_z - v_z w_y \\
v_z w_x - v_x w_z \\
v_x w_y - v_y w_x
\end{bmatrix} \in \R^3
\end{align}

Definition (Matriz antismétrica)
: $R \in \RR3$ se dice antisimétrica si $R = -R^T$

Definition
: Definimos el operador $\hat{\cdot} : \R^3 \rightarrow \RR3$ que devuelve la
siguiente matriz antisimétrica:
\begin{align}
\hat{v} = \begin{bmatrix}
0 & -v_z & v_y \\
v_z & 0 & -v_x \\
-v_y & v_x & 0
\end{bmatrix} \in \RR3
\end{align}

La construcción del operador $\hat{v}$ está diseñada para tener la siguiente
propiedad:

Property
: $\hat{v} w = v \times w$

Además, por la definición de matriz antisimétrica es sencillo ver que:

Property prop:skew-mat-vec
: Toda matriz antisimétrica $R$ está unívocamente definida por un vector $v \in
\R^3$ tal que $R = \hat{v}$

Definition
: El conjunto de todas las matrices antisimétricas en $\R^3$ se denomina Álgebra
de Lie Ortogonal Especial $\so3$,
es decir:
\begin{align}
\so3 = \{ \hat{v} \in \RR3 : v \in \R^3 \}
\end{align}

Veremos a continuación cuál es su relación con $SO(3)$ y el por qué de su nombre.

##### Rotaciones infinitesimales

Consideremos una familia de rotaciones $R(t) \in SO(3)$ con $t \in \R$ que describen
una rotación continua aplicada sobre un punto $X(0) \in \R^3$ hacia otro $X(t)$,
es decir:
\begin{align}
  R(0) = I \\
  X(t) = R(t)X(0)
\end{align}

Notation
: El parámetro $t$ lo consideraremos implícito en algunas ocasiones, o sea
$R = R(t)$. Además, utilizaremos la notación $\dot{R} = \frac{dR}{dt}$.

Como $RR^T = I$ tenemos que
\begin{align}
& 0 = \frac{d}{dt}I = \frac{d}{dt}(RR^T) = \dot{R}R^T + R \dot{R}^T \\
& \Rightarrow \dot{R}R^T = -R \dot{R}^T
\end{align}
O sea que $\dot{R}R^T \in \so3$. Por la \Cref{prop:skew-mat-vec} tenemos que
existe un vector único $v(t) \in \R^3$ tal que
\begin{align}
\dot{R}(t) R(t)^T = \hat{v}(t) \Leftrightarrow \dot{R}(t) = \hat{v}(t) R(t)
\end{align}
Y como $R(0) = I$, entonces $\dot{R}(0) = \hat{v}(0)$. Por lo tanto, tenemos que
la matriz antisimétrica $\hat{v}(0)$ nos da la aproximacíon de primer orden de una rotación:
\begin{align}
R(dt) = R(0) + (dR)(0) = I + \hat{v}(0)dt \label{eq:hatop-is-rotvel}
\end{align}
Notar que si pensamos a $t$ en términos de tiempo, la \Cref{eq:hatop-is-rotvel}
deja ver a $\hat{v}$ como una matriz que describe la velocidad de la rotación.

\clearpage
<!-- #define MN_LIE_GROUP %\
Un grupo de Lie es una ``variedad diferenciable'' en el cual la operación del grupo,
y su inversa, también son diferenciables. Intuitivamente, esto significa que la
aplicación de rotaciones o transformaciones es ``suave'' o continua y esto nos
permite trabajar con el concepto de límite y derivadas.
-->

<!-- TODO@high@end: La ultima vez que vi este margin note se iba tanto de la pagina que no aparecia ni cortado, revisarlo -->
<!-- #define MN_LIE_ALGEBRA %\
Un grupo de Lie tiene un álgebra de Lie relacionada. Esta última es el
``espacio tangente'' en la identidad $I$ del grupo (en particular, de la variedad).
Intuitivamente, este puede pensarse como el espacio de todas las posibles
velocidades alrededor de $I$.
Esto es precisamente lo que desarrollamos al calcular $R(dt)$ en la \Cref{eq:hatop-is-rotvel}.
-->

Tenemos entonces que el efecto de una rotación infinitesimal en $SO(3)$ puede
ser aproximado por matrices en $\so3$. Es necesario mencionar que $SO(3)$ es lo
que se denomina un _grupo de Lie_ \marginnote{MN_LIE_GROUP} mientras que $\so3$
es su correspondiente _álgebra de Lie_ \marginnote{MN_LIE_ALGEBRA}. No
necesitaremos adentrarnos en estos conceptos, pero es común encontrarlos en la
literatura y gran parte del desarrollo que estamos realizando está ligado a
ellos.

Luego de haber presentado estas ideas fundamentales, a partir de aquí
procederemos a dar una _vista general_ de la definición de dos operadores, $exp$
y $log$ que nos permiten pasar del grupo al álgebra de Lie y viceversa. Más
adelante, también veremos rápidamente como estos conceptos se traducen de forma
muy similar para las transformaciones en $\R^3$. Al final del capítulo
listaremos algunas referencias para el lector que quiera profundizar en los
conceptos y las derivaciones.

\bigbreak

--------

\bigbreak

Vimos en el desarrollo anterior que existe un vector $\hat{v}(t) \in \so3$
que actúa como un término de velocidad rotacional. Si asumimos velocidad
constante, es decir $\hat{v}$ constante, nos interesaría saber cual es la
rotación total luego de rotar desde $R(0) = I$ con esta velocidad
durante un tiempo $t$. En otras palabras, queremos computar $R(t)$ dado
$\hat{v}$. Teniendo en cuenta el desarrollo anterior basta con plantear el
siguiente sistema de ecuaciones diferenciales:
\begin{align} \begin{cases}
\dot{R}(t) = \hat{v} R(t) \\
R(0) = I
\end{cases}
\end{align}
Es posible ver que este sistema tiene como solución la siguiente expresión.
\begin{align}
R(t) = exp(\hat{v}t) = \sum_{n=0}^{\infty}\frac{(\hat{v}t)^n}{n!} \label{eq:exp-def}
\end{align}
Notar que los exponentes de la \Cref{eq:exp-def} son respecto a la multiplicación matricial.

Esta rotación se corresponde con, dado $w = v t \in \R^3$, la rotación de
$\omega = \norm{w}$ radianes alrededor del eje dado por el vector unitario $a =
w / \norm{w}$. Dicho de otro modo, _la representación ángulo-axial $w = \omega
a$ puede ser convertida en la matriz de rotación $R$ equivalente mediante el
operador $exp$ con $R = exp(\hat{w})$_. Más aún, $\so3$ contiene todos estos
vectores ángulo-axiales.

El operador $exp : \so3 \rightarrow SO(3)$ se denomina _mapa o aplicación exponencial_ y su inversa es el
_mapa logarítmico_ $log : SO(3) \rightarrow \so3$. Este, dado una matriz de
rotación $R \in SO(3)$ devuelve $\hat{w} \in \so3$ tal que $R = exp(\hat{w})$
computando $w$ de la siguiente manera [@eadeDerivativeExponentialMap]:
\begin{align}
  \norm{w} = cos^{-1} \left( \frac{traza(R) - 1}{2} \right) \label{eq:log-def-start}\\
  w = \frac{\norm{w}}{2sin(\norm{w})} \begin{bmatrix} R_{3,2} - R_{2,3} \\
  R_{1,3} - R_{3,1} \\ R_{2,1} - R_{1,2} \end{bmatrix} \label{eq:log-def-end}
\end{align}
Notar que definimos $exp$ en la \Cref{eq:exp-def} como una suma infinita
mientras que $log$ pudo definirse con una expresión cerrada en las
\Crefrange{eq:log-def-start}{eq:log-def-end}. Existe la _fórmula de Rodrigues_
que permite expresar también $exp$ de forma cerrada:
\begin{align}
exp(\hat{w}) = I + \frac{sin(\norm{w})}{\norm{w}} \hat{w} + \frac{1 - cos(\norm{w})}{\norm{w}^2} \hat{w}^2
\end{align}

##### Transformaciones infinitesimales

Para las transformaciones en $SE(3)$ tenemos un desarrollo muy similar al de las
rotaciones en $SO(3)$. Consideremos una familia de transformaciones $T(t) \in
SE(3)$ compuestas por rotaciones $R(t) \in SO(3)$ y traslaciones $b(t) \in
\R^3$ con $t \in \R$ que representan una transformación continua aplicada al punto $X(0)
\in \R^3$ con $T(0) = I$. Es decir,
\begin{align}
X(t) &= T(t)X(0) \\
T(t) &= \begin{bmatrix}
R(t) & b(t) \\
0 & 1
\end{bmatrix}
\end{align}
Considerando que esta vez la inversa de $T$ es $T^{-1}$ y no su transpuesta como era el caso con las
rotaciones. Podemos aplicar un desarrollo similar al de la sección anterior
y llegar a que:
\begin{align} \label{eq:translation-deriv}
\dot{T}T^{-1} = \begin{bmatrix}
\dot{R}R^T & \dot{b} - \dot{R} R^T b \\
0 & 0
\end{bmatrix} \in \RR4
\end{align}
De vuelta, $\dot{R}R^T$ corresponde a alguna matriz antisimétrica $\hat{v} \in
\so3$. Definiendo un vector $y(t) = \dot{b}(t) - \hat{v}(t) b(t)$ podemos
reescribir la \Cref{eq:translation-deriv} e introducir el concepto de _giro o twist_ $\hat{\xi}(t)$:
\begin{align}
\hat{\xi}(t) = \dot{T}(t)T^{-1}(t) = \begin{bmatrix}
\hat{v}(t) & y(t) \\
0 & 0
\end{bmatrix}
\end{align}
La matriz de giro $\hat{\xi}$ pertenece al álgebra de Lie $\se3$ del grupo de Lie $SE(3)$ y
puede ser parametrizada por las coordenadas de giro $\xi \in \R^6$. Para esto se utiliza un operador
_hat_ $\cdot^{\wedge}$ y su inversa _vee_ $\cdot^{\vee}$ de la siguiente manera:
\begin{align}
\hat{\xi} &= {\begin{bmatrix}y \\ v\end{bmatrix}}^{\wedge} = \begin{bmatrix}\hat{v} &
y \\ 0 & 0 \end{bmatrix} \in \RR4 \\
{\begin{bmatrix}\hat{v} & y \\ 0 & 0 \end{bmatrix}}^{\vee} &= \begin{bmatrix}y \\
v\end{bmatrix} = \xi \in \R^6
\end{align}
Es decir, podemos codificar el cambio infinitesimal de una transformación en un
vector de giro $\xi$ de seis dimensiones en donde:
\bigbreak

- Los últimos tres componentes dados por $v$ son la representación **ángulo-axial**
  de la velocidad rotacional.

- Los primeros tres componentes dados por $y$ describen el cambio de traslación
  teniendo en cuenta esta velocidad rotacional instantánea $\hat{v}$.

\bigbreak

Finalmente, tenemos el mapa exponencial y mapa logarítmico entre $SE(3)$ y
$\se3$. Similar a $SO(3)$, cualquier transformación $T \in SE(3)$ va a poder ser
representada por un vector de giro $\xi$ con $T = exp(\hat{\xi})$.

Existen expresiones cerradas para ambos $exp : \se3 \rightarrow SE(3)$ y $log :
SE(3) \rightarrow \se3$.

Para $exp(\hat{\xi})$ con $\xi = [y, v]^T$ tenemos:
\begin{align}
exp(\hat{\xi}) = \begin{bmatrix}
exp(\hat{v}) & Jy \\
0 & 1
\end{bmatrix}
\end{align}
Con $J$ el llamado _jacobiano izquierdo_ de $SO(3)$ que se puede computar con el ángulo
$\omega$ de $v$, es decir con $\omega = \norm{v}$ de esta manera [@eadeDerivativeExponentialMap]:
\begin{align}
J = I + \frac{1-cos(\omega)}{\omega^2} \hat{v} + \frac{\omega -
sin(\omega)}{\omega^3} \hat{v}^2.
\end{align}
Para $log(T)$ con $T = \begin{bmatrix}R & b \\ 0 & 1\end{bmatrix}\in SE(3)$ tenemos:
\begin{align}
log(T) = \begin{bmatrix}log(R)^{\vee} \\ J^{-1}b\end{bmatrix}^{\wedge}
\end{align}
Con el jacobiano inverso $J^{-1}$ dado por [@eadeDerivativeExponentialMap]:
\begin{align}
J^{-1} = I - \frac{1}{2} \hat{v} +
\left( \frac{1}{\omega^2} - \frac{1 + cos(\omega)}{2 \omega sin(\omega)} \right) \hat{v}^2
\end{align}

##### Cierre y literatura recomendada

<!-- #define MN_UNCONSTRAINED_OPTIMIZATION %\
Representaciones de cuaterniones o matriciales requieren mantener los errores
numéricos a raya mediante la constante renormalización de sus valores.
Las representaciones dadas en las álgebras de Lie no tienen este problema.
-->

Tenemos ahora una mirada suficientemente formal como para ser capaces de
utilizar y comprender las herramientas usualmente utilizadas en sistemas que
modelan rotaciones y transformaciones en dos y tres dimensiones por computadora.
Nos tomamos el trabajo de entender varias formalizaciones para las rotaciones, ya
que todas ellas aparecen de una u otra forma en el pipeline que se desarrolla en
este trabajo. Las formalizaciones infinitesimales que hemos presentado en la
última subsección, y sus representaciones en el álgebra de Lie, permiten además
modelar los estados de las entidades que un algoritmo de SLAM necesita describir
de una forma particularmente elegante. Esto es así porque permiten la aplicación
de algoritmos de optimización, como los que veremos en el próximo capítulo, _sin
restricciones_\marginnote{MN_UNCONSTRAINED_OPTIMIZATION}.

Respecto a la última sección de infinitesimales, se pueden encontrar algunos de
estos conceptos explorados en mayor profundidad en
@barfootStateEstimationRobotics2017 cap. 7. Una excelente introducción a los
grupos de Lie con una teoría reducida enfocada en aplicaciones de robótica es
presentada en @solaMicroLieTheory2021. Finalmente, gran parte de las
derivaciones de las expresiones que se vieron se encuentran detalladas en
@eadeDerivativeExponentialMap.
