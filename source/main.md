<!-- Posibles valores de MODE: DRAFT, RELEASE -->
<!-- #define MODE RELEASE -->

\cleardoublepage
\pagestyle{scrheadings}
\pagenumbering{arabic}

<!-- %\setcounter{page}{90} -->
<!-- % use \cleardoublepage here to avoid problems with pdfbookmark -->
\cleardoublepage
\ctparttext{Esta primera parte está enfocada a intentar entender el problema
encarado en este trabajo. Además de una \italic{introducción} general a algunos
de los conceptos de XR y SLAM, veremos los \italic{fundamentos} que serán
utilizados de referencia a lo largo del escrito.}
<!-- #include contents/fundamentals/fundamentals.md -->

\cleardoublepage
\ctparttext{En esta parte contextualizaremos los distintos sistemas estudiados y
profundizaremos en uno de ellos: \italic{Basalt}. El estudio detallado de una
implementación será particularmente esclarecedor al hilar sin generalizaciones
multitud de métodos y algoritmos utilizados en contextos concretos y con
objetivos bien definidos.}
<!-- #include contents/basalt/basalt.md -->

\cleardoublepage
\ctparttext{Describiremos algunas de las contribuciones clave que fueron
producto de este trabajo. En el proceso se obtendrá un mejor entendimiento de
los problemas comunes de implementación por los que estos sistemas se ven
afectados. Además, veremos las soluciones que se les ha dado a otras
problemáticas que son propias de la localización en tiempo real aplicada a XR.}
<!-- #include contents/contributions/contributions.md -->

\cleardoublepage
\ctparttext{Para cerrar presentaremos algunos resultados que
intentan describir el rendimiento y la precisión logrados en la implementación
actual. Concluiremos con una revisión general de los temas tratados y posibles
líneas de trabajo a considerar para el futuro.}
<!-- #include contents/conclusions/conclusions.md -->

