## Controladores en Monado

En Monado, la interacción con la gran variedad de dispositivos que el runtime
soporta es realizada mediante _drivers_ o _controladores_. Estos, como se puede
ver en la \figref{fig:slam-tracker-dataflow}, le permiten a Monado interactuar con
sistemas XR físicos mediante abstracciones derivadas de los requisitos de
OpenXR. Un sistema XR en este contexto hace referencia a un conjunto de
dispositivos XR. Un dispositivo XR en forma intuitiva, es algún tipo de hardware
que permite la entrada o salida de información con simulaciones de XR. Un caso
paradigmático de un sistema XR podría considerarse el conjunto de casco y un par
de mandos provistos por un fabricante.

El concepto que se termina implementando en Monado es un poco más general, ya
que además de sistemas físicos, soporta sistemas simulados que proveen distintas
funcionalidades, como la capacidad de conectar dispositivos de forma remota,
emulación de dispositivos con teclado y ratón (o mediante otros dispositivos que
puedan ser de más fácil acceso como placas Arduino). En este trabajo se
diferenció el concepto de _fuente de datos_ del de dispositivo ya que es en
definitiva esto en lo que estaremos interesados para SLAM, obtener fuentes de
datos de IMU y cámaras.

\fig{fig:devices-ody-d455}{source/figures/devices-ody-d455.jpg}{Dispositivos XR utilizados}{%
Dispositivos XR utilizados en este trabajo. A izquierda un casco Samsung
Odyssey+ y a derecha una cámara Intel RealSense D455.
}

<!-- TODO@def: no defino que es SDK, o bindings -->
<!-- TODO@def: uso el termino seis grados de libertad -->
<!-- TODO@def: uso upstream -->

En este trabajo se desarrolló con los dos dispositivos mostrados en la
\figref{fig:devices-ody-d455} como principales fuentes de datos para SLAM. A la derecha
de la imagen tenemos una cámara de profundidad _Intel RealSense D455_[^d455]
mientras que a izquierda tenemos un casco _Samsung Odyssey+_. La línea de
cámaras y módulos RealSense de Intel se enfoca en aplicaciones de robótica y
visión por computadora, presentan distintos modelos con múltiples sensores
especializados (en nuestro caso nos limitaremos a utilizar su IMU y cámaras
estéreo). Estos vienen precalibrados, y además se tiene un SDK[^realsense-sdk]
de código abierto en C/C++ (con _bindings_ para otros lenguajes) que facilita la
obtención y manipulación de datos. En contraste con esto, el casco de Samsung es
un casco ligado a la plataforma privativa _Windows Mixed Reality (WMR)_[^wmr]
que solo funciona en sistemas operativos Windows. WMR incluye algoritmos
propietarios de tracking por SLAM desarrollados por Microsoft.

Mientras que la cámara D455 funcionó como un dispositivo sumamente versátil para
el prototipado y experimentación con sistemas de SLAM, el Odyssey+ presenta
serios desafíos que requirieron trabajo con la comunidad e ingeniería inversa
para poder tener acceso a las fuentes de datos necesarias para el tracking por
SLAM. Cabe aclarar, que anterior a este trabajo, y según mi mejor entendimiento,
no existía forma de utilizar este tipo de cascos con tracking con seis grados
para correr aplicaciones OpenXR sobre sistemas operativos basados en GNU/Linux
[^wmr-novelty] [^quest-android].

[^d455]: https://www.intelrealsense.com/depth-camera-d455/
[^odysseyplus]: https://www.samsung.com/us/support/computing/hmd/hmd-odyssey/hmd-odyssey-plus-mixed-reality/
[^realsense-sdk]: https://github.com/IntelRealSense/librealsense
[^wmr]: https://www.microsoft.com/en-us/mixed-reality/windows-mixed-reality

[^wmr-novelty]: A pesar de que aún queda mucho por hacer para que el tracking
presentado en este trabajo llegue a niveles de calidad comparables a la versión
privativa de WMR, la contribución presentada deja asentada en upstream una
infraestructura sobre la que extender y mejorar el ecosistema de VR para
GNU/Linux.

[^quest-android]: Cuando hablamos de GNU/Linux nos referimos a sistemas
operativos enfocados a computadoras personales como Ubuntu o Manjaro.
Técnicamente, los dispositivos autónomos Oculus Quest de Meta (y otros), corren
sobre sistemas operativos basados en Android, que a su vez está basado en
GNU/Linux.

### Consideraciones

Lo primero que se necesita para poder utilizar estos dispositivos para SLAM es
conseguir el acceso a los datos que estos generan; o sea los flujos de imágenes
y muestras de IMU. La forma y protocolos necesarios para comunicarse con estos
dispositivos se realiza de maneras específicas para cada uno veremos en las
secciones dedicadas, y este es uno de los trabajos fundamentales de un
controlador. Además, un controlador tiene que ser capaz, no solo de obtener esta
información sino que también de redirigirla a los módulos adecuados de Monado.
En la implementación de estas ideas surge naturalmente una idea de fuentes y
sumideros de datos. En el runtime, estos conceptos existían pero de forma
específica para imágenes, y fueron extendidos para el manejo de muestras de IMU.
Los dispositivos entonces funcionan como fuentes de datos, que instancian un
`TrackerSlam` el cual les provee sumideros a los que redirigir sus muestras de
IMU e imágenes.

A la hora de implementar un controlador para una familia de dispositivos
enfocado a SLAM, hay una serie de cuestiones a tener en cuenta. Desde el punto
de vista de sistemas de SLAM/VIO, lo único que nos interesa es un flujo adecuado
de imágenes de cámaras y muestras de IMU. Es en la definición de adecuado en
donde se esconden varios detalles importantes.

<!-- TODO: referenciar sección de calibración de IMU si la hago -->
<!-- TODO: referenciar sección de calibración de cámara si la hago -->
<!-- TODO@def: uso calibración "intrínseca" y "extrínseca" -->

En primer lugar, es necesario acceder a la información de calibración, tanto
intrínseca como extrínseca, de los dispositivos en cuestión, para poder
comunicársela de alguna forma a los sistemas de SLAM. Esto incluye la
calibración para los cuatro sensores usuales: giroscopio, acelerómetro y el par
de cámaras estéreo. A pesar de ser conveniente recalibrar estos sistemas, ya que
sus parámetros van modificandose con el tiempo, es usual que los fabricantes
proveean alguna forma de acceder a parámetros para ciertos modelos de
calibración y preferiremos usar estos para facilitarle la experiencia al usuario
que no tendrá que calibrar sus dispositivos. Es vital que losk sistemas de SLAM
soporten estos modelos, de lo contrario se necesitarán correcciones que
usualmente terminan siendo mucho más costosas que si los sistemas hubieran
soportado los modelos nativamente. Ejemplos de esto son la
desdistorsión[^opencv-undistort] y rectificación[^opencv-stereorectify] de
imágenes sobre la cual no nos explayaremos aquí, pero basta con entender que es
una transformación aplicada a todos los píxeles de las imágenes para
"normalizarla" de forma tal que a los sistemas se les facilite su utilización.

[^opencv-stereorectify]: Documentación de `cv::stereoRectify`:
https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html#ga617b1685d4059c6040827800e72ad2b6

[^opencv-undistort]: Documentación de `cv::initUndistortRectifyMap`:
https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a

Otro problema escencial que debe solucionarse es el de la sincronización de
timestamps. Cualquier dispositivo que quiera utilizarse para SLAM, debería tener
las muestras de todos sus sensores sincronizadas por hardware. Es decir, con
timestamps que reflejen lo más precisamente posible los tiempos internos en los
que las muestras se tomaron. Siguiendo con esta línea de problemas de marcas de
tiempo, se necesita sincronizar de alguna manera los relojes del dispositivo con
los del host para poder dar sentido a las estimaciones que los sistemas de SLAM
realizarán cuando una aplicación OpenXR solicite la predicción de una pose a un
tiempo dado.

Entrando a problemas que afectan a sensores específicos, todos los sistemas de
SLAM estudiados esperan datos de IMU que combinen en una única timestamp los
valores del acelerómetro y los del giroscopio. De lo contrario será necesario
realizar algún tipo de transformación sobre las muestras para simular esta
condición. Por el lado de los sensores de la cámara, será importante que el
obturador o _shutter_[^shutter] de las cámaras sea un _global shutter_, es decir
que todos los píxeles sean capturados en el mismo instante. Por el contrario,
las cámaras que se utilizan habitualmente en dispositivos de consumo como
teléfonos inteligentes, presentan un _rolling shutter_ en dónde los píxeles son
capturados en un "barrido", fila por fila. Esto genera
distorsiones[^rolling-shutter-name] significativas en presencia de movimientos
suficientemente rápidos como se ve en la \figref{fig:rolling-shutter}. Estas
distorsiones afectan negativamente la capacidad de los algoritmos de SLAM para
reconocer y trackear features de forma estable.

\fig{fig:rolling-shutter}{source/figures/rolling-shutter.jpg}{Efecto rolling shutter}{%
Ejemplo de la distorsión que se genera en cámaras con rolling shutter que
capturan la imagen barriendo por filas de píxeles. Esto genera distorsiones en
los objetos rígidos que son particularmente notables en presencia de movimientos
de alta velocidad como los de la hélice. Esto no sucede con cámaras con global
shutter que capturan todos los píxeles en el mismo momento.
}

[^shutter]: El término obturador proviene de los sensores ópticos tradicionales.
Un obturador era una pieza mecánica en movimiento que controlaba el tiempo
durante el cual la película fotográfica era expuesta a la luz de la escena.
Actualmente el proceso de control de exposición se realiza con interruptores
en los sensores ópticos.

[^rolling-shutter-name]: Esta distorsión es homónima al tipo de cámara y se
denomina el efecto de rolling shutter.

Otro aspecto muy importante a la hora de presentar muestras de imágenes a
sistemas de SLAM es el de utilizar valores adecuados de _exposición (exposure)_
y _ganancia (gain)_. La exposición o exposure es la cantidad de tiempo que el
obturador de la cámara habilita la entrada de luz a los sensores ópticos por
cada cuadro. Por otro lado, la ganancia controla el nivel de amplificación
(usualmente digital) que ocurrirá sobre la señal original.

Además de las problemáticas presentadas en la \figref{fig:expgain-grids}, existen
otros problemas a considerar relacionados también a estos parámetros y la
iluminación del entorno del usuario. Uno de ellos es la _sobreexposición_,
cuando se presentan fuentes de iluminación muy intensas y la exposición (y
también la ganancia) se encuentra en valores relativamente altos, los sensores
ópticos son saturados y se pierde información. Esto se puede observar levemente
en la imagen de la figura con mayor valor de exposición y ganancia. La
problemática opuesta es cuando el usuario no posee suficiente cantidad de luz en
su entorno y entonces el sistema de SLAM no es capaz de distinguir features. Una
regla de pulgar

\fig{fig:expgain-grids}{source/figures/expgain-grids.pdf}{Exposición y ganancia}{%
Ejemplos tomados con la D455 sobre los efectos de la exposición y ganancia sobre
las muestras de imágenes. A izquierda se observa una región de 256 píxeles
cuadrados con distintas configuraciones de tiempos de exposición y valores de
ganancia. En esta región se encuentra un objeto en movimiento (el cuaderno con
cuadrados). A derecha tenemos otra región más pequeña de 32 píxeles cuadrados
provenientes de las mismas imágenes. Se puede observar en ambas grillas que
aumentar ambos valores también incrementa el brillo de la imagen. Por su parte
en la figura derecha podemos ver que aumentar la ganancia incrementa el ruido,
mientras que en la figura izquierda se observa que valores altos de exposición
incrementan el motion blur del objeto en movimiento.
}

<!-- #if 0 -->

HABLAR DEL PROBLEMA DE FLICKER, hablar de AUTOEXPOSURE
Datasets TUM-VI, EuRoC?
quizás todo esto debería estar mencionado en una sección de datasets en la parte
de fundamentos ?

TODO: terminar de mencionar las caracteristicas que falta acá,
despues describirlas rápidamente en la seccion de realsense
despues hablar de lo que me interese de WMR
despues describir las caracteristica srapidamente tambien en la seccion de WMR
y finalmente presentar una tabla comparativa (o capaz eso hacerlo antes?)

-------------------------------

-[x]imu/frame sinks
-[x]communication con OpenXR app y TrackerSlam
-[]pose correction: per system


-[x]que son las camaras realsense
-[x]por que esta bueno tener estas camaras y por que las use
-[x]variedad de dispositivos, rs_ddev, t265

-[x]lib: realsense api
-stream options: multiple (configured through json)
-[x]camera calibration: precalibrated
-[x]imu calibration: precalibrated
-[x]imu stream detail: accel/gyro stream merge
-[x]clock sync: global timestamp automatically managed
-[x]clock sync: hardware timestamps synced
-exposure-gain-auto: can use auto exposure from realsense sdk, sensorquality<->exposure
-[x]shutter: global
-frame management: realsense sdk threads, thread queues, ¿rs_frame/xrt_frame/cv::Mat?
-UI: screenshot?

<!-- TODO: tabla para comparar estas características de los dispositivos? -->
<!-- #endif -->

### RealSense

<!-- TODO@def: "host", lo uso acá y en otros lados -->
<!-- TODO@def: DIY -->

Para soportar la cámara D455, se extendió significativamente en Monado el
controlador de dispositivos RealSense. Hasta el momento, la única cámara de esta
línea soportadas por Monado era la T265[^t265]. Esta cámara es curiosa ya que
presenta un algoritmo de SLAM privativo que corre dentro del dispositivo sin
interacción del host. Este controlador se encargaba únicamente de inicializar el
módulo interno de SLAM de la cámara y obtener las poses computadas por la misma
para uso en las aplicacions OpenXR. Uno de sus usuarios clave era el casco libre
del proyecto North Star [^north-star] que la utiliza como principal forma de
tracking; en la \figref{fig:northstar-t265}.jpg se puede ver uno de estos cascos
con la cámara sujeta al mismo en la parte superior.

\fig{fig:northstar-t265}{source/figures/northstar-t265.jpg}{T265 y proyecto North Star}{%
El casco AR libre del proyecto North Star con una camara T265 sujeta en la parte superior.
}


[^t265]: https://www.intelrealsense.com/tracking-camera-t265/

[^north-star]: El proyecto North Star de UltraLeap (prev. LeapMotion) es un
casco AR "DIY" que puede fabricarse con piezas impresas en 3D y la compra de
algunos componentes. https://developer.leapmotion.com/northstar

Al no haber ningún tipo de manejo de las imágenes o muestras de IMU provistas
por la cámara, se tuvo que implementar la gestión de estos sensores. Es ahora
posible utilizar cualquier cámara de la línea RealSense que posea un par de
cámaras estéreo y una IMU. Como trabajo futuro, sería interesante comparar el
tracking interno de una T265 con los distintos sistemas externos integrados en
este trabajo.

### Windows Mixed Reality
