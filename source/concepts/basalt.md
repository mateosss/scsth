<!-- TODO: explicar bundle adjustmente -->
<!-- TODO: que es motion blur, (quizás usar nota al pie) -->
<!-- TODO: maybe? cuando menciono preintegración citar el paper On-Manifold preintegration -->
<!-- TODO: Estoy implicitamente hablando de un optimizador, cuando hablo de factor graphs? -->
<!-- TODO: Explicar factores no-lineales, o almenos decir que no se explican -->
<!-- TODO: Que son features? -->
<!-- TODO: Que es loop closing? -->
<!-- TODO: VIO habla acerca de componentes: (patch tracking, landmark
representation, first-estimate Jacobians, marginalization
scheme) que podría ser interesante discutir -->
<!-- TODO: Citar bien la cita -->

# Basalt

## Problemáticas Preliminares

Un problema central en este tipo de sistemas es el de poder generar un mapa y
una trayectoria que sea *globalmente consistente*. Con esto nos referimos a que
nuevas mediciones tengan en cuenta todas las mediciones anteriores en el
sistema. Una forma ingenua de encarar este problema sería realizando *bundle
adjustment* sobre todas las imágenes capturadas a lo largo de una corrida,
integrando de alguna forma todas las mediciones provenientes de la IMU.
Desafortunadamente, este método excede rápidamente cualquier capacidad de
cómputo de la que dispongamos, y aún más teniendo en cuenta que nuestro objetivo
es localizar en tiempo real al dispositivo de XR.

Por esta razón, es usual recurrir a distintas formas de reducir la complejidad
del problema. Para realizar *odometría visual-inercial (VIO)*, es común que
realicen la función de optimización sobre una *ventana local* de cuadros y
muestras recientemente capturadas, ignorando muestras históricas y acumulando
error en las estimaciones a lo largo del tiempo. Además, este enfoque tiene la
problemática añadida de que una porción significativa de los fotogramas
capturados tienen posiciones similares que no añaden información al estimador, o
incluso que algunos fotogramas puedan ser de baja calidad por contener *motion
blur* u otro tipo de anomalías. Por otro lado, soluciones que intenta realizar
*mapeo visual-inercial*  realizan el bundle adjustment sin utilizar todas las
imágenes capturadas, si no que se limitan a la utilización de algunos fotogramas
clave, o *keyframes* elegidos mediante criterios que priorizan cuadros nítidos y
con distancias (*baselines*) prudenciales entre ellos.

Como las muestras de IMU vienen a altas frecuencias, es común que estas se
preintegren de forma tal de combinar muestras simultáneas entre dos keyframes en
una única entrada del optimizador. Sin embargo, un problema en el que esta
integración incurre, es que las mediciones de las IMU son altamente ruidosas, y
acumularlas durante tiempos prolongados acumula también cantidades
significativas de error. Este factor nos limita el tiempo que puede transcurrir
entre dos keyframes; como ejemplo en [1] se habla de keyframes que no pueden
tener más de 0.5 segundos entre sí. A su vez, tener keyframes a muy bajas
frecuencias afecta la calidad de las estimaciones de velocidad y biases; estos
últimos son offsets de medición inherentemente variables de los acelerómetros y
giroscopios a los que es necesario estimar para compensar por ellos en la
medición final.

## Propuesta

La novedad de Basalt es que formula el mapeo visual-inercial como un problema de
bundle adjustment con mediciones visuales e inerciales a altas frecuencias.
Utiliza un *grafo de factores* similarmente a otros sistemas, también llamado
*grafo de poses* en este contexto por contener poses a estimar como nodos. En
lugar de utilizar todos los fotogramas se propone realizar la optimización en
dos capas. La capa de VIO, emplea un sistema de odometría visual-inercial, que
ya de por sí supera a otros sistemas del mismo tipo, proveyendo estimaciones de
movimiento a la misma frecuencia que el sensor de la cámara provee imágenes.
Luego, se seleccionan keyframes y se introducen *factores no-lineales*
entre estos que estiman la diferencia de posición relativa entre estos.
Estos dos factores, keyframes y poses relativas, se utilizan en la capa de
bundle-adjustment global.

La capa de VIO, utiliza features que son rápidas y buenas para tracking
(*optical flow*), mientras que en la capa de mapeo se usan features adecuadas
para *loop closing* que son indiferentes a las condiciones de luz o al punto de
vista de la cámara. De esta forma tenemos un sistema que es capaz de utilizar
las mediciones a alta frecuencias de los sensores y al mismo tiempo tiene la
capacidad de detectar a frecuencias más bajas cuando se está en ubicaciones ya
visitadas, obteniendo así un mapa que es globalmente consistente. Además, el
problema de optimización se reduce, ya que a diferencia de otros sistemas, no es
necesario estimar velocidades ni biases.




[1]: Visual Inertial ORB-SLAM: https://arxiv.org/pdf/1610.05949.pdf
