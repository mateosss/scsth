## Ideas

- [ ] poner un ejemplo de SLAM basico 2d? tutorial de slam
- en general: encontrar "los nudos centrales", sin vueltas

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

# Basalt

- Basalt se ignoró originalmente por que no corría con una sola cámara

## Future Work
- [ ] Idea for a paper: mathematical formulations and a tool to translate
  between camera models. First idea to translate KB into DS, but could be
  between others too.

- [ ] Chapter 2 - Math Fundamentals
  https://www.vectornav.com/resources/inertial-navigation-primer
