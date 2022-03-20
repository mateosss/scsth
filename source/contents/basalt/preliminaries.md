### Preliminares

La decisión sobre cuál sistema de localización visual-inercial integrar con
Monado no fue sencilla. Fue necesario descartar docenas de implementaciones e
incluso así, no fue trivial entender si los sistemas elegidos finalmente
resultaron los más adecuados para el contexto de XR. Cada implementación
presentaba ventajas y desventajas, aunque es usual que las respectivas
publicaciones se concentren en destacar solo las métricas favorables. Más aún,
es necesario conocimiento experto para comprender cómo la elección de ciertos
fundamentos teóricos, técnicas algorítmicas, decisiones arquitecturales o de
tecnología afectan a la calidad del tracking dedicado a XR. Gran parte
de este trabajo se basó en el estudio de los conceptos necesarios para poder
tomar este tipo de decisiones.

A grandes rasgos y sin un orden en particular, las propiedades deseables que se
consideraron a la hora de elegir sistemas fueron:

1. Versatilidad en la configuración sensores: Monado necesita soportar una gran
  variedad de dispositivos, es por esto que se prefirieron sistemas que soporten
  la mayor cantidad de combinaciones y tipos de sensores. En el mejor de los
  casos, Monado debería ser capaz de localizar desde cascos con cámaras estéreo
  y una IMU, hasta celulares con una única cámara y sin giroscopio.

2. Licencia permisiva: La licencia y filosofía de Monado da gran libertad al
   programador que lo utilice de hacer lo que desee con su código fuente. Esto
   incluye poder utilizarlo en proyectos en dónde se prefiere no distribuir
   dicho código. Licencias de código libre “virales” como la GPL
   [@GNUGeneralPublic] no permiten esto y enlazar Monado a sistemas con este
   tipo de licencias contagiaría a los proyectos que dependen de Monado
   quitándoles la libertad de decidir no publicar su código.

3. Desarrolladores activos: Estos sistemas suelen surgir de grupos de
   investigación y es muy común que se abandonen luego de que el trabajo sea
   publicado. Será necesario encontrar, dentro de lo posible, sistemas con un
   desarrollo activo, con mantenedores accesibles y que, en el mejor de los
   casos, acepten contribuciones a su proyecto.

4. Estabilidad, facilidad de instalación y buenas prácticas de desarrollo: Los
   sistemas de SLAM son muy complejos y es usual que se optimicen para funcionar
   únicamente en los conjuntos de datos de prueba dejando de lado estas
   características que son fundamentales a la hora de querer brindar un sistema
   para ser utilizado por usuarios finales.

5. Rendimiento: El área de XR tiende a buscar la reducción del tamaño de los
   dispositivos para mejorar su ergonomía y practicidad. Un sistema de tracking
   debe ser capaz de operar en contextos con recursos acotados, debería utilizar
   poca memoria, poca energía y ser capaz de estimar poses a altas frecuencias y
   utilizando poca capacidad de cómputo.

6. Precisión: Por último y no menos importante, queremos que la precisión de la
   localización sea adecuada. El nivel de precisión requerido dependerá del tipo
   de aplicación. Es común que se necesite precisión submilimétrica en contextos
   de VR donde la simulación cubre completamente el campo de visión del usuario,
   y fallos en el tracking puedan inducir mareos. Mientras que para otros
   contextos como AR realizado por un celular, no es tan vital contar con ese
   nivel de exactitud.

#### Sistemas integrados

En este trabajo se integraron con Monado tres sistemas de código libre
distintos, primero _Kimera-VIO_ [@rosinolKimeraOpenSourceLibrary2020], luego
_ORB-SLAM3_ [@camposORBSLAM3AccurateOpenSource2021] y finalmente _Basalt_
[@usenkoBasaltVisualInertialMapping2020].

Kimera-VIO[^kimera-repo] es una implementación desarrollada en el Instituto de
Tecnología de Massachusetts (MIT) con una licencia permisiva BSD-2
[@2ClauseBSDLicense]. Fue publicada originalmente en octubre de 2019 y su última
actualización significativa[^kimera-last-update], en dónde se introduce la
posibilidad utilizar una única cámara, ocurrió en abril de 2021.
Kimera resultó inicialmente atractivo por su licencia y su promesa de correr en
tiempo real. Además de esto posee funcionalidades muy interesantes para XR como
la reconstrucción y análisis semántico del entorno en el que el dispositivo se
encuentra. Desgraciadamente, no logró ser adecuado mostrando grandes
dificultades a la hora de correrlo en sensores distintos a los presentados en su
publicación. Más aún el término “tiempo real” en el contexto de la publicación
es ambiguo, ya que está lejos de ser capaz de ejecutarse a frecuencias adecuadas
para XR y es más adecuado para uso en robots con frecuencias de menos de 10 Hz
[@rosinolKimeraOpenSourceLibrary2020, Fig. 5].

ORB-SLAM3[^orbslam3-repo] es desarrollado por la Universidad de Zaragoza con una
licencia viral GPL-3.0 [@GNUGeneralPublic]. Fue publicado inicialmente en julio
de 2020 y su última actualización significativa[^orbslam3-last-update] ocurrió
en diciembre de 2021. ORB-SLAM3 es la tercera iteración de una línea de sistemas
que dominan las tablas comparativas de SLAM desde hace unos cuantos años y es
por esto que se implementó incluso aunque no posea una licencia permisiva. El
sistema presenta varios métodos novedosos que mejoran la precisión del tracking
mientras que muestra ser capaz de estimar poses a unos 20 Hz o 30 Hz
[@camposORBSLAM3AccurateOpenSource2021, Tabla 6]. El sistema es el más versátil
del campo permitiendo ser ejecutado en configuraciones con una cámara
(monocular) o dos (estéreo), con o sin uso de la IMU e incluso con cámaras de
profundidad. Además, soporta la reconstrucción de múltiples mapas y la capacidad
de interconectarlos o incluso guardarlos en almacenamiento persistente para ser
reutilizados en sesiones de tracking posteriores. Una desventaja es que la
trayectoria que se da al construir el mapa es particularmente ruidosa y difícil
de utilizar en XR. Se plantea como trabajo a futuro investigar más acerca de la
funcionalidad de reutilización del mapa y como funciona el tracking con mapas ya
construidos.

Finalmente, Basalt[^basalt-repo] es desarrollado por el Instituto Técnico de
Múnich con una licencia permisiva BSD-3 [@3ClauseBSDLicense]. Fue publicado
originalmente en abril de 2019 y su última actualización
significativa[^basalt-last-update] [@demmelBasaltSquareRoot2021] ocurrió en
octubre de 2021. Basalt solo es capaz de correr en tiempo real su sistema de VIO
necesitando de una pasada offline de su _“mapper”_ para lograr un mapa
consistente. A pesar de esto, mostró ser sorprendentemente preciso y tener un
gran desempeño. En particular, es un sistema que puede correr fácilmente a 60 Hz
consumiendo cuadros a mayores resoluciones que las probadas en ORB-SLAM3 y
Kimera y duplicando las frecuencias de muestreo a 60 fps. Esta capacidad de
soportar mayor cantidad de muestras aumenta significativamente la precisión de
la trayectoria a pesar de que no sea un sistema de SLAM completo. Además de
esto, el sistema es notablemente más sencillo de compilar al tener un buen
manejo de sus dependencias, posee mejores prácticas de ingeniería de software y
es en general mucho más estable logrando fácilmente sesiones de tracking
ininterrumpidas a diferencia de los sistemas anteriores.

[^kimera-repo]: <https://github.com/MIT-SPARK/Kimera-VIO>
[^orbslam3-repo]: <https://github.com/UZ-SLAMLab/ORB_SLAM3>
[^basalt-repo]: <https://gitlab.com/VladyslavUsenko/basalt>
[^kimera-last-update]: <https://github.com/MIT-SPARK/Kimera-VIO/pull/152>
[^orbslam3-last-update]: <https://github.com/UZ-SLAMLab/ORB_SLAM3/releases/tag/v1.0-release>
[^basalt-last-update]: <https://gitlab.com/VladyslavUsenko/basalt/-/commit/24325f2a>

Los tres sistemas fueron integrados en Monado con distintos niveles de éxito,
pueden verse demostraciones de cómo funcionan en los videos referenciados al pie
de página [^kimera-video] [^orbslam3-video] [^basalt-video]. Más adelante, en el
[](#evaluation), se verán resultados y distintas métricas comparativas entre los
sistemas.

[^kimera-video]: Kimera-VIO con Monado: <https://youtu.be/gxu3Ve8VCnI>
[^orbslam3-video]: ORB-SLAM3 con Monado: <https://youtu.be/kJwWY973b10>
[^basalt-video]: Basalt con Monado: <https://youtu.be/ajuqQ7E1MFw>

Las terminologías y jerga del área de SLAM/VIO pueden resultar abrumadoras, pero
se espera que introduciéndolas en el contexto de una implementación concreta se
puedan entender mejor los problemas que los sistemas, en general, tienen que
resolver. Por todas las razones mencionadas anteriormente, Basalt es actualmente
el sistema de preferencia para ser utilizado con Monado y, si bien se estudió el
código fuentes de los tres sistemas, en esta parte del trabajo que sigue a
continuación _nos vamos a enfocar en profundizar en la implementación de
Basalt_.

#### Problemáticas de un sistema

<!-- #define MN_BUNDLE_ADJUSTMENT %\
Introdujimos el término bundle adjustment (BA) en la \Cref{def:bundle-adjustment}
en el contexto de cuadrados mínimos. Este se refiere al refinamiento simultáneo de un conjunto de
poses de cámara, o vistas, y puntos 3D en el mapa que han sido observados por
estas vistas. Así, se intenta reducir el llamado “error de reproyección” del
conjunto actualizando tanto las poses de las cámaras como la posición de los
puntos observados. Este error hace referencia a la distancia entre las
posiciones de los puntos y en dónde las vistas esperan que estos
se encuentren \autocite{hartleyMultipleViewGeometry2004}.
-->

Un problema central en este tipo de sistemas es el de poder generar un mapa y
una trayectoria que sean _globalmente consistentes_. Con esto nos referimos a que
nuevas mediciones tengan en cuenta todas las mediciones anteriores en el
sistema. Una forma ingenua de encarar esto, sería realizando _bundle adjustment_\marginnote{MN_BUNDLE_ADJUSTMENT}
sobre todas las imágenes capturadas a lo largo de una corrida,
integrando además las mediciones provenientes de la IMU.
Desafortunadamente, este método excede rápidamente cualquier capacidad de
cómputo de la que dispongamos, y aún más teniendo en cuenta que nuestro objetivo
es localizar en tiempo real al dispositivo de XR.

Por esta razón, es usual recurrir a distintas formas de reducir la complejidad
del problema. Para realizar _odometría visual-inercial (VIO)_, es común que
se ejecute la función de optimización sobre una _ventana local_ de cuadros y
muestras recientemente capturadas, ignorando muestras históricas y acumulando
error en las estimaciones a lo largo del tiempo. Además, esta mirada tiene la
desventaja adicional de que una porción significativa de los fotogramas
capturados podrían tener posiciones similares que no añadirían demasiada información al estimador, o
incluso que algunos fotogramas puedan ser de baja calidad por contener _motion
blur_ u otro tipo de anomalías. Por otro lado, soluciones que intentan hacer
_mapeo visual-inercial_ realizan el bundle adjustment sin utilizar todas las
imágenes capturadas, sino que se limitan a la utilización de algunos fotogramas
clave, o _keyframes_ elegidos mediante criterios que priorizan cuadros nítidos y
con distancias (_baselines_) prudenciales entre ellos.

Como las muestras de IMU vienen a mayor frecuencia que las de la cámara, es
común que estas se _preintegren_ de forma tal de combinar muestras simultáneas entre dos keyframes en
una única entrada del optimizador. Sin embargo, un problema en el que esta
integración incurre, es que las mediciones de las IMU son altamente ruidosas, y
acumularlas durante tiempos prolongados acumula también cantidades
significativas de error. Este factor nos limita el tiempo que puede transcurrir
entre dos keyframes; como ejemplo en @mur-artalVisualInertialMonocularSLAM2017
se habla de keyframes que no pueden tener más de medio segundo entre sí. Además,
tener keyframes a muy bajas frecuencias afecta la calidad de las
estimaciones de velocidad y _biases_; estos últimos son offsets de medición
inherentemente variables de los acelerómetros y giroscopios a los que es
necesario reestimar de forma constante para compensar por ellos en la medición final.

#### Propuesta de Basalt

<!-- TODO@high@end: vi que esta Margin note parece salirse tambien -->
<!-- #define MN_FACTOR_GRAPH %\
Los grafos de factores son una muy buena forma de representar problemas con
muchas variables aleatorias interdependientes y muestras que las relacionan (factores).
En general, el uso de estos grafos trae beneficios
computacionales interesantes y son de gran importancia para el área de SLAM.
Sin embargo, no nos adentraremos demasiado en el tema en este trabajo y dirigimos
al lector interesado a \textcite{dellaertFactorGraphsRobot2017}.
-->

<!-- XXX: USO FACTOR NO LINEAL SIN EXPLICARLO!! -->
La novedad de Basalt [@usenkoBasaltVisualInertialMapping2020] es que formula el mapeo visual-inercial como un problema de
bundle adjustment y utiliza, de una forma específica, todas mediciones visuales e inerciales a altas frecuencias.
Usa un _grafo de factores_\marginnote{MN_FACTOR_GRAPH} [^gtsam-whatarefactorgraphs] de forma similar a otros sistemas, también llamado
_grafo de poses_ en este contexto por contener poses a estimar como nodos. En
lugar de utilizar todos los fotogramas se propone realizar la optimización en
dos capas. La capa de VIO, emplea un sistema de odometría visual-inercial, que
ya de por sí supera a otros sistemas del mismo tipo, proveyendo estimaciones de
movimiento a la misma frecuencia que el sensor de la cámara provee imágenes.
Luego, se seleccionan keyframes y se agregan _factores no-lineales_
entre estos que estiman la diferencia de posición relativa.
Estos dos factores, keyframes y poses relativas, se utilizan en la capa de
bundle-adjustment global.

[^gtsam-whatarefactorgraphs]: Artículo introductorio a los grafos de factores: <https://gtsam.org/2020/06/01/factor-graphs.html>

<!-- #define MN_LOOP_CLOSING %\
Esto es fundamental para entender cuándo el dispositivo está visitando un lugar
por el que ya pasó. Esto se denomina “loop closing”.
-->

<!-- #define MN_FEATURES %\
Las features son puntos de interés relevados en una imagen.
Son estos los puntos que triangularemos en el bundle adjustment.
-->

La capa de VIO, detecta _features_\marginnote{MN_FEATURES} que son rápidas y buenas para seguir durante
varios cuadros (esto es el _optical flow_ que veremos en la sección
[](#optical-flow)), mientras que en la capa de mapeo se usan features adecuadas
que son indiferentes a las condiciones de luz o al punto de
vista de la cámara\marginnote{MN_LOOP_CLOSING}. De esta forma tenemos un sistema que es capaz de utilizar
las mediciones a alta frecuencias de los sensores y al mismo tiempo tiene la
capacidad de detectar cuando se está en ubicaciones ya
visitadas, obteniendo así un mapa que es globalmente consistente. Además, el
problema de optimización se reduce, ya que a diferencia de otros sistemas, no es
necesario estimar velocidades ni biases (de la IMU).
