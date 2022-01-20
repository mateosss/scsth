<!-- TODO: Que es propioceptivo? -->
<!-- TODO: Que es odometría? -->
<!-- TODO: decidir si pongo las citas al final del archivo md o lo dejo así abajo el párrafo en donde se uso -->

# IMUs

## IMUs

<!-- PARAGRAPH: Que es un IMU -->

Una _unidad de medición inercial (IMU)_ es uno de los dispositivos que más
comúnmente se utilizan para medir los movimientos propioceptivos del agente a
localizar. Integran en un único paquete _acelerómetros_ para medir la
**aceleración lineal**, _giroscopios_ para la **velocidad angular**, y
opcionalmente _magnetómetros_. En este trabajo nos enfocaremos en el uso de
acelerómetros y giroscopios, ya que ninguno de los sistemas de localización
estudiados poseen la habilidad de integrar mediciones de magnetómetros. Ambos
sensores, acelerómetro y giroscopio, proveen una muestra por cada uno de los
tres ejes exponiendo un sistema con seis grados de libertad. Suelen funcionar a
altas frecuencias (p. ej. $200hz$) en comparación a las cámaras comúnmente
utilizadas para SLAM (p. ej. $20hz$). El funcionamiento y diseño específico de
estos sensores [@inertial-nav-intro-section3;@mems-imu] escapa al alcance de
este trabajo, pero es suficiente con aclarar que para este trabajo, tratamos con
sistemas microelectromecánicos (_MEMS_) de tamaño reducido y de bajo costo.

[@mems-imu]: Amita Gupta and Amir Ahmad. 2007. Microsensors based on MEMS technology. Defence Science Journal 57, (May 2007). DOI:https://doi.org/10.14429/dsj.57.1763

# Calibración y Modelado de Sensores Inerciales

A pesar de ser sumamente convenientes, las mediciones obtenidas por las IMU son
afectadas por múltiples problemas físicos que es necesario contrarrestar
aplicando distintos tipos de modelos correctivos.

## Calibración

Es común que los sensores tengan fallas estructurales de fábrica; errores que
afectan a las mediciones de manera constante. Es por esto que, de forma similar a lo
que ocurre con cualquier otro sensor sujeto a imperfecciones de fabricación, es
necesario aplicar correcciones a las mediciones directas (_raw_) provenientes
del sensor. Estas correcciones suelen basarse en modelos matemáticos con
parámetros relativamente estandarizados en la literatura, y la obtención de los
valores de estos parámetros para una IMU específica es a lo que denominamos
_calibración_. Los parámetros de calibración _intrínsecos (intrinsics)_ de una IMU que se utilizan más comúnmente conforman
una transformación lineal sobre la medición raw $m_r$ y modelan la corrección de
errores
de escala $S$, desalineación de los ejes $A$, y de offset $t$ constantes.
Se obtiene así una muestra calibrada $m_c$ de la siguiente forma:

$$
m_c =
\begin{bmatrix}
x_c \\
y_c \\
z_c
\end{bmatrix} =
\begin{bmatrix}
S_x & 0 & 0 \\
0 & S_y & 0 \\
0 & 0 & S_z
\end{bmatrix}
\begin{bmatrix}
1 & \alpha_1 & \alpha_2 \\
\alpha_3 & 1 & \alpha_4 \\
\alpha_5 & \alpha_6 & 1
\end{bmatrix}
\begin{bmatrix}
x_r \\
y_r \\
z_r
\end{bmatrix} +
\begin{bmatrix}
t_x \\
t_y \\
t_z
\end{bmatrix}=
S \ A \ m_r + t
$$

Cabe aclarar que este fue el modelo de calibración más utilizado,
pero existen otros aspectos que un modelo más preciso podría considerar. Suelen
existir **no-linearidades** en las imperfecciones que no son modeladas de forma
apropiada por una simple transformación lineal. Pueden existir correlaciones
entre las aceleraciones lineales y las mediciones del giroscopio, para estas
puede utilizarse la llamada **sensibilidad-g**. Proveer un **modelo de
temperatura** basándose en polinomios o tablas de valores es otra mejora que puede
resultar significativa en la práctica [@vectornav-imu-calib-charac].

[@vectornav-imu-calib-charac]: https://www.vectornav.com/resources/inertial-navigation-primer/specifications--and--error-budgets/specs-imucal

Además de los aspectos intrínsecos, cuando la IMU se considera en un conjunto de
más de un sensor, como es el caso de SLAM que también presenta cámaras, puede
tener sentido calibrar los parámetros _extrínsecos (extrinsics)_ que dan
la transformación de la IMU relativa a los otros sensores. Sin embargo, al ser
la IMU la principal fuente de odometría en SLAM, se suele utilizar como el punto
de origen del agente, su $(0, 0, 0)$, y es por esto que para este trabajo en
donde solo consideramos una IMU, no necesitaremos enfocarnos en estos valores.

El proceso de calibración va a variar según las herramientas utilizadas y el
grado de precisión deseado. Los fabricantes de IMU proveen extensivas fichas de
datos (_datasheets_) de sus distintos dispositivos con información específica
sobre la precisión y nivel de ruido esperable de sus sensores. Además, es común
que los parámetros de calibración intrínsecos específicos del dispositivo estén
almacenados en registros particulares del sensor y, en casos en donde el IMU
provee la posibilidad de aplicar las correcciones de calibración en el mismo
hardware, es usual que estos registros sean sobreescribibles. Por otro lado,
existen herramientas especializadas como _Kalibr_ o incluso la herramienta de
calibración contenida en _Basalt_, uno de los sistemas de SLAM estudiados, que
permiten calibrar los parámetros extrínsecos de sistemas con múltiples sensores.

<!-- TODO: Mencionar algo de TUM-VI en este parrafo? -->

## Modelado

<!-- TODO: Terminar esta sección -->

No solo es necesario compensar por las imperfecciones estructurales de
fabricación, sino que además las mediciones de las IMU son, en general, muy
ruidosas debido a las características físicas de estos sensores. El trabajo
realizado en [@inertial-nav-intro] muestra que el error acumulado sobre la
posición estimada o _drift_, luego de integrar durante 60 segundos una IMU particular es
mayor a 150 metros, similarmente [@vectornav-imu-ins-error-budget] muestra los
valores de drift esperados para distintas calidades de IMUs.

[@inertial-nav-intro]: Oliver J Woodman. An introduction to inertial navigation. 37.
noise/drift 150mt (pdf de cambridge)

[@inertial-nav-intro-section3]: Section 3 of [@inertial-nav-intro]

[@vectornav-imu-ins-error-budget]: https://www.vectornav.com/resources/inertial-navigation-primer/specifications--and--error-budgets/specs-inserrorbudget

[@ikf-attitude-estimation]: Nikolas Trawny and Stergios I Roumeliotis. Indirect Kalman Filter for 3D Attitude Estimation. 25.

---

Intentando ver como seusan los parametros de bias y noise inerciales. Ahora
estoy parado en (y creo que estoy por llegar a algun tipo de respuesta):

- Basalt paper: seccion IV-B-3
  - On-Manifold preintegartion paper: seccion V-A

[REFERENCIAR https://www.vectornav.com/resources/inertial-navigation-primer/]
ROBUSTES:
Es importante aclarar que un sistema de SLAM debería
ser lo suficientemente robusto como para funcionar, siempre y cuando los valores
sean razonables, bajo calibraciones subóptimas

AUTOCALIBRACION:
Idealmente, un sistema de SLAM debería ser capaz de auto-calibrar sus distintos
sensores durante la ejecución (_online calibration_) y, de hecho, existen sistemas capaces de
esto como lo son OpenVINS [REFERENCIAR] y [ALGUNOMAS?] [REFERENCIAR]. Estos
sistemas sin embargo no han sido estudiados en este trabajo debido, entre otras
cosas, a que ambos poseen licencias GPL [VER SECCION X DE POR QUE ESTO ES UN PROBLEMA].

Modelo noise: preintegración, jacobians

<!-- TODO: Revisar si luego de terminar con lo del odyssey no tengo algo más para decir de los modelos de temperatura -->
