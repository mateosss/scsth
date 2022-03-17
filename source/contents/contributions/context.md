### Contexto {#sec:thesis-context}

Por su naturaleza, el área de XR involucra una gran cantidad de partes
interconectadas y de dispositivos muy diversos con configuraciones difíciles de
generalizar, y más aún de predecir. Por esta razón hasta hace muy poco tiempo no
existían estándares razonables en el área lo cual agravaba la situación con un
ecosistema altamente fragmentado en soluciones propietarias que causaban grandes
problemas a los desarrolladores de aplicaciones finales. En el mejor de los
casos, la carga de soportar los distintos SDK propietarios recaía sobre
frameworks como _WebXR_[^webxr] o motores de juegos (p. ej. _Unreal Engine_, _Unity_, _Godot_[^engines]) y esto
forzaba a los desarrolladores a elegir alguna de estas soluciones para realizar
su aplicación de XR. En caso de no querer hacerlo, se vería obligado a realizar
un esfuerzo significativo para portar su aplicación a cada uno de estos SDK,
y eso sin considerar el manejo de características especiales que algunas
plataformas exponen y otras no. Este escenario se puede ver en la
\figref{fig:before-openxr}.

\fig{fig:before-openxr}{source/figures/before-openxr.pdf}{Antes de OpenXR}{%
Antes de OpenXR las aplicaciones y motores necesitaban código
propietario separado para cada SDK de los dispositivos que quisieran soportar.
}

[^webxr]: <https://www.w3.org/TR/webxr>
[^engines]: <https://www.unrealengine.com>, <https://unity.com> y <https://godotengine.org>

Luego de unos años de sufrir esta fragmentación, en julio de 2019 se presenta la
primera versión de _OpenXR_ [@thekhronosgroupinc.OpenXRSpecification] de la mano del _Khronos Group_[^khronos1]. Este es
un consorcio abierto y sin fines de lucro compuesto de, a la fecha, 170 organizaciones que
desarrolla estándares en distintas áreas de la industria como computación
gráfica (_OpenGL_, _Vulkan_), computación paralela (_OpenCL_, _SYCL_) y, ahora con
OpenXR, realidad virtual y aumentada entre otras. OpenXR provee
una API estandarizada con soporte para extensiones que permiten
añadir características peculiares de ser necesarias por algún fabricante en
particular. El estándar ha tenido un gran éxito al haber sido adoptado por una
gran cantidad de compañías [^openxr-companies] como reemplazo a sus
antiguos SDK propietarios. De esta forma, los motores de juego y desarrolladores
solo necesitan interactuar con una única API que además les
permite aprovechar cualquier característica especial ofrecida por alguna
extensión. Se puede ver la simplificación del esquema de integración con OpenXR
en la \figref{fig:after-openxr}.

[^khronos1]: <https://www.khronos.org>
[^openxr-companies]: Compañías respaldando públicamente el estándar OpenXR: <https://www.khronos.org/assets/uploads/apis/2019-openxr-logo-field_1_15.jpg>

\fig{fig:after-openxr}{source/figures/after-openxr.pdf}{OpenXR}{%
OpenXR provee una única interfaz (API) multiplataforma de alta performance entre las aplicaciones
y todos los dispositivos compatibles. Esto es una mejora en comparación a la
situación presentada en la \figref{fig:before-openxr}.
}

OpenXR es exclusivamente la especificación [@thekhronosgroupinc.OpenXRSpecification] de una API y por lo
tanto requiere una implementación, o _runtime_, sobre el que ejecutarse. Las
implementaciones son provistas por los distintos fabricantes interesados en
soportar el estándar, en la imagen referenciada en la nota al
pie [^openxr-implementations] se pueden ver algunas de las
implementaciones ya desarrolladas. En este trabajo nos enfocaremos en una de
ellas, _Monado_. Monado es un runtime de la especificación
OpenXR de código abierto, por ahora el único con esta característica, licenciado bajo la _Boost Software License 1.0_ [@BoostSoftwareLicensea].
La plataforma principal sobre la que Monado corre y se desarrolla
es GNU/Linux, pero es capaz de ser ejecutarse en otras como Android y Windows.
Su desarrollo está soportado por _Collabora Ltd._, quien es parte del grupo de
trabajo de OpenXR desde sus inicios. Las contribuciones a Monado listadas en
esta sección fueron realizadas durante una pasantía de seis meses realizada por
el autor en Collabora.

[^openxr-implementations]: Algunas de las compañías que implementan un runtime de
OpenXR: <https://www.khronos.org/assets/uploads/apis/OpenXR-After_3.png>.

Además de proveer una implementación de OpenXR, Monado es altamente modular e
implementa distintos componentes reutilizables para XR como un compositor
especializado para realidad virtual; controladores para una gran variedad de
dispositivos, incluyendo hardware propietario y de consumo masivo sobre los que
la comunidad ha realizado ingeniería inversa para poder utilizar; herramientas
varias de calibración y configuración de hardware; así como también distintos
sistemas de fusión de sensores para tracking; recientemente incluso incorpora un módulo
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

<!-- TODO@def: SDK, API -->
