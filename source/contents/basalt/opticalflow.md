<!-- #### Optical flow {#optical-flow} -->

<!-- TODO@fig: algún gráfico que represente lo que le entra al módulo y lo que
sale, lo mismo para todo el pipeline de VIO, y lo mismo para todo Basalt -->

El módulo de VIO toma dos tipos de entrada, una de ellas son las muestras raw de
la IMU; y la otra, contra intuitivamente, no son las imágenes raw provenientes
de las cámaras, sino que son los _keypoints_ resultantes de ellas. Estos son la posición en dos dimensiones
sobre el plano de la imagen de las _features_ detectadas. Las features a su vez
son la representación de los puntos de interés o _landmarks_ de la escena
tridimensional proyectados sobre las imágenes. El proceso de detectar features,
computar su transformación entre distintos cuadros, y producir los keypoints de
entrada para el módulo de VIO, está a cargo del módulo de _optical flow_ (o
_flujo óptico_). Cabe aclarar que optical flow es el nombre que recibe tanto el
campo vectorial que representa el movimiento aparente de puntos entre dos
imágenes, como el proceso de estimarlo. Este puede ser denso, si se considera el
flujo de todos los píxeles, o no (_sparse_) si solo se computa el flujo de
algunos keypoints como es el caso que veremos.

El módulo de optical flow corre en un hilo
separado y es por donde las muestras del par de cámaras estéreo ingresan al
pipeline de Basalt. Inicialmente se genera una representación piramidal de las
imágenes, o también llamada de _mipmaps_, esta es una forma tradicional
[@williamsPyramidalParametrics1983] de almacenar una imagen en memoria junto a versiones
reescaladas de la misma como se ve en la \figref{fig:mipmap}. Los mipmaps tienen múltiples utilidades en
computación gráfica (p. ej. _filtrado trilineal_, _LODs_, reducción de
_patrones moiré_) pero en el caso de Basalt serán utilizados para darle robustez
al algoritmo de seguimiento de features o _feature tracking_.

\fig{fig:mipmap}{source/figures/mipmap.png}{Mipmaps}{%
Representación piramidal (mipmaps) de un cuadro del conjunto de datos estándar
EuRoC \autocite{burriEuRoCMicroAerial2016}.
}

<!-- #define MN_OPENCV %\
OpenCV es una de las bibliotecas de visión por computadora más populares y
utilizadas en este tipo de sistemas. Combina múltiples algoritmos y presenta
una licencia permisiva Apache 2 \autocite{ApacheLicenseVersion} (prev. BSD-3 \autocite{3ClauseBSDLicense}).
-->

Posteriormente se realiza la detección de features nuevas sobre las imágenes
utilizando el algoritmo _FAST_ [@rostenFasterBetterMachine2010a] para detección
de esquinas, o puntos sobresalientes de la imagen en general (keypoints), implementado
sobre _OpenCV_\marginnote{MN_OPENCV}. Resulta importante aclarar que Basalt es uno de
los sistemas que menos depende de OpenCV, siendo `cv::FAST` el único algoritmo de la
biblioteca en uso durante una ejecución usual. El proyecto
tiende a reimplementar muchas de las técnicas y algoritmia de forma
especializada y, como veremos en otros módulos, otras tareas razonablemente
complejas como la optimización de grafos de poses se implementan también dentro
del proyecto y sin recurrir a bibliotecas externas. Esta es una de las varias
razones por las que el sistema logra tan buen rendimiento, ya que
estas bibliotecas suelen necesitar de campos y comprobaciones generales
del problema que intenta solucionar, mientras que Basalt puede
prescindir de todas las que no apliquen a VIO. Aunque, también es cierto que estas
reimplementaciones añaden complejidad al sistema.

Siguiendo con la
detección de features, una heurística particular de Basalt es la división del
cuadro completo en celdas de, por defecto, 50 por 50 píxeles en donde se
detectan los nuevos puntos de interés. Por celda solo se conserva la feature
de mejor calidad o con mejor _respuesta (response)_, aunque se puede configurar
para detectar más de una. Siempre que la celda tenga alguna
localizada de cuadros anteriores, no se intenta detectar nuevas. Esto contrasta
con sistemas como Kimera-VIO que corren la detección FAST sobre el cuadro entero
y evitan la redetección mediante el uso de _máscaras_ que le instruyen al
algoritmo a obviar esas secciones. Desafortunadamente la construcción de tales
máscaras suele ser costosa y la heurística de Basalt, a pesar de desperdiciar
espacio por no permitir la detección de nuevas características entre celdas, es
más eficiente, ya que en situaciones comunes se logran detectar una cantidad
razonable de features sin problemas. Esta detección se
realiza únicamente sobre la primera cámara, usualmente la izquierda, mientras
que en la otra cámara se reutiliza el método de seguimiento de keypoints que se
describe a continuación.

<!-- TODO@fig: Agregar imágenes de los parches, de la detección de features, del optical flow -->

En cada instante de tiempo que entran un nuevo par de imágenes se tiene acceso a
toda la información recolectada del instante anterior, en particular a sus
keypoints. Una suposición razonable es que las imágenes correspondientes a este
nuevo instante van a compartir muchos de los keypoints con las imágenes
anteriores y en posiciones similares. Con esa suposición Basalt logra
ahorrarse tener que volver a detectar features de la imagen con FAST y en cambio
el problema se transforma en, dado una imagen anterior (inicial), sus keypoints
y una imagen nueva (objetivo), estimar donde ocurren esos mismos keypoints en la
imagen nueva. Para esto, por cada keypoint anterior, se genera un parche
$\Omega$ alrededor de su ubicación de, por defecto, 52 puntos como se ve en el
ejemplo de la \figref{fig:patches}.

\fig{fig:patches}{source/figures/patches.png}{Parches}{%
Ejemplos de los parches de 52 puntos considerados para computar el optical flow
de distintos keypoints de una imagen.
}

Considerando
entonces que este parche debería estar en la imagen nueva en coordenadas
cercanas a las del keypoint anterior, queremos encontrar la transformación $\mathbf{T}
\in SE(2)$ que le ocurrió al parche, y por ende al nuevo keypoint que se
encontraría en el centro de este nuevo parche. Basalt emplea entonces
optimización por cuadrados mínimos mediante el algoritmo iterativo de
Gauss-Newton para encontrar $\mathbf{T}$ utilizando un residual $r$ con:

<!-- TODO@correct: Realmente es gauss newton lo que se hace? ver optical_flow_max_iterations -->
<!-- TODO@correct: Not quite, es inverse-compositional method, que es un gauss newton
sobre algo un poco distinto: https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0910/zhao.pdf
por eso aparece el hessiano y cosas de esa pinta -->
<!-- TODO: Mencionar ZNCC como norma no utilizada: https://martin-thoma.com/zero-mean-normalized-cross-correlation/ -->

$$
r_i =
  \frac{I_{t + 1}(\mathbf{T} \mathbf{x}_i)}{\overline{I_{t + 1}}} -
  \frac{I_{t}(\mathbf{x}_i)}{\overline{I_{t}}}
  \ \ \ \ \forall \mathbf{x}_i \in \Omega
$$

Y aquí siendo $I_t(\mathbf{x})$ la intensidad de la imagen anterior en el pixel ubicado en
las coordenadas $\mathbf{x}$, análogamente $I_{t + 1}(\mathbf{x})$ para la
imagen objetivo; y siendo $\overline{I_{t}}$ la intensidad media del parche
$\Omega$ en la imagen inicial, análogamente $\overline{I_{t + 1}}$ para la
imagen objetivo y el parche transformado $\mathbf{T}\Omega$. Notar que al
normalizar las intensidades obtenemos un valor que es invariante incluso ante
cambios de iluminación.

Los detalles del cálculo de gradientes y jacobianos están basados en el método
de @lucasIterativeImageRegistration1981 para tracking de features (_KLT_). El
uso adicional de mipmaps sobre KLT fue originalmente expuesto en
@bouguetPyramidalImplementationLucas1999.

Para asegurar que la estimación fue exitosa se invierte el problema y se intenta
trackear desde la imagen nueva hacia la inicial y, si el resultado está muy
alejado de la posición inicial, el nuevo keypoint se considera inválido
(un _outlier_) y se lo descarta. Otro detalle a aclarar es que, recordando que la
detección costosa de features con FAST solo ocurría en las imágenes de una de
las cámaras, es posible ahora entender que las features en la segunda cámara
pueden ser “detectadas” con este método menos costoso. Es decir, simplemente se
computa el optical flow desde la imagen de la cámara izquierda a la de la cámara
derecha en el mismo instante de tiempo.

Finalmente, el último de los pasos que ocurre cuando el módulo de optical flow
procesa un cuadro, es el de filtrado de keypoints, en el cual se desproyectan los
keypoints a posiciones en la escena tridimensional y en caso de que el error
de reproyección supere cierto umbral, estos keypoints serán descartados por
considerarse outliers.
