<!-- #### Filtrado de poses -->

Continuando con la descripción de la funcionalidad presente en la clase
adaptadora `TrackerSlam` y luego de haber presentado el método de predicción que
se emplea en Monado, veremos ahora la siguiente funcionalidad que `TrackerSlam`
implementa: el **filtrado** de poses.

También llamado _smoothing_, alisado o suavizado, el filtro de señales, curvas
o, en este caso poses, es una forma de minimizar o _filtrar_ el ruido presente
en alguna fuente de información y suavizar los cambios abruptos en las poses.
Lo que sucede en nuestro caso es que por la naturaleza del problema en cuestión
y por algunas de las decisiones tomadas, se pueden notar la presencia de micro
movimientos de alta frecuencia que existen en la trayectoria estimada. Estas
alteraciones no son más que ruido proveniente de distintos factores.

<!-- TODO@def: uso ATE,APE,AOE, RTE,RPE,ROE y loop closure -->

Por un lado, los sistemas de SLAM/VIO en el área no necesariamente priorizan el
caso de uso de XR y suelen estar mayormente interesados en aplicaciones de
robótica. En este campo, la “sensación” que produciría el tracking no es un
factor de importancia comparado a la precisión absoluta del mismo. En
particular, las métricas más utilizadas en estos trabajos son las que evalúan el
error absoluto de la trayectoria en su totalidad (ATE, APE, AOE). Es intuitivo
ver que estas métricas, a diferencias de sus versiones relativas (RTE, RPE,
ROE), incentivan correcciones abruptas en la trayectoria cuando los sistemas
determinan que su pose actual no es la mejor posible (p. ej. en momentos de loop
closure). Más aún, minimizar el ruido en la trayectoria no es uno de sus
objetivos, ya que la aplicación artificial de filtros que suavicen la
trayectoria podría tender a empeorar el puntaje obtenido en estos conjuntos de
datos. Todo esto hace que muchas veces las trayectorias computadas por los
sistemas en condiciones no óptimas tiendan a presentar una gran cantidad de
movimientos bruscos. Estos pueden resultar particularmente notables en sistemas
VR en dónde las pantallas ocupan todo el campo de visión del usuario;
movimientos de este tipo pueden fácilmente inducir cinetosis.

Por sobre esto, el método de predicción presentado en la sección anterior en la
\figref{fig:prediction-with-imu} presenta problemas que no fueron tratados. En
particular, la predicción que realizamos está basada en una única pose del
sistema SLAM y las muestras nueva de la IMU, pero no comparte ningún otro estado
en común. Entonces podría esperarse que la diferencia entre las poses que se
fueron prediciendo con la nueva pose que el sistema estimará sea significativa.
Más aún, en la realidad el error acumulado por la IMU, a pesar de verse limitado
a un intervalo corto de unas decenas de milisegundos, es un término más que
afectaría esta diferencia. Todo esto puede verse en el error marcado en la
\figref{fig:prediction-offset-jump}. Este tipo de desfasaje sería reintroducido
de forma repetitiva afectando las predicciones cada vez que una nueva pose es
estimada, causando así constantes micro saltos (ruido), especialmente en los
momentos en los que la pose estimada por SLAM y la pose predicha por nuestro
método difieran significativamente.

\fig{fig:prediction-offset-jump}{source/figures/prediction-offset-jump.pdf}{Predicción sin uso de muestras IMU}{%
Desfasaje esperado entre el método de predicción por muestras promediadas y la
pose \mono{C} estimada de SLAM cuando \mono{C} aún no pertenece al historial de espacios.
Se muestra la incidencia de la acumulación de errores de la IMU. Este desfasaje
causará micro saltos que serían disruptivos en una experiencia de VR.
}

Es entonces por estas razones, que se implementaron tres métodos sencillos de
filtrado combinables para suavizar las trayectorias estimadas y que intentan
minimizar los problemas expuestos. Se deja como trabajo futuro el uso de filtros
más elaborados como los filtros Kalman [@welchSCAATIncrementalTracking1997, ap.
B]. Cabe aclarar que en general, el uso de filtros también presenta una
desventaja fundamental. Esta es, la introducción de latencia artificial al
sistema, ya que para poder suavizar este ruido, los filtros tienden a reducir
cambios abruptos en la trayectoria, incluso cuando estos sean realmente los
movimientos que el usuario realizó físicamente.

Presentaremos tres filtros, con el más sofisticado basado en
@casiezFilterSimpleSpeedbased2012. Además, dicho trabajo cubre el resto de
filtros presentados, muestra gráficas comparativas, y es también una buena
lectura para contextualizar el uso de filtros para tracking de movimientos
humanos. Los filtros presentados aquí y en el trabajo mencionado pueden
visualizarse interactivamente en la siguiente aplicación web:
<https://cristal.univ-lille.fr/~casiez/1euro/InteractiveDemo/>.

El funcionamiento esquemático de un filtro es muy sencillo: es un contenedor de
**estado**, con un método de **actualización** que recibe un nuevo **dato** con
una **timestamp** posterior a las provistas hasta el momento; con esto, el
filtro computa el valor de la **señal filtrada** para una timestamp requerida.
En nuestro caso, esta timestamp coincidirá con la del dato de entrada. En
Monado, ubicaremos el filtro al final del pipeline de `TrackerSlam`, justo antes
de devolverle la pose a la aplicación OpenXR, es decir luego de haber pasado por
el procedimiento de predicción. Los filtros habilitados interceptan la pose con
sus métodos de actualización respectivos y devuelven en su lugar una nueva pose
filtrada con la misma timestamp. Los tres filtros se encuentran uno detrás del
otro y son combinables.

Expresado más formalmente, lo que tendremos es un conjunto de poses $X_0, ...,
X_k \in \R^7$ que ocurren a tiempos $t_0 < ... < t_k$ respectivamente. Para $i =
0, ..., k$ definimos $X_i = (p_i, q_i)$ con $p_i \in \R^3$ definido por los
primeros tres componentes de $X_i$ para representar la posición, mientras que
definimos el cuaternión $q_i$ para representar la orientación con coeficientes
dados por los últimos cuatro componentes. Tenemos además las versiones filtradas
de las poses anteriores $\hat{X}_0, ..., \hat{X}_{k - 1}$ y querremos ahora
computar la versión filtrada de la pose actual $\hat{X}_k$.

##### Media móvil

El primer filtro es una _media móvil_. El estado de este filtro consiste de un
historial de poses de los últimos $m$ segundos. El método de actualización
registra la pose de entrada y su timestamp en este historial interno. Para
computar la pose de salida en esa timestamp, se toma el promedio de las poses de
los últimos $w < m$ segundos (por defecto 66 ms). El parámetro $w$ es
configurable por el usuario.

Cabe aclarar, que si bien la forma de calcular el promedio para las posiciones
$p_i$ debería resultar clara, promediar las orientaciones $q_i$ expresadas
mediante cuaterniones no es trivial. En este caso, nos aprovecharemos del hecho
de que $w$ suele ser pequeño y por ende contiene orientaciones que no cambian
significativamente. Esto nos permite utilizar el resultado expuesto en
[@gramkowAveragingRotations2001] que muestra que, para rotaciones de menos de 40
grados, calcular la media usual (y posteriormente normalizarla) es una muy buena
aproximación con un error de menos del $1\%$.

Tenemos entonces que el filtro queda definido por la siguiente ecuación.
\begin{align}
\hat{X}_k &= \frac{1}{|W|} \sum_{i \in W}{X_i}
\quad \text{con} \\
W &= \{ i : t_k - w \leq t_i \leq t_k \} \quad \text{(ventana del filtro)}
\end{align}

Notar que podemos definir el concepto de sumatoria componente a componente en
$\R^7$ gracias a la aproximación de los cuaterniones mencionada anteriormente.

##### Suavizado exponencial

Este filtro codifica en un único valor los datos históricos e integra nuevos
datos con una intensidad dada por un _factor de suavizado_ $\alpha \in [0, 1]$
configurable por el usuario (0,1 por defecto). En el caso de tener un único
escalar $x_k$ que filtrar, el suavizado exponencial queda definido de esta
forma:
\begin{align}
\hat{x}_0 &= x_0 \\
\hat{x}_k &= \alpha x_k + (1 - \alpha) \hat{x}_{k-1} \label{eq:exp-smoothing-scalar}
\end{align}

Reformulemos la [Ecuación](#eq:exp-smoothing-scalar) de la siguiente manera:
\begin{align}
\hat{x}_k &= \alpha x_k + (1 - \alpha) \hat{x}_{k-1} \\
&= \alpha x_k + \hat{x}_{k-1} - \alpha \hat{x}_{k-1} \\
&= \hat{x}_{k-1} + \alpha (x_k - \hat{x}_{k-1})
\end{align}

Esto nos deja ver el paso de actualización del filtro como una interpolación
(lineal) de $\hat{x}_{k-1}$ hacia $x_k$ con paso $\alpha$. Utilizaremos esta
idea para interpolar esféricamente la orientación de $\hat{X}_k$. Tenemos
entonces que el paso de actualización para este filtro queda definido como:
\begin{align}
\hat{X}_k &= (\hat{p}_k, \hat{q}_k) \\
\hat{p}_k &= lerp(\hat{p}_{k-1}, p_k, \alpha) = \hat{p}_{k-1} + \alpha (p_k - \hat{p}_{k-1}) \\
\hat{q}_k &= slerp(\hat{q}_{k-1}, q_k, \alpha) = \hat{q}_{k-1}
(\hat{q}_{k-1}^{-1} q_k)^\alpha
\end{align}

<!-- TODO@def: uso lerp y slerp de pecho ahí, uso inversa, composición y exponenciación
escalar de los quaternions -->

##### Filtro 1€

El filtro 1€ [@casiezFilterSimpleSpeedbased2012] se basa en el
\hyperref[suavizado-exponencial]{suavizado exponencial}, pero utiliza un factor
$\alpha$ dinámico que se adapta automáticamente con base a la tasa de cambio de
la señal. Reusamos también la idea de interpolar esféricamente para la
orientación presentada en el filtro anterior. El filtro queda definido para la
posición $p_k$ de la siguiente manera:
\begin{align}
\hat{p}_0 &= p_0 \\
\hat{p}_k &= lerp(\hat{p}_{k-1}, p_k, \alpha)
\end{align}

Con $\alpha$ que se adapta con la velocidad de la señal:
\begin{align}
\alpha &= \frac{1}{1 + \frac{\tau}{\Delta t_k}} \\
\Delta t_k &= t_k - t_{k-1} \\
\tau &= \frac{1}{2 \pi f_C}
\end{align}

A continuación, $f_C$ es la llamada _frecuencia de corte_[^fc-lowpass] y posee
un mínimo ajustable por el usuario $f_{C_{min}}$ y un parámetro de intensidad de
actualización $\beta$ también configurable[^fc-perception].
\begin{align}
f_C &= f_{C_{min}} + \beta | \hat{\dot{p}}_k |
\end{align}

[^fc-lowpass]: Algunos lectores reconocerán que el término “frecuencia de corte”
proviene de los filtros _low-pass_ y efectivamente, notarán que el filtro 1€ es
de este tipo con la particularidad de tener una frecuencia de corte dinámica.

[^fc-perception]: Frecuencias de corte bajas reducen el ruido de las poses a
costa de aumentar la latencia. La forma en la que $f_c$ es definida resulta en
valores altos (y por ende con baja latencia) cuando se presentan cambios
significativos en las poses, mientras que para movimientos más suaves se reduce
$f_c$ para a su vez disminuir el ruido.

La velocidad de la señal es a su vez ajustada con otro filtro de suavizado
exponencial con factor de suavizado fijo $f_{C_d}$, también configurable por el
usuario.
\begin{align}
\hat{\dot{p}}_0 &= 0 \\
\hat{\dot{p}}_k &= lerp(\hat{\dot{p}}_{k-1}, \dot{p}_k, f_{C_d})
\end{align}

Con velocidades instantáneas.
\begin{align}
\dot{p}_0 &= 0 \\
\dot{p}_k &= \frac{p_k - \hat{p}_{k-1}}{\Delta t_k}
\end{align}

La versión del filtro utilizada para la orientación $q_k$ es análoga a la
definición anterior con algunas aclaraciones:

<!-- TODO@high@def: uso lerp acá, lo definí en algún lado? -->
\bigbreak

- En lugar de $lerp$ se utiliza $slerp$.

- Sobrecargamos el operador de resta de cuaterniones de la siguiente forma:
  $q_a - q_b = q_b^{-1} q_a$.

- La norma de un cuaternión es equivalente a la norma euclídea en $\R^4$, es
  decir $|q| = \sqrt{q_x^2 + q_y^2 + q_z^2 + q_w^2}$.

\bigbreak
