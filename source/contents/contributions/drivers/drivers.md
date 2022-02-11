## Controladores en Monado

En Monado, la interacción con la gran variedad de dispositivos que el runtime
soporta es realizada mediante _drivers_ o _controladores_. Estos, como se mostró
en la \figref{fig:slam-tracker-dataflow}, le permiten a Monado interactuar con
sistemas XR físicos mediante abstracciones derivadas de los requisitos de
OpenXR. Un sistema XR en este contexto hace referencia a un conjunto de
dispositivos XR. Un dispositivo XR, en forma intuitiva, es algún tipo de hardware
que permite la entrada y/o salida de información para intercambio con aplicaciones de XR. Un caso
paradigmático de un sistema XR podría considerarse al conjunto de casco y un par
de mandos provistos por un fabricante.

El concepto que se termina implementando en Monado es un poco más general, ya
que además de sistemas físicos, soporta sistemas simulados que proveen distintas
funcionalidades. Entre estas se incluyen la capacidad de conectar dispositivos de forma remota,
emulación de dispositivos con teclado y ratón[^qwerty-mr] o mediante otros dispositivos como
placas Arduino[^arduino]. En este trabajo se
diferenció el concepto de _fuente de datos_ del de _dispositivo_ ya que es en
definitiva esto en lo que estaremos interesados para SLAM, obtener fuentes de
datos de IMU y cámaras.

[^qwerty-mr]: <https://gitlab.freedesktop.org/monado/monado/-/merge_requests/714>
[^arduino]: <https://www.arduino.cc/>

\fig{fig:devices-ody-d455}{source/figures/devices-ody-d455.jpg}{Dispositivos XR utilizados}{%
Dispositivos XR utilizados en este trabajo. A izquierda un casco Samsung
Odyssey+ y a derecha una cámara Intel RealSense D455.
}

<!-- TODO@def: no defino que es SDK, o bindings -->

Se utilizaron los dos dispositivos que se muestran en la
\figref{fig:devices-ody-d455} como principales fuentes de datos para SLAM. A la derecha
de la imagen tenemos una cámara de profundidad _Intel RealSense D455_[^d455]
mientras que a izquierda tenemos un casco _Samsung Odyssey+_. La línea de
cámaras y módulos RealSense de Intel se enfoca en aplicaciones de robótica y
visión por computadora, presentan distintos modelos con múltiples sensores
especializados; en nuestro caso nos limitaremos a utilizar su IMU y cámaras
estéreo. Estos vienen precalibrados, y además se tiene un SDK[^realsense-sdk]
de código abierto en C/C++, con _bindings_ para otros lenguajes, que facilita la
obtención y manipulación de datos. En contraste con esto, el casco de Samsung es
un casco ligado a la plataforma privativa _Windows Mixed Reality (WMR)_[^wmr]
que solo es soportada en sistemas operativos Windows[^windows]. WMR incluye algoritmos
propietarios de tracking por SLAM desarrollados por Microsoft.

[^windows]: <https://www.microsoft.com/en-us/windows/>
<!-- TODO@def: uso el termino seis grados de libertad -->
<!-- TODO@def: uso upstream -->

<!-- #define MN_WMR_NOVELTY %\
A pesar de que aún queda mucho por hacer para que el tracking
presentado llegue a niveles de calidad comparables a la versión
privativa de WMR, la contribución presentada deja asentada en upstream una
infraestructura sobre la que extender y mejorar el ecosistema de VR para
GNU/Linux.
-->

<!-- #define MN_QUEST_ANDROID %\
Cuando hablamos de GNU/Linux nos referimos a distribuciones
enfocadas a computadoras personales como Ubuntu o Manjaro.
Técnicamente, los dispositivos autónomos Oculus Quest de Meta (y otros), corren
sobre sistemas operativos basados en Android, que a su vez está basado en
GNU/Linux.
-->

Mientras que la cámara D455 funcionó como un dispositivo sumamente versátil para
el prototipado y experimentación con sistemas de SLAM, el Odyssey+ presenta
serios desafíos que requirieron trabajo con la comunidad y métodos de ingeniería inversa
para poder obtener acceso a las fuentes de datos necesarias para el tracking por
SLAM. Cabe aclarar, que anterior a este trabajo, y según mi mejor entendimiento,
no existía forma de utilizar este tipo de cascos con tracking basado en SLAM/VIO
para correr aplicaciones OpenXR sobre sistemas operativos basados en GNU/Linux
\marginnote{MN_WMR_NOVELTY} \marginnote{MN_QUEST_ANDROID}.

[^d455]: <https://www.intelrealsense.com/depth-camera-d455/>
[^odysseyplus]: <https://www.samsung.com/us/support/computing/hmd/hmd-odyssey/hmd-odyssey-plus-mixed-reality/>
[^realsense-sdk]: <https://github.com/IntelRealSense/librealsense>
[^wmr]: <https://www.microsoft.com/en-us/mixed-reality/windows-mixed-reality>

### Características de los datos

Lo primero que se necesita para poder utilizar estos dispositivos para SLAM es
conseguir el acceso a los datos que generan; o sea los flujos de imágenes
y muestras de IMU. La forma y protocolos necesarios para comunicarse con estos
dispositivos se realiza de maneras específicas para cada uno y como veremos en
las secciones dedicadas, este es uno de los trabajos fundamentales de un
controlador. Además, un controlador tiene que ser capaz, no solo de obtener esta
información sino que también de redirigirla a los módulos adecuados de Monado.
En la implementación de estas ideas surgen naturalmente los conceptos de
_fuentes (sources)_ y _sumideros (sinks)_ de datos. En el runtime, estos
conceptos existían exclusivamente para el tratado de imágenes, y fueron extendidos
para también soportar el flujo de muestras de IMU. Los dispositivos entonces funcionan como
fuentes de datos, que instancian un `TrackerSlam` el cual les provee sumideros a
los que redirigir las muestras de sus sensores.

A la hora de implementar un controlador para una familia de dispositivos
enfocado a SLAM, hay una serie de cuestiones a tener en cuenta. Desde el punto
de vista de sistemas de SLAM/VIO, lo único que nos interesa es un flujo adecuado
de imágenes de cámaras y muestras de IMU. Es en la definición de _adecuado_ en
donde se esconden varios detalles importantes. Intentaremos clarificar los
las características que deben considerarse en las muestras para que los sistemas
de SLAM puedan utilizarlas apropiadamente:

<!-- TODO@end: referenciar sección de calibración de IMU si la hago -->
<!-- TODO@end: referenciar sección de calibración de cámara si la hago -->
<!-- TODO@def: uso calibración -->

#### Calibración de parámetros intrínsecos

En primer lugar, es necesario acceder a la información de calibración de los
sensores en cuestión, para poder comunicársela de alguna forma a los sistemas de
SLAM. Esto incluye la calibración para los cuatro sensores usuales: giroscopio,
acelerómetro y el par de cámaras estéreo. La información de calibración describe
valores que toman los parámetros _intrínsecos_ (propios del sensor) de un modelo de calibración especificado. Es
usual que, para evitarle el proceso de calibración al usuario de los sensores,
estos provean valores de fábrica. La precisión de tales valores ha probado ser
de suficiente calidad para los sistemas de SLAM integrados en este trabajo, pero
es necesario aclarar que los valores reales irán cambiando con el tiempo y el
desgaste, haciendo que la recalibración sea un punto importante en el uso de
estos dispositivos. Monado provee algunas herramientas básicas de calibración
para unos pocos modelos de cámara, pero será necesario profundizar en este
aspecto como trabajo a futuro.

Habiendo dicho esto, vale aclarar que existen sistemas como OpenVINS
[@genevaOpenVINSResearchPlatform2020] que son capaces de realizar el proceso de
calibración de forma _online_ durante corridas normales. Esto es una
característica realmente importante que ninguno de los tres sistemas
integrados provee. Todos ellos asumen parámetros de calibración fijos que
deben ser provistos previos a la ejecución.

<!-- #define MN_MODEL_TRANSLATION %\
Mientras que en la práctica es conveniente recalibrar con modelos soportados,
podría resultar razonable estudiar expresiones analíticas que "traduzcan",
en alguna forma significativa, parámetros de un modelo a otro.
-->

Como intentamos evitarle la calibración manual al usuario, querremos ser capaces
de utilizar los valores de fábrica. Para esto es vital que los
sistemas de SLAM soporten los mismos modelos de calibración para los que el
fabricante especificó los valores\marginnote{MN_MODEL_TRANSLATION}. De lo contrario se necesitarán correcciones que
usualmente terminan siendo mucho más costosas que si los sistemas soportaran los
modelos nativamente. Ejemplos de esto son la _desdistorsión_[^opencv-undistort]
y _rectificación_[^opencv-stereorectify] de imágenes sobre la cual no nos
explayaremos aquí, pero basta con entender que es una transformación costosa
aplicada sobre todos los píxeles de las imágenes para “normalizarlas”. Esta
normalización facilita su uso cuando los sistemas no implementan
los modelos de calibración en los que el fabricante comparte los parámetros del
dispositivo.

[^opencv-stereorectify]: Ver `stereoRectify` en
<https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html>

[^opencv-undistort]: Ver `initUndistortRectifyMap` en
<https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html>


#### Calibración de parámetros extrínsecos

El conjunto de sensores a utilizar: un par de cámaras estéreo y una IMU con
acelerómetro y giroscopio, deben estar sujetos a un cuerpo rígido. Es decir, las
transformaciones en $SE3$ que describen como alterar la pose de un sensor a otro
se mantienen constantes sin importar los movimientos del dispositivo en conjunto.
Los valores que describen estas transformaciones relativas son lo que se denominan
_parámetros extrínsecos_ de la calibración en contraste con los íntrinsecos. Los
tres sistemas integrados requieren estos valores antes de comenzar la corrida.

#### Sincronización temporal

Otro problema escencial que debe solucionarse es el de la
sincronización de timestamps internas. Cualquier dispositivo que quiera
utilizarse para SLAM, debería tener las muestras de todos sus sensores
sincronizadas por hardware. Es decir, con timestamps que reflejen lo más
precisamente posible los tiempos internos en los que las muestras se tomaron.

Siguiendo con esta línea de problemas de marcas de tiempo, necesitamos un
mecanismo de sincronización de timestamps con el host que traiga los relojes
del dispositivo y los del host, el cual está corriendo Monado, al mismo _dominio
temporal_. Es decir, que una timestamp en uno, represente el mismo momento de
tiempo en el otro. Como las aplicaciones OpenXR utilizan el tiempo del host al
solicitar predicciones de poses, siempre intentaremos trabajar en ese dominio.
Veremos que esta sincronización no es trivial y es una fuente de errores
común.

#### Muestras de IMU unificadas

Entrando a problemas que afectan a sensores particulares, todos los sistemas de
SLAM estudiados esperan muestras de IMU unificadas que combinen en una única
timestamp los valores del acelerómetro y los del giroscopio. En el caso de tener
sensores con frecuencias diferentes o timestamps que no coinciden (pero siempre
sincronizadas), será necesario realizar algun tipo de transformacion sobre las
muestras para unifcarlas.

#### Obturador

<!-- #define MN_ROLLING_SHUTTER_NAME %\
Esta distorsión es homónima al tipo de cámara y se
denomina el efecto de rolling shutter.
-->

<!-- #define MN_SHUTTER %\
El término obturador proviene de los sensores ópticos tradicionales.
Un obturador era una pieza mecánica en movimiento que controlaba el tiempo
durante el cual la película fotográfica era expuesta a la luz de la escena.
Actualmente el proceso de control de exposición se realiza con interrupciones
digitales.
-->

Por el lado de los sensores de la cámara, será importante que el obturador o
_shutter_\marginnote{MN_SHUTTER} de las cámaras sea un _global shutter_, es
decir que todos los píxeles sean capturados en el mismo instante. Por el
contrario, las cámaras que se utilizan habitualmente en dispositivos de consumo
como teléfonos inteligentes, presentan un _rolling shutter_ en dónde los píxeles
son capturados en un "barrido", fila por fila. Esto genera
distorsiones\marginnote{MN_ROLLING_SHUTTER_NAME} significativas en presencia de
movimientos suficientemente rápidos como se ve en la
\figref{fig:rolling-shutter}. Estas distorsiones afectan negativamente la
capacidad de los algoritmos de SLAM para reconocer y trackear features de forma
estable.

\figw{fig:rolling-shutter}{source/figures/rolling-shutter.jpg}{Efecto rolling shutter}{%
Ejemplo de la distorsión que se genera en cámaras con rolling shutter que
capturan la imagen barriendo por filas de píxeles. Esto genera distorsiones en
los objetos rígidos que son particularmente notables en presencia de movimientos
de alta velocidad como los de la hélice. Esto no sucede con cámaras con global
shutter que capturan todos los píxeles en el mismo momento.\\
\\
\tiny Recorte de fotografía por Soren Ragsdale CC BY 2.0 \url{https://creativecommons.org/licenses/by/2.0/}
}{0.5\linewidth}

#### Exposición y ganancia

<!-- #define MN_MOTION_BLUR %\
El motion blur ocurre cuando los movimientos que se realizan modifican
sustancialmente la imagen a la que los sensores ópticos están expuestos mientras
el obturador sigue abierto.
-->

Otro aspecto muy importante a la hora de presentar muestras de imágenes a
sistemas de SLAM es el de utilizar valores adecuados de _exposición
(exposure)_ y _ganancia (gain)_. La exposición o exposure es la cantidad de
tiempo que el obturador de la cámara habilita la entrada de luz a los sensores
ópticos por cada cuadro. Por otro lado, la ganancia controla el nivel de
amplificación, usualmente digital, que ocurrirá sobre la señal original. El
control de estos parámetros, y el de la iluminación del entorno, es vital para
asegurar imágenes que posean un brillo adecuado. Imágenes muy oscuras pierden
detalles, y por ende la posibilidad de generar features. Imágenes
_sobreexpuestas_ que tienen demasiada iluminación en el entorno y valores de
exposición y ganancia altos, presentan el mismo problema al saturar los
receptores ópticos, causando que porciones significativas de la imagen se
transformen en manchas blancas. Estos problemas pueden verse en la
\figref{fig:under-over-exposure}. Además, los valores de
exposición y ganancia afectan el _ruido_ y el _motion blur_, esto es la difuminación que
se genera por movimientos rápidos en la imagen\marginnote{MN_MOTION_BLUR};
ejemplos esto se muestran en la \figref{fig:expgain-grids}.

\fig{fig:under-over-exposure}{source/figures/under-over-exposure.pdf}{Poca y sobre-exposición}{
Arriba: imagen con valores de exposición y ganancia adecuados a las condiciones
de iluminación de la toma. Izquierda: imagen oscura. Derecha: imagen sobre
expuesta. Los histogramas muestran la cantidad de píxeles que toman los valores
del eje X de 0 a 255. En las imágenes de abajo hay pérdida de información hacia
ambos extremos del histograma.
}

\fig{fig:expgain-grids}{source/figures/expgain-grids.pdf}{Ruido y motion blur}{%
Efectos de la exposición y ganancia sobre el ruido y motion blur de la imagen.
El ejemplo fue tomados con la cámara D455 con distintas configuracions de
exposición y ganancia. A izquierda se observan múltiples capturas de la misma
región de 256 píxeles cuadrados que tiene un objeto en movimiento. A derecha
tenemos una porción más pequeña de 32 píxeles cuadrados provenientes de las
mismas imágenes. Se puede observar en ambas grillas que aumentar ambos valores
también incrementa el brillo de la imagen. Por su parte en la figura derecha
podemos ver que aumentar la ganancia incrementa el ruido, mientras que en la
figura izquierda se observa que valores altos de exposición incrementan el
motion blur del objeto en movimiento.
}

Un último problema a considerar que se presenta por el parámetro de exposición,
es el llamado _parpadeo_ o _flicker_. Este ocurre en entornos iluminados por
lámparas artificiales. Estas presentan oscilaciones de intensidad a altas frecuencias que no son
visibles a simple vista, pero que si esas frecuencias no están alineadas con las
de la exposición de las cámaras, producen una secuencia de imágenes con niveles
de brillo intermitentes. Este punto debe tenerse en cuenta, ya que no todos los
sistemas son capaces de trackear features de forma eficiente cuando estas
cambian las intensidades de sus píxeles.

<!-- TODO@def: uso el concepto de "upstream" -->

Para evitar este abanico de problemas, se emplean algoritmos de _ajuste
automático_ de exposición y ganancia. Estos intentan balancear los valores de
estos parámetros en tiempo real; usualmente con técnicas de análisis de
histogramas. Hay que ser cuidadoso de que los sistemas empleados soporten tales
cambios en la naturaleza de los datos introducidos. En este trabajo se evaluaron
algunas posibilidades para emplear algoritmos de este tipo pero ninguna se
desarrolló lo suficiente como para realizar una contribución a upstream.
Implementar ideas como las propuestas por @zhangActiveExposureControl2017 es una
tarea pendiente como trabajo a futuro. Por ahora, los controladores recaen en
ajustes manuales en los cuales se usa la heurística de que si la imagen se ve
razonablemente bien a los ojos del usuario, entonces esta es probablemente
adecuada para el sistema de SLAM.

#### Comunicación con el dispositivo

La interfaz de comunicación con el hardware será diferente en cada controlador, pero
será usual tener que tratar con hilos consumidores y callbacks asíncronos. En estos
habrá colas de datos que deberemos evitar saturar con procesamientos bloqueantes. Para el caso particular del
manejo de imágenes, al ser estos recursos de gran tamaño, Monado utiliza mecanismos de
_reference counting_ mediante su estructura `xrt_frame` para la gestión de memoria.
Además, como se mencionó anteriormente, `slam_tracker` utiliza la estructura de datos
`cv::Mat` de OpenCV como contenedora de imágenes la cual también provee conteo de
referencias. Finalmente, las interfaces con hardware mediante librerías específicas
puede traer un contenedor extra de conteo de referencias. Esto puede dar lugar a muchos
problemas con el manejo de la memoria y especial cuidado debe tenerse a la hora de
adquirir y liberar estos recursos.

#### Configuraciones de captura

Los sensores suelen venir con distintos modos de captura de muestras. Algunos
habilitan mayores frecuencias a costa de menor precisión, o mayor precisión a
costa de un mayor consumo energético, y otras soluciones de compromiso similares. La
capacidad de acceso a la configuración de estos sensores dependerá
principalmente de lo que los fabricantes del dispositivo decidan exponer al
programador. En caso de existir más de una forma de captura, será necesario
poder seleccionar en el controlador la configuración deseada.

#### Sistemas de coordenadas

Finalmente, el último punto que traeremos a atención, es la convivencia de
múltiples sistemas de coordenadas que deben unificarse: el de la IMU, el de la
implementación de SLAM y el de Monado.

Por un lado, será necesario en algunos casos alinear las muestras de la IMU al
sistema de coordenadas de la implementación de SLAM antes de transferirlas. De
lo contrario, se pueden presentar situaciones como una implementación que
considera que está moviéndose hacia adelante por las muestras ópticas, mientras
que las muestras de la IMU le indican que está yendo hacia la derecha; esto
causa inconsistencias que suelen terminar en divergencias de los algoritmos de
optimización. Además, es usual que también se necesite aplicar un cambio de
coordenadas a las poses que el sistema le devuelve a Monado.

### RealSense (TODO)

Estamos ahora en condiciones de entender las contribuciones a controladores
realizadas en este trabajo. Comencemos por las del controlador para dispositivos
RealSense.

<!-- TODO@def: "host", lo uso acá y en otros lados -->
<!-- TODO@def: DIY -->

Para soportar la cámara D455, se extendió significativamente en Monado el
controlador de dispositivos RealSense. Hasta el momento, la única cámara de esta
línea soportada por Monado era la T265[^t265]. Esta cámara es curiosa, ya que
presenta un algoritmo de SLAM privativo que corre dentro del dispositivo sin
necesidad de interactuar con el host. Este controlador se encargaba únicamente
de inicializar el módulo interno de SLAM de la cámara y obtener las poses
computadas por la misma para uso en las aplicaciones OpenXR. Uno de sus usuarios
clave era el casco libre del proyecto North Star [^north-star] que las
utilizaba, en iteraciones anteriores, como principal forma de tracking. En la
web del proyecto pueden encontrarse imágenes [^north-star-img1]
[^north-star-img2] que muestran estos cascos con la cámara T265 sujeta en su
parte superior.

\fig{fig:northstar-t265}{source/figures/northstar-t265.jpg}{T265 y proyecto North Star}{%
El casco AR libre del proyecto North Star con una cámara T265 sujeta en la parte superior.
}

https://www.collabora.com/assets/images/blog/ProjectNorthStar.jpg
[^t265]: <https://www.intelrealsense.com/tracking-camera-t265/>

[^north-star]: El proyecto North Star de UltraLeap (prev. LeapMotion) es un
casco AR "DIY" que puede fabricarse con piezas impresas en 3D y la compra de
algunos componentes. <https://developer.leapmotion.com/northstar>

[^north-star-img1]:
[^north-star-img2]:

Al no haber ningún tipo de manejo de las imágenes o muestras de IMU provistas
por la cámara, se tuvo que implementar la gestión de estos sensores. Es ahora
posible utilizar cualquier cámara de la línea RealSense que posea un par de
cámaras estéreo y una IMU. Como trabajo futuro, sería interesante comparar el
tracking interno de una T265 con los distintos sistemas externos integrados en
este trabajo.

### Windows Mixed Reality (TODO)

<!-- #if 0 -->
      - [TODO] Atenuación exponencial para sincronización temporal
      - [TODO] Problemas específicos de calibración: camaras con poco solapamiento,
            intrinsics para modelo raro radtan8 (referenciar a las contribuciones
            explicadas abajo)
      - [TODO] Trabajo con la comunidad, ingeniería inversa, thaytan camera
            streams, exposure setting, analisis de exposure en sistema privativo,
            analisis de parámetros extrínsicos, lectura de paquetes USB binarios
<!-- #endif -->
<!-- #if 0 -->
| Caraceterística/Controlador      | RealSense                                                                                                                                                 | WMR                                                                                                      |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Calibración de Cámaras           | Modelo de cámara rt4 precalibrado, los parámetros son cero, no hay distorsión. Cámaras con mucho solapamiento.                                            | Cámara fisheye, con modelo rt8 (extraño). No soportado en ningún sistema. Cámaras con poco solapamiento. |
| Calibración de IMU               | Precalibrados. Parámetros son cero. Soportado por cualquier sistema. Soportado por cualquier sistema.                                                     | No precalibrado. Solo soportado por Basalt. Aunque la calibración es sencilla de realizar en Monado.     |
| Sincronización temporal interna  | Sí, aunque requiere parche en el kernel.                                                                                                                  | Sí.                                                                                                      |
| Sincronización temporal con host | Automática por SDK.                                                                                                                                       | Manual con suavizado exponencial. Resta hacer cálculo de latencia.                                       |
| Muestras de IMU                  | Muestras no unificadas. Se utiliza omisión de sensor más lento. Resta interpolar. D455: accel. 60-250hz y giro. 200-400hz.                                | Muestras unificadas. 1000hz en paquetes de 4. Se promedian y se usan 250hz.                              |
| Muestras de Cámara               | Múltiples resoluciones y frecuencias para elegir. Obturador global.                                                                                       | Cámaras monocromáticas 640x480 a 30fps. Obturador global.                                                |
| Exposición y ganancia            | Manual. Alternativa automática con el SDK aunque no es ideal para aplicaciones  de SLAM por que aumenta exposure rápido. Los sensores son de más calidad. | Manual. Resta implementar curvas estudiadas. Sensores baratos. Ingeniería inversa.                       |
| Interfaz con hardware            | RealSense SDK. Manejo automático de colas. rs_frame.                                                                                                      | Libusb. Manejo manual de memoria. Protocolo desconocido.                                                 |
<!-- #endif -->
<!-- #if 0 -->



TODO: terminar de mencionar las caracteristicas que falta acá,
despues describirlas rápidamente en la seccion de realsense
despues hablar de lo que me interese de WMR
despues describir las caracteristica srapidamente tambien en la seccion de WMR
y finalmente presentar una tabla comparativa (o capaz eso hacerlo antes?)

-------------------------------

-[x]imu/frame sinks
-[x]communication con OpenXR app y TrackerSlam
-[x]pose correction: per system


-[x]que son las camaras realsense
-[x]por que esta bueno tener estas camaras y por que las use
-[x]variedad de dispositivos, rs_ddev, t265

-[x]lib: realsense api
-[x]stream options: multiple (configured through json)
-[x]camera calibration: precalibrated
-[x]imu calibration: precalibrated
-[x]imu stream detail: accel/gyro stream merge
-[x]clock sync: global timestamp automatically managed
-[x]clock sync: hardware timestamps synced
-[x]exposure-gain-auto: can use auto exposure from realsense sdk, sensorquality<->exposure
-[x]shutter: global
-[x]frame management: realsense sdk threads, thread queues, ¿rs_frame/xrt_frame/cv::Mat?
-UI: screenshot?
-mencionar modelos de sensoreS? BMI, OV, etc
<!-- TODO: tabla para comparar estas características de los dispositivos? -->



<!-- #endif -->
