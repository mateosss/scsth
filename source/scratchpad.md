# En general

- 4 páginas por día
- en general: encontrar "los nudos centrales", sin vueltas

## 1. Introducción

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
  - licencias problemáticas, GPL, MIT, BSL, BSD (se recomendó hacer incapié)
  - como trabajar con la comunidad, insertarse a un proyecto, relaciones
    interpeersonales
  - enfasis en que no todos los problemas son técnicos: tambien hay legales,
    sociales (y otros?)
- factor graphs vs kalman filters

## 3. Arquitectura

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

## 4. Implementación

- Mi arquitectura
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

## 6. Citas

- como manejar las citas: bibtex, bibfile, references.bib, zotero, etc
- si uso el template tengo que citarlo:
  <https://github.com/tompollard/phd_thesis_markdown#citing-the-template>
