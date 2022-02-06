<!-- #### Predicción de poses -->

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

\fig{fig:prediction-timeline}{source/figures/prediction-timeline.png}{Línea de tiempo de predicción}{%
Línea de tiempo con timestamps normalizadas. Las barras representan las
siguientes duraciones:
\mono{REQUEST\_TO\_PREDICTION}: Del momento en que una predicción es solicitada hasta la timestamp de la predicción.
\mono{SHOT\_TO\_RECEIVED}: Captura de imagen en el dispositivo hasta su recepción en Monado.
\mono{RECEIVED\_TO\_PUSHED}: Transferencia de Monado a Basalt.
\mono{PUSHED\_TO\_PROCESSED}: Cómputo de la estimación de pose.
}

En la \figref{fig:prediction-timeline} se puede apreciar una captura de pantalla
de la interfaz de *Perfetto*[^perfetto-web] que, en conjunto con *Percetto*[^percetto-web],
son herramientas de medición de tiempos preferidas para Monado.
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
un cable USB 3.2 con una demora de unos 13,5 ms representada por la barra
`SHOT_TO_RECEIVED`. En ese momento ocurre una pequeña copia de Monado hacia
Basalt `RECEIVED_TO_PUSHED`\marginnote{Esta copia es necesaria por un detalle en la
implementación del \mono{slam\_tracker} para Basalt. Si bien es solucionable,
como se ve en el gráfico, no afecta significativamente al rendimiento del
pipeline}, y luego de unos 12 ms representados por
`PUSHED_TO_PROCESSED`, a tiempo `[F]`, la pose estimada para el tiempo `[A]`
está computada. Es decir, tenemos una demora de unos 25,5 ms desde que la
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
Notar que en ese punto, todavía faltan 25,5 ms para tener la predicción de
Basalt para `[A]`, más aún, una predicción dada por Basalt para el futuro
`[B]` ni siquiera existirá, ya que el sistema solo estima poses para los tiempos
de las muestras, es decir la próxima estimación correspondería al tiempo `[G]`.
Además de esto, tenemos que mientras todavía se está procesando la muestra, otra
petición a tiempo `[D]` para `[E]` debe ser respondida.

En conclusión, tenemos un **desfasaje temporal** que hace que las poses
estimadas siempre estén levemente en el pasado; en el tramo seleccionado fue de
25,5ms (más los 7 ms de predicción), pero es variable durante la corrida.
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

<!-- TODO@ref: la cita del autor "khronos group inc" se ve muy rara -->

[^openxr-time-limits]: La especificación de OpenXR tiene una sección dedicada a
las restricciones y condiciones a los que el runtime está sujeto respecto a
solicitudes en el pasado y en el futuro por parte del usuario. Ver
[@thekhronosgroupinc.OpenXRSpecification], secc. 2.14.

Sería razonable, como primera aproximación a nuestro problema, utilizar este
historial de espacios. Esto nos garantiza que podamos proveerle al usuario una
pose para cualquier punto arbitrario en el tiempo que solicite, basándonos en
las estimaciones del sistema de SLAM que asumimos son precisas. Sin embargo, un
leve problema que surge es que no existe ningún requerimiento para los sistemas
sobre la estimación de velocidades, ya que no todos estiman esta variable. La
interfaz `slam_tracker` solo garantizan la estimación de la posición y
orientación del dispositivo como puede verse en su definición en el
\Cref{lst:slam-tracker-def}. Lo que haremos para solventar esto es computar las
velocidades con base a los pares de poses adyacentes que tengamos en el
historial. Estas poses tienen su timestamp correspondiente, entonces es sencillo
computar la diferencia entre las mismas respecto a la unidad de tiempo, dando
como resultado una estimación de la velocidad del espacio. La
\figref{fig:prediction-with-space-history} muestra como funcionaría este tipo de
predicción en un ejemplo simplificado en 2D y en el que asumimos que las poses
estimadas por el sistema de SLAM/VIO coinciden perfectamente con la trayectoria
real del dispositivo.

\fig{fig:prediction-with-space-history}{source/figures/prediction-with-space-history.pdf}{Predicción con historial de espacios}{%
Ejemplo de predicción con el historial de espacios. Se asume que las poses
estimadas por el sistema de SLAM son perfectas por simplicidad.
}

\FloatBarrier

<!-- TODO@def: Estoy caminando alrededor del tema de los cuaterniones muy fuerte. -->

Esto es una buena primera solución al problema, y es la opción más básica que la
clase adaptadora `TrackerSlam` le ofrece a los usuarios de Monado.
Desafortunadamente, si vemos el ejemplo estudiado en la
\figref{fig:prediction-timeline} notaremos que la frecuencia de poses que se computan es
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
estudiado en la \figref{fig:prediction-timeline}. Además, a pesar de sufrir de
severos problemas de drift, al utilizarlas en ventanas cortas de tiempo (unos
pocos milisegundos), estos se ven reducidos en gran medida y la odometría que
sus sensores proveen resulta suficientemente precisa.

La clase adaptadora tiene acceso a estas muestras, ya que las intercepta para
redirigirlas hacia los sistemas de SLAM. Utilizaremos un concepto similar al de
la pre-integración de muestras de IMU explorado en la \Cref{basalt-preintegration}
con algunas ideas relacionadas con las ecuaciones presentadas a partir de la
\cref{eq:imu-preintegration}. Consideremos que no vamos
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

``` {#lst:predict-pose .cpp caption="Predicción de poses en Monado" emph="timestamp"}
struct xrt_space_relation predict_pose(timestamp t) {
   if (relation_history.is_empty()) return {0};

   // Espacio más reciente estimado con SLAM/VIO
   struct xrt_space_relation r = relation_history.get_latest();
   timestamp rt = timestamp_of(r);

   // Variables configuradas por el usuario en tiempo de ejecución
   bool pred_on = /* predicción habilitada por usuario? */
   bool gyro_on = /* giroscopio habilitado por usuario? */
   bool acc_on = /* acelerómetro habilitado por usuario? */
   bool imu_on = gyro_on or acc_on;

   // Flujo condicional de la predicción según la configuración
   if (pred_on) return r;
   if (!imu_on or t <= rt) relation_history.predict(t);
   if (gyro_on) {
      vec3 avg_gyro = gyro_average_between(rt, t);
      vec3 world_gyro = rotate_angular_velocity(r.orientation, avg_gyro);
      r.angular_velocity = world_gyro;
   }
   if (acc_on) {
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

Mostramos en la \figref{fig:prediction-with-imu} un ejemplo simplificado del
algoritmo implementado utilizando esta idea de promediar muestras de odometría
de la IMU para predecir puntos de tiempo posteriores a `B` cuando `C` todavía no
pertenece al historial de espacios. En el ejemplo se muestra como iría
actualizándose el vector promediado (en verde) al integrar las tres muestras (en
azul) que ocurren entre $t=1$ y $t=2$. Además, se muestra como estos vectores
promedios se utilizan para extrapolar linealmente para los tiempos requeridos
por un usuario $t \in \{1,45; 1,75; 1,95\}$ (en anaranjado). Por simplicidad, el
ejemplo asume que tanto las muestras de odometría de la IMU a tiempos $t \in
\{1,3; 1,6; 1,9\}$ como las estimaciones `B` y `C` coinciden perfectamente con
la trayectoria real del dispositivo.

<!-- TODO@end: estaríá bueno que ambas figuras aparezcan en la misma página -->

\fig{fig:prediction-with-imu}{source/figures/prediction-with-imu.pdf}{Predicción con promediado de muestras IMU}{%
Ejemplo de predicción para tiempos $t \in \{1,45; 1,75; 1,95\}$ utilizando la
idea de promediar muestras de la IMU posteriores a la pose más reciente del
historial (\mono{B} en este caso, se considera que \mono{C} no pertenece al historial
aún). Se asume que las poses estimadas por el sistema de SLAM y las muestras de
la IMU son perfectas por simplicidad.
}

Para contrastar esto con el caso en el que se ignoran las muestras de la IMU y
solo se utiliza el historial de poses, se muestra en la
\figref{fig:prediction-without-imu} los errores de esta predicción para el mismo
escenario.

\fig{fig:prediction-without-imu}{source/figures/prediction-without-imu.pdf}{Predicción sin uso de muestras IMU}{%
Ejemplo de predicción para tiempos $t \in \{1,45; 1,75; 1,95\}$ ignorando las
muestras de IMU y utilizando unicamente el historial de poses con \mono{A} y \mono{B} como
últimas muestras (esto es antes de que llegue \mono{C}). De vuelta, asumimos que las
estimaciones y no contienen error por simplicidad.
}

Finalmente, cabe aclarar que la trayectoria presentada en estas figuras es
particularmente desafiante. Considerando que estos dispositivos XR están
usualmente sujetos a partes como la cabeza o las manos del usuario, es
improbable encontrar trayectorias demasiado abruptas entre los tiempos de
estimación de las poses de SLAM. Estos, al coincidir con la frecuencia de
muestreo de las cámaras, suelen ser menores a 50ms (p.ej. a 30 cuadros por
segundo, tenemos ~33ms entre pose y pose). Por otro lado, es usual tener una
mayor cantidad de muestras de IMU entre estimaciones y no solo las 3 que se
muestran en las figuras (p.ej. a 30 cuadros por segundo con la IMU a 250 hz,
tenemos unas ~8 muestras de IMU entre cada par de cuadros consecutivos), lo cual
mejora la precisión de la predicción aún más.
