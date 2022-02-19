## Contexto {#sec:thesis-context}

<!-- TODO@def: Qué es XR? -->

Por su naturaleza, el área de XR involucra una gran cantidad de partes
interconectadas y de dispositivos muy diversos con configuraciones difíciles de
generalizar, y más aún de predecir. Por esta razón hasta hace muy poco tiempo no
existían estándares razonables en el área lo cual agravaba la situación con un
ecosistema altamente fragmentado en soluciones propietarias que causaban a los
desarrolladores de aplicaciones finales grandes problemas. En el mejor de los
casos, la carga de soportar los distintos SDK propietarios recaía sobre
frameworks y motores de juegos (p. ej. _Unreal Engine_, _Unity_, _Godot_) y esto
forzaba a los desarrolladores a elegir alguna de estas soluciones para realizar
su aplicación de XR. En caso de no querer hacerlo, se vería obligado a realizar
un esfuerzo no trivial para portar su aplicación a cada uno de estos SDK,
y eso sin considerar el manejo de características especiales que algunas
plataformas exponen y otras no.

Luego de unos años de sufrir esta fragmentación, en julio de 2019 se presenta la
primera versión de _OpenXR_ de la mano del _Khronos Group_. El Khronos Group es
un consorcio abierto y sin fines de lucro compuesto de 170 organizaciones que
desarrolla estándares en distintas áreas de la industria como computación
gráfica, (_OpenGL_, _Vulkan_), computación paralela (_OpenCL_, _SYCL_) y, con
OpenXR, realidad virtual y aumentada entre otras. OpenXR por su parte, provee
una API estandarizada con soporte para extensiones de fabricante que permiten
añadir características peculiares de ser necesitadas por algún fabricante en
particular. El estándar ha tenido un gran éxito al haber sido adoptado por una
gran cantidad de fabricantes [^openxr-companies] como reemplazo a sus
antiguos SDK propietarios. De esta forma, los motores de juego y desarrolladores
solo necesitan interactuar con una única API (Fig. \figref{fig:openxr}) que además les
permite aprovechar cualquier característica peculiar ofrecida por alguna
extensión.

\fig{fig:openxr}{source/figures/openxr.png}{OpenXR}{%
\bold{Antes de OpenXR} (izquierda) aplicaciones y motores necesitaban código
propietario separado para cada dispositivo en el mercado. \bold{OpenXR} (derecha)
provee una única API multiplataforma de alta performance entre las aplicaciones
y todos los dispositivos compatibles
}

[^openxr-companies]: Compañías respaldando públicamente el estándar OpenXR: <https://www.khronos.org/assets/uploads/apis/2019-openxr-logo-field_1_15.jpg>

OpenXR es exclusivamente la [especificación][openxr-spec] de una API y por lo
tanto requiere una implementación, o _runtime_, sobre el que ser ejecutado. Las
implementaciones son provistas por los distintos fabricantes interesados en
soportar el estándar, en la \figref{fig:openxr-companies} vemos algunas de las
implementaciones ya desarrolladas. En este trabajo nos enfocaremos en una de
ellas, _Monado_. Monado es un runtime (por ahora el único) de la especificación
OpenXR de código abierto, licenciada bajo la _Boost Software License 1.0
([BSL-1.0])_. La plataforma principal sobre la que Monado corre y se desarrolla
es GNU/Linux, pero es capaz de ser ejecutarse en otras como Android y Windows.
Su desarrollo está soportado por _Collabora Ltd._, quien es parte del grupo de
trabajo de OpenXR desde sus inicios. Las contribuciones a Monado listadas en
esta sección fueron hechas durante una pasantía en Collabora.

Además de proveer una implementación de OpenXR, Monado es altamente modular e
implementa distintos componentes reutilizables para XR como un compositor
especializado para realidad virtual; controladores para una gran variedad de
dispositivos, incluyendo hardware propietario y de consumo masivo sobre los que
la comunidad ha realizado ingeniería inversa para poder utilizar; herramientas
varias de calibración y configuración de hardware; así como también distintos
sistemas de fusión de sensores para tracking; y recientemente incluso un módulo
de localización de manos mediante visión por computadora y aprendizaje
automático.

Una característica faltante en Monado era la posibilidad de realizar
localización visual-inercial mediante sistemas de SLAM/VIO. Este tipo de
tracking ha cobrado gran popularidad en los últimos años por resultar sumamente
convenientes al no requerir sensores externos al dispositivo de XR. Sistemas de
este tipo son empleados en productos como el _Meta Quest_, los cascos _Windows
Mixed Reality_ o incluso los SDK _ARCore_ y _ARKit_ presentes en dispositivos
móviles. Desafortunadamente, todas estas soluciones son privativas y, por lo
tanto, no es posible obtener acceso a sus códigos fuentes para reusarlos,
modificarlos o simplemente estudiarlos sin obtener licencias especiales de sus
fabricantes. Más aún, existen compañías que se especializan en desarrollar
soluciones comerciales de SLAM como _SLAMCore[^slam-core]_,
_Arcturus[^arcturus]_ y _Spectacular AI[^spectacular-ai]_ entre otras.

[^slam-core]: <https://www.slamcore.com/>
[^arcturus]: <https://arcturus.industries/>
[^spectacular-ai]: <https://www.spectacularai.com/>

Este trabajo se concentró entonces en el estudio de implementaciones de código
abierto de sistemas de tracking visual-inercial (ya sea mediante SLAM o
solamente VIO) y en la integración de estos sobre Monado. Se necesitó armar la
infraestructura para soportar una interacción modular con los sistemas mediante
el desarrollo de interfaces, herramientas, controladores, y mejoras
principalmente en Monado, pero también en los sistemas a integrar o en sus
_forks_ (clones específicos de las implementaciones de SLAM/VIO para uso en
Monado).

<!-- TODO@def: Ya expliqué qué es el acrónimo VR? -->
<!-- TODO@def: Ya expliqué que es XR no es un acrónimo para "extended"? -->
<!-- TODO@def: SDK, API -->

<!-- TODO@high@ref: Todavía no se como referenciar links en la tesis. edit: ahora sé, hacerlo -->

[openxr-spec]: TODO
[bsl-1.0]: TODO

<!-- TODO@def: Ya explqué que es tracker, tracking? uso esos terminos o me voy a localizar/rastrear/seguir/ubicar/posicionar -->
