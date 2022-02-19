## Introducción

### Localización en XR

Los sistemas de _realidad virtual_ y _realidad aumentada_, o _VR_ y _AR_
respectivamente por sus siglas en inglés, intentan valerse de nuestras formas
usuales de interactuar con el mundo que nos rodea, para así generar simulaciones
con características muy particulares y difíciles de obtener de otra forma.

<!-- #define MN_REVERSE_ENGINEER_BIOLOGY %\
Al considerar sistemas de VR deben tenerse en cuenta, además de los desafíos
de ingeniería, los problemas propios de comprender como nuestra percepción
afecta lo que experimentamos. Lograr entender estos procesos cognitivos lo suficiente
como para valernos de ellos a la hora de diseñar sistemas de XR es fundamental
para obtener experiencias inmersivas. Esto puede pensarse como un trabajo de
``ingeniería inversa'' sobre nuestra propia biología \autocite{lavalleVirtualReality}.
-->

En el caso de VR uno usualmente tiene cascos con pantallas o, en inglés, _head
mounted displays (HMD)_, y algún tipo de controles manejados con ambas manos.
Estos permiten aplicaciones con un alto nivel de inmersión. La característica de
poder adentrarse profundamente en la simulación son deseadas para fines que
varían desde el entretenimiento, generalmente en forma de videojuegos, hasta el
entrenamiento para situaciones críticas, como lo pueden ser operaciones médicas
o la navegación de aeronaves. Por el lado de AR, se suele pensar en dispositivos
que permiten agregar o “aumentar” lo que uno ve con información adicional. Estos
pueden ser celulares con cámaras o incluso lentes con pantallas transparentes
que superponen información 2D o modelos 3D sobre la escena real. Además existen
otros términos como _realidad mixta_ (_MR_) que intentan hacer referencia a los
distintos matices en los que la realidad puede ser combinada con la simulación;
es común utilizar el término _XR_ para englobar a este espectro de sistemas, a
veces también referido como _realidad extendida_. En general, todos ellos
comparten problemas similares que son propios de la percepción humana y están
relacionados con nuestra psicología y fisiología
\marginnote{MN_REVERSE_ENGINEER_BIOLOGY}.

Para producir experiencias de XR, es necesario coordinar un gran número de
sistemas internos que se encuentran a lo largo del hardware y del software para
XR. Uno de los problemas fundamentales y particularmente complicados en XR es el
de la _localización_ o _tracking_; esta es la capacidad del sistema de
identificar la posición y orientación del dispositivo XR, su _pose_, en el
entorno para poder reflejarla en la experiencia simulada. En este trabajo nos
enfocaremos en el problema de localización. Para una lectura más comprensiva
sobre el resto de los problemas a los que XR se enfrenta, y en particular VR, se
recomienda el trabajo de @lavalleVirtualReality.

Hay muchas formas de encarar el problema de localización y en general todas
requieren del uso inteligente de sensores físicos, ya sean mecánicos,
inerciales, magnéticos, ópticos, o incluso acústicos
[@welchMotionTrackingNo2002]. Todos estos métodos de tracking comparten un
problema en común: los sensores son imperfectos y sus mediciones son _ruidosas_.
Tomemos por ejemplo uno de los paquetes de sensores más comúnmente utilizados en
esta área, una _unidad de medición inercial_ o _IMU_ por sus siglas en inglés.
Estas integran _giroscopios_ para la medición de velocidad angular,
_acelerómetros_ para la aceleración lineal, y algunas veces también
incluyen _magnetómetros_. En teoría, si sus mediciones fueran perfectas, una IMU
debería proveer suficiente información para determinar la pose en el espacio de
un dispositivo que la contenga. Pero incluso las IMU de mayor calidad acumulan
tanto ruido que la integración de sus mediciones durante cortos períodos de
tiempo devuelve poses que tienen un error de cientos de metros, ver
\Cref{tbl:imu-accumulated-error}. Para contrarrestar la naturaleza imperfecta de
sensores físicos como estos, los enfoques más exitosos de localización emplean
una combinación de múltiples sensores junto a algoritmos de fusión ingeniosos
capaces de integrar tipos de muestras tremendamente distintos en una estimación
de la pose que es suficientemente buena.

Table: \label{tbl:imu-accumulated-error} Error acumulado luego de cierto tiempo
de integrar mediciones de IMU de distinta calidad. Vale aclarar que en
dispositivos XR las IMU utilizadas son del tipo _consumidor_ por su menor costo.
Datos de [@InertialNavigationPrimer, secc 3.3].


| **Categoría / Tiempo** | **1 s** | **10 s** | **60 s** | **10 min** | **1 hr**  |
|------------------------|---------|----------|----------|------------|-----------|
| Consumidor             | 6 cm    | 6.5 m    | 400 m    | 200 km     | 39.000 km |
| Industrial             | 6 mm    | 0.7 m    | 40 m     | 20 km      | 3.900 km  |
| Táctico                | 1 mm    | 8 cm     | 5 m      | 2 km       | 400 km    |
| Navegación             | <1 mm   | 1 mm     | 50 cm    | 100 m      | 10 km     |

En años recientes, la llamada localización _visual-inercial (VI)_ ha cobrado gran
popularidad en el ecosistema de XR. Al emplear cámaras, usualmente al menos dos,
junto a una IMU dentro de un dispositivo XR (p. ej. un HMD o un celular). La
localización VI estima la pose del agente haciendo que el mismo dispositivo
“mire” hacia su entorno para ganar entendimiento del mismo. Uno de los
principales beneficios de este tipo de tracking es que tener todos los sensores
empaquetados dentro del dispositivo resulta muy conveniente para el usuario, ya
que no necesita colocar ni configurar ningún tipo de sensor externo en su
entorno. Este tipo de localización para aplicaciones de XR se consideraba
inviable hasta hace un poco más de una década, pero avances en la capacidad de
cómputo y en las técnicas de fusión han hecho posible que este ya no sea el
caso.

Ya existen dispositivos XR que emplean localización visual-inercial de forma
exitosa en productos comerciales como el _Meta Quest_[^quest2], los cascos
_Windows Mixed Reality_[^wmr] o incluso los SDK _ARCore_[^arcore] y
_ARKit_[^arkit] utilizados en celulares inteligentes. No obstante, todas estas
soluciones son propietarias, por lo tanto no hay manera de mejorarlos, reusarlos
en nuevos proyectos o productos, o incluso aprender de su implementación a menos
que se adquieran licencias especiales de sus fabricantes.

[^quest2]: <https://www.oculus.com/quest-2/>
[^wmr]: <https://www.microsoft.com/en-us/mixed-reality/windows-mixed-reality>
[^arkit]: <https://developer.apple.com/augmented-reality/arkit/>
[^arcore]: <https://developers.google.com/ar>

### SLAM y VIO para localización visual-inercial

Afortunadamente, el área académica en navegación visual-inercial ha
experimentado un gran desarrollo en estas últimas décadas. No solo es un
problema central en áreas como las de robótica, sino que además es atractiva por
combinar una diversa cantidad de áreas como visión por computadora, fusión de
sensores, optimización, estimación probabilística, entre otras. Esta ola de
investigación ha dado lugar a una gran cantidad de implementaciones de software
libre, con distintos grados de rendimiento, robustez, precisión, aplicaciones,
facilidad de uso, entre otras propiedades de interés. Recursos como
<http://openslam.org> y estudios como [@servieresVisualVisualInertialSLAM2021a] o
[@taketomiVisualSLAMAlgorithms2017a] pueden listar docenas de sistemas
disponibles para considerar. Más aún, cada año nuevos sistemas aparecen mientras
otros dejan de ser mantenidos. Seguir los avances del área puede ser
desafiante, pero esto es una consecuencia de su desarrollo tan activo.

Específicamente, en este trabajo trataremos con sistemas de _localización y
mapeo simultáneo (SLAM)_ mediante sensores visuales-inerciales (VI-SLAM). Como
su nombre lo indica, SLAM intenta construir un mapa del entorno en el que el
agente XR se encuentra y localizarlo en el mismo de forma simultánea;
usualmente, sin contar con información a priori sobre su pose ni el entorno en
el que se encuentra. Hay múltiples maneras de implementar SLAM y VI-SLAM, pero
los sistemas en los que nos concentraremos en este trabajo usan mediciones de la
IMU a altas frecuencias (p. ej. 200 hz) que miden el _“movimiento interno”_ que
el agente experimenta, también conocidas como mediciones _propioceptivas_, junto
a muestras más lentas (p. ej. 20 hz) de cámaras, usualmente un par de ellas, que
dan información acerca de como el entorno está cambiando alrededor del agente
cuando este se mueve. Estas son llamadas mediciones _exteroceptivas_ y ayudan a
corregir las mediciones ruidosas de la IMU.

<!-- #define MN_FEATURE_DEF %\
La terminología para definir puntos de interés es un poco confusa. Intentaremos
esclarecer en capítulos posteriores el significado de términos como keypoint,
landmark, feature, corner, etc. que algunas veces pueden parecer
intercambiables en la literatura de visión por computadora.
-->

El mapa que se forma en VI-SLAM suele crearse a partir de _puntos de interés_
(_landmarks_) en la escena que fueron triangulados y detectados durante
múltiples muestras como _esquinas_ o _features_\marginnote{MN_FEATURE_DEF} en
las imágenes de las cámaras. En el mejor de los casos el mapa formado en SLAM y
las actualizaciones que este sufre pueden durar la corrida entera o incluso ser
guardados en almacenamiento persistente, y esto ayuda al dispositivo a entender
cuando está viendo un lugar que ya vio anteriormente. Sin embargo, hay
soluciones más sencillas que solo mantienen el mapa por una corta ventana de
tiempo. A estos sistemas se los suele denominar de _odometría visual-inercial
(VIO)_, y suelen presentar mejor desempeño que soluciones completas
de SLAM a costa de la precisión en la trayectoria estimada.

### Integración en Monado

_Monado_[^monado] es una implementación de código libre del estándar abierto
_OpenXR_ [@thekhronosgroupinc.OpenXRSpecification] que intenta unificar la forma
en la que las aplicaciones interactúan con el hardware XR. Si bien
entenderemos mejor estos términos más adelante en la \Cref{sec:thesis-context},
basta con saber que OpenXR es una especificación desarrollada por el _Khronos
Group_[^khronos], un consorcio abierto sin fines de lucro integrado por
distintos participantes de la industria. Monado fue desarrollado y es mantenido
por _Collabora_[^collabora], una consultora especializada en proyectos de código
abierto, la cual además participa activamente en la especificación de OpenXR
desde sus inicios. Este trabajo fue realizado en el marco de una pasantía con
Collabora.

[^monado]: <https://monado.dev>
[^khronos]: <https://www.khronos.org>
[^collabora]: <https://www.collabora.com>

Monado, además de implementar la especificación de OpenXR, provee varias
herramientas y funcionalidades para XR, además de controladores para
dispositivos populares. El proyecto, antes de este trabajo, contaba con un
puñado de métodos de tracking, pero la localización visual-inercial por SLAM o
VIO era una característica faltante.

Este trabajo, entonces, resultó en la integración de tres sistemas de SLAM/VIO
de código libre con Monado. En particular, los sistemas integrados fueron
Kimera-VIO [@rosinolKimeraOpenSourceLibrary2020], ORB-SLAM3
[@camposORBSLAM3AccurateOpenSource2021] y Basalt
[@usenkoBasaltVisualInertialMapping2020]. Además, se adaptaron controladores para
poder utilizar dispositivos con este tipo de tracking en Monado, incluyendo
cascos de la plataforma Windows Mixed Reality. Estos, según el mejor
entendimiento del autor, son ahora los primeros cascos comerciales capaces de
ser localizados por SLAM/VIO en una plataforma basada completamente en código
libre.

### Estructura de la Tesis (TODO)

```none
[TODO] En esta sección detallaría lo que se va a ver en cada capítulo.

La planeo escribir después de terminar de acomodarlos. Ahora tengo
algunos de muy pocas páginas (1 o 2) y eso no tiene mucho sentido.
```

<!--
Contexto/motivación (mencionar algo de las comunidades con las que trabajé,
mencionar que CV es muy trial and error, oversights pueden costar horas)
mencionar ILLIXR, WMR community?
-->
