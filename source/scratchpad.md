# Scratchpad

## Ahora

Instalar linter de repetición de palabras

- ver como approchean los otros
- encarar la tesis un poco como una generalización de estos sistemas?

## En general

- poner un ejemplo de SLAM basico 2d? tutorial de slam
- releerme los papers?
- 4 páginas por día
- en general: encontrar "los nudos centrales", sin vueltas
- introducir conceptos con cursiva

## 1. Introducción

- Que es SLAM
- Que es XR
- Por que SLAM en XR (mención oculus y otros que se vienen)
- problemas específicos de XR vs muchos sistemas de SLAM que son más para cosas
  no tan drásticas (drones, autos, ver EuRoC dataset).
- online SLAM vs full SLAM
- "thesis outline" o una sección que describa de que va cada capítulo

## 2. Marco Teórico

- que la tesis no sea mumbo jumbo de teoría
- teoría: call by need, solo si lo necesito agregarlo. algo que normalmente no
  se recomienda pero le parece "mas saludable" por que no puedo entenderlo tan
  bien al tema en un mes los conceptos necesarios para el pipeline explicados en
  la parte teórica cuando explico la arquitectura, mencionar la teoría
- puedo ir por descripciones de alto nivel
- explicar métricas de evaluación (todavía no tengo nada pensado de como
  evaluar)
- explicar los temas soft del open source también:
  - Ecosistema: Monado, khronos, openxr
  - soluciones contempladas:
    - libres para el proyecto: Basalt, Kimera, ORB-SLAM3, OpenVINS, maplab,
      RTABMAP, OV2SLAM, OpenVSLAM, ProSLAM, granite
    - lo problemático que fue elegir una solución por que los reportes que hacen
      son malos, muchos no reportan tiempos de ejecución (solo estadísticas RMS
      ATE) cuando el el rendimiento de estas soluciones es crucial para sistemas
      XR que corren en dispositivos con grandes limitaciones de computo
    - otras soluciones privativas (arcturus, SLAMCore, realsense t265, nvidia elbrus)
  - licencias problemáticas, GPL, MIT, BSL, BSD (se recomendó hacer incapié)
  - como trabajar con la comunidad, insertarse a un proyecto, relaciones
    interpeersonales
  - enfasis en que no todos los problemas son técnicos: tambien hay legales,
    sociales (y otros?)
- factor graphs vs kalman filters

## 3. Arquitectura(s)

Ver otras tesis como encaran el hablar de estos sistemas, cuanto tiempo le
dedican, en que hacen incapie, solo rejurgitan lo que dicen los papers
originales o agregan comentarios nuevos e interesantes?

- decisiones de los distintos sistemas (Kimera, ORB-SLAM3, Basalt)
  - arquitecturaes, teóricas, algorítmicas
- espacios de diseño explorados
- corrientes históricas de SLAM
- que se hizo
- que se está haciendo
- que se hará
- idea de "mostrar minimalidad":
  - la teoría es minimal o no? que le puedo sacar y sigue andando?
  - el pipeline es robusto o le saco algo y se cae a pedazos?
  - cuales son las partes fundamentales que no podrían faltar en un sistema
    minimal?
- idea interesante: empezar con una arquitectura minimal que muestre los
  componentes fundamentales e ir construyendo sobre eso las mejoras que haya
- la calidad deplorable de algunas implementaciones, que la mala implementación
  académica dificulta el reuso científico y práctico e incluso la
  reproducibilidad

### Kimera-VIO

### ORB-SLAM3

### Basalt

## 4. Implementación

- otros intentos de generalizar arquitecturas de slam (los 3 papers/tesis que vi)
- Mi arquitectura
- Monado
- Que decisiones tomé
- Por qué?
- Se puede bajar un poco más a detalles de implementación acá.
- Acá se habló un poco de esta idea de tener un diseño con múltiples constraints
  de performance y corrección, y que uno no está separado del otro, no son
  independientes. A veces subir performance te rompe corrección y viceversa. O a
  veces ser muy lento es ser incorrecto si es para cosas en tiempo real.

## 5. Resultados

- Comparaciones entre los sistemas
  - Medidas de corrección
  - Medidas de performance

## 6. Referencias

- como manejar las citas: bibtex, bibfile, references.bib, zotero, etc
- si uso el template tengo que citarlo:
  <https://github.com/tompollard/phd_thesis_markdown#citing-the-template>

## Cosas que tengo que responder en algún momento

- que es un IMU (que tipos)
- que es odometría (que tipos)
- cual es la diferencia entre odometría visual-inercial y SLAM
  (<https://docs.nvidia.com/isaac/isaac/packages/visual_slam/doc/index.html>)
- casos de uso de SLAM, otros lugares donde se usa
- loop closure
- GTSAM, g2o, slam++
- otros usos de SLAM
  - robótica
- RMS ATE
- mejorar formato/estilo del documento final
- datasets: EuRoC, TUM-VI, Kitti, OpenLoris?
- ROS? al menos hablar de lo relevante que pareció ser pero que pude
  circunventarlo
- uso de machine learning en SLAM
- oculus insight?
- future work: custom SLAM modules in Monado based (cite thesis on SLAM
  modularity)
- features and landmarks

## Al terminar

- verificar typos
- verifica errores de gramatica
- check markdown and other linter errors

## Historia

Es muy util poder localizar el casco en el espacio en el que se encuentra. SLAM
se usa para esto y Monado no tenía esta funcionalidad. Existe una gran variedad
de implementacines dando vuelta que pueden confundir a un iniciante en el tema.
Este traabajo fue un estudio del área que intentó encontrar las soluciones más
adecuadas para el problema: tanto para XR y como por su licencia. Tres
implementaciones fueron seleccionadas, cada una por distintas razones
contextuales al problema que debería detallar al explicarlas. Primero se eligió
Kimera por haber sido una implementación relativamente reciente que soportaba
stereo y mono VIO bajo una licencia permisiva. Nos topamos con un muy mal
rendimiento tanto en precisión como en performance. Aunque como primera
aproximación sirvió para generar la infraestructura necesaria del lado de Monado
para poder comunicarse con sistemas de SLAM. Dos drivers uno de reproducción de
datasets EuRoC y otro para poder utilizar una cámara D455 como fuente de
muestras para SLAM en tiempo real. Además del tracker y la interfaz y la
implementación de la misma en un fork de Kimera. Luego de tener toda esta
aparotología se siguió por ORB-SLAM3 que venía siendo el ganador
consistentemente en las distintas tablas comparativas en donde aparecía en
distintos papers. ORB-SLAM3 tiene una licencia GPL que fuerza a
proyectos usuarios del sistema a migrar a una licencia open source compatible (y
esto es muchas veces inadmisible para proyectos comerciales, en los cuales
Monado quiere poder ser utilizado). A pesar de esto valía la pena implementarlo
para tener una referencia de que tan bien un sistema podría funcionar.
Efectivamente el sistema es bastante robusto y cuenta con buena performance y
precisión. No está exento de problemas pero cumple su función muy bien.
Finalmente se trabajó sobre Basalt, un sistema de odometría visual-inercial
también con licencia permisiva que fue ignorado originalmente por no presentar
la posibilidad de ser corrido con una única cámara.

# Heurísticas

- Introducción de conceptos con _cursiva_
- También se puede utilizar negrita para dar énfasis en general
- Luego de introducirlas, las palabras en inglés se consideran palabras comunes
- El género de las palabras en inglés es preferentemente el género que tendrían
  al traducirlas, pero si se siente incorrecto, se puede utilizar el otro
  género.
