## Resultados {#evaluation}

El proceso de evaluar y obtener métricas en sistemas de SLAM/VIO requiere de
ciertas consideraciones. A grandes rasgos, podemos dividir las métricas de
interés usuales en medidas de _precisión_ y de _eficiencia_ que describen,
respectivamente, la exactitud de la trayectoria estimada y el uso de recursos
por parte de los sistemas. Para la evaluación de sistemas se desarrollaron
funcionalidades [^euroc-player] [^euroc-recorder] [^slambatch1] [^slambatch2] y
herramientas [^xrtslam-metrics] dedicadas a la evaluación de sistemas de SLAM en
Monado. Para más información sobre evaluación que la que presentaremos en esta
sección, referimos al lector al trabajo de @kummerleMeasuringAccuracySLAM2009
que detalla en mayor profundidad el proceso de evaluación y a la suite de
herramientas SLAMBench[^slambench] [@nardiIntroducingSLAMBenchPerformance2015]
que intenta generalizarlo para una gran variedad de sistemas.

[^euroc-player]: <https://gitlab.freedesktop.org/monado/monado/-/merge_requests/880>
[^euroc-recorder]: <https://gitlab.freedesktop.org/monado/monado/-/merge_requests/1017>
[^slambatch1]: <https://gitlab.freedesktop.org/monado/monado/-/merge_requests/1152>
[^slambatch2]: <https://gitlab.freedesktop.org/monado/monado/-/merge_requests/1172>
[^xrtslam-metrics]: <https://gitlab.freedesktop.org/mateosss/xrtslam-metrics>
[^slambench]: <https://apt.cs.manchester.ac.uk/projects/PAMELA/tools/SLAMBench>

Para la evaluación se utilizan _conjuntos de datos_ o _datasets_ pregrabados con
distintos dispositivos. Utilizaremos dos datasets populares en el área: _EuRoC_
[@burriEuRoCMicroAerial2016] que es grabado con un _vehículo micro aéreo_
(_MAV_ o _drone_) y _TUM-VI_
[@schubertBasaltTUMVI2018] con muestras provenientes de un dispositivo que es
sostenido con la mano (_handheld_) lo cual lo hace particularmente bueno para
evaluar tracking en aplicaciones de XR. Además, estos conjuntos de datos fueron
tomados con sistemas de captura de movimiento (_MoCap_) externos de gran
precisión pero también de gran costo. Esto les permite presentar una trayectoria
muy precisa que se utiliza como punto de referencia y se la conoce como _ground
truth_.

Además de estos datasets, se presentan datos tomados especialmente para este
trabajo[^custom-datasets] con los dispositivos introducidos en el [](#drivers):
la cámara RealSense D455 y el casco Odyssey+. Se tienen también datos
monoculares del celular móvil Poco X3 Pro capturados con el trabajo de
@huaiMobileARSensor2019 pero no llegaron a utilizarse en estos resultados; es
decir, todos los datos evaluados son con cámaras estéreo. Estos conjuntos
capturados con la D455 y el Odyssey+ no presentan ground truth, pero ofrecen
grabaciones especialmente pensadas para XR y utilizan dispositivos que Monado ya
soporta. En la figura \figref{fig:datasets-preview} se pueden observar algunas
imágenes de los distintos datasets utilizados en al evaluación.

[^custom-datasets]: <https://drive.google.com/drive/folders/163KuF88viW_wPcVNZJ2Onxe7zHf2Qo7L?usp=sharing>

\fig{fig:datasets-preview}{source/figures/datasets-preview.pdf}{Datasets}{%
Imágenes para visualizar el tipo de entorno en el que los datasets de evaluación fueron capturados.
}

Como es usual en este tipo de estudios comparativos, utilizaremos acrónimos para
referirnos a los distintos conjuntos de datos con las siguientes características:
\newline

- C*: Datasets específicos para este trabajo (_custom_). Cada uno presenta dos
  modalidades, la primera EASY tiene movimientos tranquilos similares a los que
  se verían al inspeccionar una habitación. Por otro lado la modalidad HARD
  contiene una sucesión de movimientos agitados e intenta simular momentos de
  acción en un juego. Los sensores utilizados son:
  \newline

  - C6*: RealSense D455 en 640x480 a 30 fps e IMU a 250 Hz.

  - C8*: RealSense D455 en 848x480 a 60 fps e IMU a 250 Hz.

  - CO*: Odyssey+ en 640x480 a 30 fps e IMU a 250 Hz. Para Basalt
    en particular tenemos dos posibles modelos de cámara para utilizar con los lentes de
    este casco. Por defecto se utilizará el modelo radial-tangencial de 8
    parámetros [^basalt-rt8-mr] dado de fábrica pero también se comparará con el
    modelo Kannala-Brandt de 4 parámetros (KB4) recalibrado y nativo en Basalt.

- E*: Los datasets EuRoC en dos habitaciones (V1 y V2) y una sala de máquinas
  (MH) en 752x480 a 20 fps e IMU a 200 Hz.

- T*: TUM-VI en una habitación (R) en 512x512 a 20 fps e IMU a 200 Hz.

[^basalt-rt8-mr]: <https://gitlab.com/VladyslavUsenko/basalt-headers/-/merge_requests/21>

También utilizaremos acrónimos para los distintos sistemas evaluados, que son
variantes de Basalt, Kimera y ORB-SLAM3 dados actualizaciones significativas que
le ocurrieron a Basalt[^basalt-last-important-update] y
ORB-SLAM3[^orbslam3-last-important-update] durante el desarrollo de este
trabajo.

- K: Kimera-VIO
- OO: ORB-SLAM3 original antes de la versión 1.0.
- ON: ORB-SLAM3 nueva versión 1.0.
- BO: Basalt original.
- BNF: Basalt nuevo luego de la actualización presentada en @demmelBasaltSquareRoot2021
  la cual incluye, entre otras cosas, la posibilidad de especificar la precisión
  de punto flotante utilizada. Esta versión utiliza `float`.
- BND: Idéntico al punto anterior pero con precisión `double`.
\newline

[^orbslam3-last-important-update]: <https://github.com/UZ-SLAMLab/ORB_SLAM3/releases/tag/v1.0-release>
[^basalt-last-important-update]: <https://gitlab.com/VladyslavUsenko/basalt/-/commit/24325f2a>

Todas las corridas fueron realizadas sobre un procesador Intel i7-1065G7 con
consumo de hasta 15 W y memoria suficiente; ninguno de los sistemas hace uso de
GPU.

### Completitud

Nuestro primer análisis se encuentra en la \autoref{tab:completion} y se centra
en la capacidad de los sistemas integrados de no presentar fallas fatales
durante las corridas de los conjuntos de datos probados. Esta métrica muestra la
tolerancia a fallas de las distintas implementaciones. La tabla presenta a
Basalt como el más estable mientras que ORB-SLAM3 presenta algunas fallas
ocasionales. Kimera por el otro lado presenta severas fallas incluso en
conjuntos estándares como TUM-VI. Vale la pena aclarar que en la práctica, si
bien Basalt resulta más estable que los otros sistemas, existen situaciones que
pueden hacerlo fallar, particularmente ante la presencia de muestras de baja
calidad durante tiempos prolongados. Es notable que la introducción de los
datasets C* es particularmente desafiante para la estabilidad de los sistemas en
comparación a los conjuntos estándares EuRoC y TUM-VI para los cuales las
implementaciones suelen estar bien probados y configurados por defecto.

<!-- #if 1 -->
\begin{table}[H]
\caption[Completitud de ejecución]{Completitud de ejecución}
\label{tab:completion}
\resizebox{\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
\hline
  \spacedlowsmallcaps{Dataset} & \spacedlowsmallcaps{BND} & \spacedlowsmallcaps{BNF} & \spacedlowsmallcaps{BO}  & \spacedlowsmallcaps{K} & \spacedlowsmallcaps{ON} & \spacedlowsmallcaps{OO}\\[3pt]
 \hline
C6EASY & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
C6HARD & ✓     & ✓     & ✓     & 35.89\% & ✓       & ✓       \\
C8EASY & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
C8HARD & ✓     & ✓     & ✓     & 52.25\% & 56.61\% & 55.86\% \\
COEASY & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
(KB4)  & ✓     & ✓     & ✓     &         &         &         \\
COHARD & ✓     & ✓     & ✓     & ✓       & ✓       & 95.71\% \\
(KB4)  & ✓     & ✓     & ✓     &         &         &         \\
EMH01  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EMH02  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EMH03  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EMH04  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EMH05  & ✓     & ✓     & ✓     & ✓       & ✓       & 96.48\% \\
EV101  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EV102  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EV103  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EV201  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
EV202  & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
TR1    & ✓     & ✓     & ✓     & 40.25\% & ✓       & ✓       \\
TR2    & ✓     & ✓     & ✓     & 38.32\% & ✓       & ✓       \\
TR3    & ✓     & ✓     & ✓     & ✓       & ✓       & ✓       \\
TR4    & ✓     & ✓     & ✓     & 63.58\% & ✓       & ✓       \\
TR5    & ✓     & ✓     & ✓     & 52.67\% & 74.81\% & ✓       \\
TR6    & ✓     & ✓     & ✓     & 52.37\% & ✓       & ✓       \\
\hline
\textbf{Media} & \textbf{100\%} & \textbf{100\%} & \textbf{100\%} & \textbf{83.42\%} & \textbf{96.88\%} & \textbf{97.64\%} \\
\hline
\end{tabular}
}
\end{table}
<!-- #else -->
|        | BND   | BNF   | BO   | K      | ON     | OO     |
|:-------|:------|:------|:-----|:-------|:-------|:-------|
| C6EASY | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| C6HARD | ✓     | ✓     | ✓    | 35.89% | ✓      | ✓      |
| C8EASY | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| C8HARD | ✓     | ✓     | ✓    | 52.25% | 56.61% | 55.86% |
| COEASY | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| (KB4)  | ✓     | ✓     | ✓    |        |        |        |
| COHARD | ✓     | ✓     | ✓    | ✓      | ✓      | 95.71% |
| (KB4)  | ✓     | ✓     | ✓    |        |        |        |
| EMH01  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EMH02  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EMH03  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EMH04  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EMH05  | ✓     | ✓     | ✓    | ✓      | ✓      | 96.48% |
| EV101  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EV102  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EV103  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EV201  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| EV202  | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| TR1    | ✓     | ✓     | ✓    | 40.25% | ✓      | ✓      |
| TR2    | ✓     | ✓     | ✓    | 38.32% | ✓      | ✓      |
| TR3    | ✓     | ✓     | ✓    | ✓      | ✓      | ✓      |
| TR4    | ✓     | ✓     | ✓    | 63.58% | ✓      | ✓      |
| TR5    | ✓     | ✓     | ✓    | 52.67% | 74.81% | ✓      |
| TR6    | ✓     | ✓     | ✓    | 52.37% | ✓      | ✓      |
| Media  | 100%  | 100%  | 100% | 83.42% | 96.88% | 97.64% |
<!-- #endif -->

### Tiempos

En este trabajo nos limitaremos a presentar el tiempo promedio que le toma a
cada sistema devolver la estimación de la pose. Se plantea como trabajo a futuro
la posibilidad de automatizar la medición del consumo de otros recursos como
memoria, energía y capacidad de cómputo. Recordar que los conjuntos de datos
probados presentan cuadros a 20, 30 y 60 fps respectivamente y para lograr
tracking a tiempo real necesitaríamos tiempos de estimación menores a 50, 33 y
16 ms respectivamente.

Viendo la \autoref{tab:timing} vemos que Basalt (BNF) sale ganador con tiempos
bien por debajo de los 16 ms. La versión BND se presenta como curiosidad y
muestra lo ineficiente que es el pipeline cuando se utilizan números `double`;
como veremos en las siguientes tablas el tracking de BNF y BND dan los mismos
resultados de precisión gracias a la técnica introducida en la actualización
[@demmelBasaltSquareRoot2021]. ORB-SLAM3 y Kimera tienen tiempos de ejecución
significativamente mayores indicando que convendría utilizar sensores a menor
frecuencia para estos sistemas si se quieren evitar congestiones. Es necesario
aclarar que los tiempos de ORB-SLAM3 podrían ser mejorados si se evitara
utilizar las configuraciones que vienen por defecto. De la misma manera, la
construcción del mapa en tiempo real de ORB-SLAM3 es pesada y en la nueva
versión (ON) soporta la capacidad construirlo de antemano para luego sólo
ejecutar los módulos de localización y no de mapeo, reduciendo así
considerablemente los tiempos de cómputo. Probar estas configuraciones con
ORB-SLAM3 se deja como trabajo a futuro.

<!-- #if 1 -->

\begin{table}[H]
\caption[Tiempos de ejecución]{Tiempos de ejecución medio por cuadro [ms]}
\label{tab:timing}
\begin{addmargin*}[-0.2\textwidth]{-0.2\textwidth}
\resizebox{1.4\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
\hline
  \spacedlowsmallcaps{Dataset} & \spacedlowsmallcaps{BND} & \spacedlowsmallcaps{BNF} & \spacedlowsmallcaps{BO}  & \spacedlowsmallcaps{K} & \spacedlowsmallcaps{ON} & \spacedlowsmallcaps{OO}\\[3pt]
 \hline
C6EASY & 826.60 ± 441.30   & 5.84 ± 1.38   & 9.05 ± 2.40    & 46.00 ± 6.10 & 36.11 ± 7.67  & 35.09 ± 11.81 \\
C6HARD & 668.75 ± 555.59   & 5.58 ± 1.38   & 9.83 ± 3.01    & 47.45 ± 7.94 & 30.66 ± 9.64  & 32.92 ± 12.41 \\
C8EASY & 940.54 ± 485.31   & 6.93 ± 2.10   & 12.89 ± 13.63  & 49.23 ± 7.37 & 33.69 ± 10.50 & 33.24 ± 10.22 \\
C8HARD & 716.58 ± 579.89   & 6.20 ± 2.46   & 12.60 ± 8.38   & 46.28 ± 7.89 & 35.83 ± 11.75 & 37.43 ± 12.04 \\
COEASY & 873.74 ± 404.36   & 6.17 ± 1.12   & 10.96 ± 2.94   & 37.25 ± 4.94 & 35.40 ± 9.35  & 29.41 ± 9.69  \\
(KB4)  & 734.47 ± 357.71 K & 6.24 ± 1.02 K & 10.92 ± 2.98 K &              &               &               \\
COHARD & 617.47 ± 419.17   & 5.71 ± 1.16   & 12.90 ± 3.83   & 37.31 ± 5.20 & 21.52 ± 7.61  & 23.69 ± 7.98  \\
(KB4)  & 592.62 ± 410.55 K & 5.81 ± 1.02 K & 12.81 ± 3.81 K &              &               &               \\
EMH01  & 2123.22 ± 1118.05 & 10.63 ± 3.22  & 14.17 ± 3.15   & 53.15 ± 7.00 & 30.29 ± 6.63  & 36.73 ± 12.68 \\
EMH02  & 2280.38 ± 1118.44 & 11.16 ± 4.28  & 15.33 ± 5.76   & 53.93 ± 6.05 & 29.29 ± 5.37  & 35.32 ± 10.40 \\
EMH03  & 2184.08 ± 940.11  & 11.02 ± 2.81  & 15.17 ± 3.65   & 53.83 ± 6.05 & 32.09 ± 5.71  & 37.08 ± 12.91 \\
EMH04  & 2117.07 ± 916.61  & 11.82 ± 3.73  & 15.83 ± 3.41   & 53.12 ± 7.19 & 29.77 ± 6.94  & 32.67 ± 11.86 \\
EMH05  & 2187.28 ± 902.72  & 11.17 ± 2.15  & 15.47 ± 3.63   & 53.40 ± 7.07 & 29.04 ± 6.17  & 34.06 ± 15.61 \\
EV101  & 1687.89 ± 524.66  & 10.23 ± 1.76  & 13.62 ± 2.21   & 54.37 ± 6.18 & 30.26 ± 5.95  & 35.43 ± 13.93 \\
EV102  & 1322.72 ± 624.59  & 10.18 ± 2.09  & 15.35 ± 3.63   & 55.48 ± 5.79 & 29.74 ± 6.06  & 32.71 ± 13.47 \\
EV103  & 844.55 ± 609.03   & 11.65 ± 2.56  & 17.31 ± 4.37   & 56.54 ± 6.47 & 34.74 ± 11.43 & 31.13 ± 10.70 \\
EV201  & 1628.73 ± 718.45  & 10.08 ± 1.89  & 15.53 ± 3.04   & 55.00 ± 5.66 & 36.63 ± 11.87 & 32.51 ± 10.04 \\
EV202  & 1296.74 ± 667.75  & 10.65 ± 3.49  & 17.57 ± 4.14   & 55.37 ± 5.24 & 37.77 ± 10.90 & 34.78 ± 11.45 \\
TR1    & 800.61 ± 327.45   & 6.37 ± 1.02   & 12.54 ± 2.70   & 21.34 ± 3.51 & 46.72 ± 11.81 & 44.95 ± 12.33 \\
TR2    & 767.92 ± 287.46   & 6.08 ± 0.93   & 11.47 ± 2.37   & 21.42 ± 2.53 & 44.78 ± 12.06 & 43.94 ± 13.21 \\
TR3    & 697.36 ± 285.12   & 5.96 ± 0.93   & 11.93 ± 2.47   & 23.31 ± 3.69 & 38.33 ± 9.31  & 41.27 ± 11.67 \\
TR4    & 857.84 ± 330.19   & 6.57 ± 1.19   & 11.74 ± 2.38   & 22.62 ± 6.31 & 39.54 ± 10.50 & 42.37 ± 11.85 \\
TR5    & 694.90 ± 308.46   & 6.09 ± 1.01   & 12.53 ± 2.98   & 20.44 ± 3.01 & 32.79 ± 5.37  & 42.42 ± 11.87 \\
TR6    & 1007.87 ± 269.40  & 7.00 ± 1.05   & 10.72 ± 1.80   & 22.33 ± 5.05 & 33.19 ± 6.98  & 44.83 ± 12.68 \\
\hline
\textbf{Media} & \textbf{1186.25 ± 566.77} & \textbf{8.13 ± 1.91} & \textbf{13.26 ± 3.86} & \textbf{42.69 ± 5.74} & \textbf{34.01 ± 8.62} & \textbf{36.09 ± 11.86}\\
\hline
\end{tabular}
}
\end{addmargin*}
\end{table}

<!-- #else -->

|        | BND               | BNF           | BO             | K            | ON            | OO            |
|:-------|:------------------|:--------------|:---------------|:-------------|:--------------|:--------------|
| C6EASY | 826.60 ± 441.30   | 5.84 ± 1.38   | 9.05 ± 2.40    | 46.00 ± 6.10 | 36.11 ± 7.67  | 35.09 ± 11.81 |
| C6HARD | 668.75 ± 555.59   | 5.58 ± 1.38   | 9.83 ± 3.01    | 47.45 ± 7.94 | 30.66 ± 9.64  | 32.92 ± 12.41 |
| C8EASY | 940.54 ± 485.31   | 6.93 ± 2.10   | 12.89 ± 13.63  | 49.23 ± 7.37 | 33.69 ± 10.50 | 33.24 ± 10.22 |
| C8HARD | 716.58 ± 579.89   | 6.20 ± 2.46   | 12.60 ± 8.38   | 46.28 ± 7.89 | 35.83 ± 11.75 | 37.43 ± 12.04 |
| COEASY | 873.74 ± 404.36   | 6.17 ± 1.12   | 10.96 ± 2.94   | 37.25 ± 4.94 | 35.40 ± 9.35  | 29.41 ± 9.69  |
| (KB4)  | 734.47 ± 357.71 K | 6.24 ± 1.02 K | 10.92 ± 2.98 K |              |               |               |
| COHARD | 617.47 ± 419.17   | 5.71 ± 1.16   | 12.90 ± 3.83   | 37.31 ± 5.20 | 21.52 ± 7.61  | 23.69 ± 7.98  |
| (KB4)  | 592.62 ± 410.55 K | 5.81 ± 1.02 K | 12.81 ± 3.81 K |              |               |               |
| EMH01  | 2123.22 ± 1118.05 | 10.63 ± 3.22  | 14.17 ± 3.15   | 53.15 ± 7.00 | 30.29 ± 6.63  | 36.73 ± 12.68 |
| EMH02  | 2280.38 ± 1118.44 | 11.16 ± 4.28  | 15.33 ± 5.76   | 53.93 ± 6.05 | 29.29 ± 5.37  | 35.32 ± 10.40 |
| EMH03  | 2184.08 ± 940.11  | 11.02 ± 2.81  | 15.17 ± 3.65   | 53.83 ± 6.05 | 32.09 ± 5.71  | 37.08 ± 12.91 |
| EMH04  | 2117.07 ± 916.61  | 11.82 ± 3.73  | 15.83 ± 3.41   | 53.12 ± 7.19 | 29.77 ± 6.94  | 32.67 ± 11.86 |
| EMH05  | 2187.28 ± 902.72  | 11.17 ± 2.15  | 15.47 ± 3.63   | 53.40 ± 7.07 | 29.04 ± 6.17  | 34.06 ± 15.61 |
| EV101  | 1687.89 ± 524.66  | 10.23 ± 1.76  | 13.62 ± 2.21   | 54.37 ± 6.18 | 30.26 ± 5.95  | 35.43 ± 13.93 |
| EV102  | 1322.72 ± 624.59  | 10.18 ± 2.09  | 15.35 ± 3.63   | 55.48 ± 5.79 | 29.74 ± 6.06  | 32.71 ± 13.47 |
| EV103  | 844.55 ± 609.03   | 11.65 ± 2.56  | 17.31 ± 4.37   | 56.54 ± 6.47 | 34.74 ± 11.43 | 31.13 ± 10.70 |
| EV201  | 1628.73 ± 718.45  | 10.08 ± 1.89  | 15.53 ± 3.04   | 55.00 ± 5.66 | 36.63 ± 11.87 | 32.51 ± 10.04 |
| EV202  | 1296.74 ± 667.75  | 10.65 ± 3.49  | 17.57 ± 4.14   | 55.37 ± 5.24 | 37.77 ± 10.90 | 34.78 ± 11.45 |
| TR1    | 800.61 ± 327.45   | 6.37 ± 1.02   | 12.54 ± 2.70   | 21.34 ± 3.51 | 46.72 ± 11.81 | 44.95 ± 12.33 |
| TR2    | 767.92 ± 287.46   | 6.08 ± 0.93   | 11.47 ± 2.37   | 21.42 ± 2.53 | 44.78 ± 12.06 | 43.94 ± 13.21 |
| TR3    | 697.36 ± 285.12   | 5.96 ± 0.93   | 11.93 ± 2.47   | 23.31 ± 3.69 | 38.33 ± 9.31  | 41.27 ± 11.67 |
| TR4    | 857.84 ± 330.19   | 6.57 ± 1.19   | 11.74 ± 2.38   | 22.62 ± 6.31 | 39.54 ± 10.50 | 42.37 ± 11.85 |
| TR5    | 694.90 ± 308.46   | 6.09 ± 1.01   | 12.53 ± 2.98   | 20.44 ± 3.01 | 32.79 ± 5.37  | 42.42 ± 11.87 |
| TR6    | 1007.87 ± 269.40  | 7.00 ± 1.05   | 10.72 ± 1.80   | 22.33 ± 5.05 | 33.19 ± 6.98  | 44.83 ± 12.68 |
| Media  | 1186.25 ± 566.77  | 8.13 ± 1.91   | 13.26 ± 3.86   | 42.69 ± 5.74 | 34.01 ± 8.62  | 36.09 ± 11.86 |

<!-- #endif -->

### Precisión de la trayectoria

Para medir la precisión de la trayectoria completa estimada por el sistema se la
compara con las trayectorias ground truth provistas por los datasets. La métrica
usual para representar esta precisión es la _raíz del error cuadrático medio
(RMSE)_ del _error de trayectoria absoluto (ATE)_ que se define de la siguiente
manera [@sturmBenchmarkEvaluationRGBD2012].

Una trayectoria será una secuencia de poses $P_i \in SE(3)$ con $i$ siendo el
tiempo o timestamp en el que la pose ocurrió. Tenemos dos trayectorias que
considerar; la estimada que denotaremos con $P^{est}_i$ y la de referencia o
groud truth que denotaremos con $P^{ref}_i$ con $i=N$ la última timestamp.

El $ATE_i$ entre cada pose $P^{est}_i$ y $P^{ref}_i$ al momento $i$ es la
distancia entre las posiciones de las poses es decir:
\begin{align}
ATE_i = ||pos(P^{est}_i) - pos(P^{ref}_i)||
\end{align}
Con $pos(P) \in \R^3$ el componente de posición o traslación de la pose $P$.
Notar que no se considera el componente de rotación de las poses.
Finalmente utilizamos el RMSE de los ATE al cuadrado:
\begin{align}
RMSE = \sqrt{\frac{1}{N} \sum_{i=1}^{N} ATE_i^2}
\end{align}

Esta es la métrica que se utiliza en esta sección para medir la
precisión en las trayectorias estimadas. Cabe aclarar además que las poses dadas
por la ground truth y las dadas por las estimaciones, en general, no van a
coincidir en sus timestamps y se debe utilizar alguna forma de relacionarlas.
Este trabajo utiliza la biblioteca EVO [@grupp2017evo] y por defecto esta
simplemente utiliza la trayectoria con menos poses y las relaciona a las poses
con timestamps más cercanas de la otra trayectoria. Otro detalle en el proceso
que es estándar en la práctica es alinear previamente las dos trayectorias
minimizando con cuadrados mínimos el error de las mismas con el trabajo de
@umeyamaLeastsquaresEstimationTransformation1991.

Ahora sí, podemos ver los resultados en la \autoref{tab:ate}. En general Basalt
es también superior en estas métricas, pero aquí hay una aclaración importante
que hacer. ORB-SLAM3 es usualmente considerado el estado del arte porque las
métricas que reporta ocurren luego de que los datasets hayan terminado de
procesarse. Esto hace que el mapa utilizado sea el final ya construido, lo cual
afecta retroactivamente a las poses computadas anteriormente. En este caso como
estamos corriendo ORB-SLAM3 en tiempo real y utilizamos las poses que reporta
inmediatamente con el mapa en construcción, estas son mucho peores. Se deja como
trabajo próximo la evaluación de ORB-SLAM3 con el mapa pre construido, creemos
que en este caso deberían verse valores más parecidos a los reportados por la
publicación original del sistema y probablemente sobrepasen a Basalt. También
hay que notar que todos los datasets tienen duraciones menores a 5 minutos, esto
hace que el desvío que se acumula en sistemas como Basalt que no tienen noción
de mapa global no se note tanto. Con esto queremos decir que es usual en Basalt
notar luego de sesiones de uso más largas que el entorno simulado empieza a
cambiar de lugar lentamente a causa de la deriva (_drift_) usuales en sistemas
de VIO y no de SLAM. Se plantea también como trabajo a futuro mejorar este
aspecto de Basalt (ver discusión relacionada[^basalt-slam-issue]).

[^basalt-slam-issue]: <https://gitlab.com/VladyslavUsenko/basalt/-/issues/69>

<!-- #if 1 -->
\begin{table}[H]
\caption[Error en las trayectorias]{Error absoluto de la trayectoria (ATE) [m]}
\label{tab:ate}
\begin{addmargin*}[-0.2\textwidth]{-0.2\textwidth}
\resizebox{1.4\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
\hline
  \spacedlowsmallcaps{Dataset} & \spacedlowsmallcaps{BND} & \spacedlowsmallcaps{BNF} & \spacedlowsmallcaps{BO}  & \spacedlowsmallcaps{K} & \spacedlowsmallcaps{ON} & \spacedlowsmallcaps{OO}\\[3pt]
 \hline
EMH01 & 0.061 ± 0.023 & 0.061 ± 0.023 & 0.087 ± 0.026 & 0.290 ± 0.568   & 0.173 ± 0.230  & 0.216 ± 0.306 \\
EMH02 & 0.043 ± 0.022 & 0.043 ± 0.022 & 0.049 ± 0.023 & 0.127 ± 0.051   & 0.151 ± 0.133  & 0.627 ± 0.811 \\
EMH03 & 0.059 ± 0.019 & 0.059 ± 0.019 & 0.075 ± 0.039 & 0.192 ± 0.056   & 1.797 ± 1.175  & 2.513 ± 1.797 \\
EMH04 & 0.107 ± 0.038 & 0.107 ± 0.038 & 0.099 ± 0.040 & 0.188 ± 0.081   & 0.815 ± 0.517  & 2.065 ± 1.132 \\
EMH05 & 0.139 ± 0.041 & 0.139 ± 0.041 & 0.120 ± 0.041 & 0.206 ± 0.071   & 1.797 ± 0.785  & 3.537 ± 1.868 \\
EV101 & 0.040 ± 0.017 & 0.040 ± 0.017 & 0.040 ± 0.016 & 0.071 ± 0.027   & 9.842 ± 10.408 & 0.179 ± 0.168 \\
EV102 & 0.043 ± 0.013 & 0.043 ± 0.013 & 0.053 ± 0.019 & 0.093 ± 0.039   & 0.600 ± 0.359  & 0.951 ± 0.393 \\
EV103 & 0.049 ± 0.020 & 0.049 ± 0.020 & 0.067 ± 0.026 & 0.182 ± 0.050   & 13.274 ± 9.972 & 0.127 ± 0.105 \\
EV201 & 0.036 ± 0.015 & 0.036 ± 0.015 & 0.031 ± 0.017 & 0.046 ± 0.024   & 0.141 ± 0.130  & 0.098 ± 0.096 \\
EV202 & 0.045 ± 0.021 & 0.045 ± 0.021 & 0.060 ± 0.022 & 0.120 ± 0.041   & 0.323 ± 0.351  & 0.471 ± 0.248 \\
TR1   & 0.096 ± 0.048 & 0.096 ± 0.048 & 0.093 ± 0.042 & 4264.6 ± 2534.0 & 0.081 ± 0.028  & 0.546 ± 0.567 \\
TR2   & 0.067 ± 0.040 & 0.067 ± 0.040 & 0.062 ± 0.030 & 4447.9 ± 2728.6 & 0.087 ± 0.075  & 0.061 ± 0.082 \\
TR3   & 0.110 ± 0.057 & 0.110 ± 0.057 & 0.123 ± 0.063 & 6916.5 ± 4071.1 & 0.076 ± 0.032  & 0.123 ± 0.127 \\
TR4   & 0.050 ± 0.029 & 0.050 ± 0.029 & 0.049 ± 0.022 & 4918.2 ± 2749.4 & 0.105 ± 0.059  & 0.211 ± 0.175 \\
TR5   & 0.160 ± 0.067 & 0.160 ± 0.067 & 0.121 ± 0.051 & 5417.1 ± 2905.8 & 0.159 ± 0.122  & 0.112 ± 0.086 \\
TR6   & 0.018 ± 0.011 & 0.018 ± 0.011 & 0.018 ± 0.009 & 5003.9 ± 2511.9 & 0.105 ± 0.059  & 0.122 ± 0.168 \\
\hline
\textbf{Media} & \textbf{0.070 ± 0.030} & \textbf{0.070 ± 0.030} & \textbf{0.072 ± 0.030} & \textbf{1935.6 ± 1093.8} & \textbf{1.845 ± 1.527} & \textbf{0.747 ± 0.508} \\
\hline
\end{tabular}
}
\end{addmargin*}
\end{table}
<!-- #else -->
|        | BND           | BNF           | BO            | K                   | ON             | OO            |
|:-------|:--------------|:--------------|:--------------|:--------------------|:---------------|:--------------|
| EMH01  | 0.061 ± 0.023 | 0.061 ± 0.023 | 0.087 ± 0.026 | 0.290 ± 0.568       | 0.173 ± 0.230  | 0.216 ± 0.306 |
| EMH02  | 0.043 ± 0.022 | 0.043 ± 0.022 | 0.049 ± 0.023 | 0.127 ± 0.051       | 0.151 ± 0.133  | 0.627 ± 0.811 |
| EMH03  | 0.059 ± 0.019 | 0.059 ± 0.019 | 0.075 ± 0.039 | 0.192 ± 0.056       | 1.797 ± 1.175  | 2.513 ± 1.797 |
| EMH04  | 0.107 ± 0.038 | 0.107 ± 0.038 | 0.099 ± 0.040 | 0.188 ± 0.081       | 0.815 ± 0.517  | 2.065 ± 1.132 |
| EMH05  | 0.139 ± 0.041 | 0.139 ± 0.041 | 0.120 ± 0.041 | 0.206 ± 0.071       | 1.797 ± 0.785  | 3.537 ± 1.868 |
| EV101  | 0.040 ± 0.017 | 0.040 ± 0.017 | 0.040 ± 0.016 | 0.071 ± 0.027       | 9.842 ± 10.408 | 0.179 ± 0.168 |
| EV102  | 0.043 ± 0.013 | 0.043 ± 0.013 | 0.053 ± 0.019 | 0.093 ± 0.039       | 0.600 ± 0.359  | 0.951 ± 0.393 |
| EV103  | 0.049 ± 0.020 | 0.049 ± 0.020 | 0.067 ± 0.026 | 0.182 ± 0.050       | 13.274 ± 9.972 | 0.127 ± 0.105 |
| EV201  | 0.036 ± 0.015 | 0.036 ± 0.015 | 0.031 ± 0.017 | 0.046 ± 0.024       | 0.141 ± 0.130  | 0.098 ± 0.096 |
| EV202  | 0.045 ± 0.021 | 0.045 ± 0.021 | 0.060 ± 0.022 | 0.120 ± 0.041       | 0.323 ± 0.351  | 0.471 ± 0.248 |
| TR1    | 0.096 ± 0.048 | 0.096 ± 0.048 | 0.093 ± 0.042 | 4264.6 ± 2534.0     | 0.081 ± 0.028  | 0.546 ± 0.567 |
| TR2    | 0.067 ± 0.040 | 0.067 ± 0.040 | 0.062 ± 0.030 | 4447.9 ± 2728.6     | 0.087 ± 0.075  | 0.061 ± 0.082 |
| TR3    | 0.110 ± 0.057 | 0.110 ± 0.057 | 0.123 ± 0.063 | 6916.5 ± 4071.1     | 0.076 ± 0.032  | 0.123 ± 0.127 |
| TR4    | 0.050 ± 0.029 | 0.050 ± 0.029 | 0.049 ± 0.022 | 4918.2 ± 2749.4     | 0.105 ± 0.059  | 0.211 ± 0.175 |
| TR5    | 0.160 ± 0.067 | 0.160 ± 0.067 | 0.121 ± 0.051 | 5417.1 ± 2905.8     | 0.159 ± 0.122  | 0.112 ± 0.086 |
| TR6    | 0.018 ± 0.011 | 0.018 ± 0.011 | 0.018 ± 0.009 | 5003.9 ± 2511.9     | 0.105 ± 0.059  | 0.122 ± 0.168 |
| Media  | 0.070 ± 0.030 | 0.070 ± 0.030 | 0.072 ± 0.030 | 1935.6 ± 1093.8     | 1.845 ± 1.527  | 0.747 ± 0.508 |
<!-- #endif -->

### Precisión de los movimientos

Finalmente presentamos en la \autoref{tab:rte} el RMSE del _error relativo de la
trayectoria (RTE)_. Este error es capaz de representar las imprecisiones en
tramos cortos de la trayectoria. Una forma de pensar esto en el contexto de XR
es qué tan mal se sentirán los movimientos individuales realizados por un
usuario.

Para definir este error primero dividimos la trajectoria $P_k$ en vectores
definidos entre pares de timestamps $i$ y $j$:
\begin{align}
\delta_{ij} = pos(P_j) - pos(P_i) \ \in \R^3
\end{align}
Luego, definimos el error de traslación entre las timestamps $i$ y $j$ como:
\begin{align}
RTE_{ij} = ||\delta^{ref}_{ij} - \delta^{est}_{ij}||
\end{align}
Y finalmente el RMSE RTE queda definido como:
\begin{align}
RMSE = \sqrt{\frac{1}{N} \sum_{\forall i, j} RTE_{ij}^2}
\end{align}
Notar que aquí la elección de que tan largo son los vectores $\delta_{ij}$ puede
variar. En nuestro caso, usando EVO, utilizamos vectores con timestamps
separadas por el equivalente tiempo a 6 cuadros de cada dataset, es decir unos
0.3, 0.2, y 0.1 segundos para 20, 30 y 60 fps.

<!-- #if 1 -->
\begin{table}[H]
\caption[Error en los movimientos]{Error relativo de la trayectoria (RTE, intervalos de 6 cuadros) [m]}
\label{tab:rte}
\begin{addmargin*}[-0.2\textwidth]{-0.2\textwidth}
\resizebox{1.4\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
\hline
  \spacedlowsmallcaps{Dataset} & \spacedlowsmallcaps{BND} & \spacedlowsmallcaps{BNF} & \spacedlowsmallcaps{BO}  & \spacedlowsmallcaps{K} & \spacedlowsmallcaps{ON} & \spacedlowsmallcaps{OO}\\[3pt]
 \hline
EMH01 & 0.004 ± 0.003 & 0.004 ± 0.003 & 0.004 ± 0.003 & 0.069 ± 0.283     & 0.138 ± 0.113 & 0.137 ± 0.110 \\
EMH02 & 0.004 ± 0.002 & 0.004 ± 0.002 & 0.004 ± 0.003 & 0.019 ± 0.019     & 0.140 ± 0.094 & 0.147 ± 0.167 \\
EMH03 & 0.009 ± 0.008 & 0.009 ± 0.008 & 0.010 ± 0.008 & 0.038 ± 0.030     & 0.368 ± 0.398 & 0.385 ± 0.460 \\
EMH04 & 0.010 ± 0.008 & 0.010 ± 0.008 & 0.011 ± 0.009 & 0.043 ± 0.031     & 0.335 ± 0.281 & 0.341 ± 0.392 \\
EMH05 & 0.009 ± 0.006 & 0.009 ± 0.006 & 0.010 ± 0.007 & 0.041 ± 0.030     & 0.307 ± 0.308 & 0.365 ± 0.660 \\
EV101 & 0.011 ± 0.006 & 0.011 ± 0.006 & 0.011 ± 0.006 & 0.044 ± 0.024     & 0.222 ± 1.958 & 0.136 ± 0.080 \\
EV102 & 0.011 ± 0.005 & 0.011 ± 0.005 & 0.011 ± 0.005 & 0.040 ± 0.022     & 0.277 ± 0.183 & 0.276 ± 0.188 \\
EV103 & 0.011 ± 0.007 & 0.011 ± 0.007 & 0.014 ± 0.009 & 0.039 ± 0.025     & 0.358 ± 2.249 & 0.246 ± 0.173 \\
EV201 & 0.003 ± 0.002 & 0.003 ± 0.002 & 0.003 ± 0.002 & 0.015 ± 0.012     & 0.092 ± 0.064 & 0.097 ± 0.081 \\
EV202 & 0.007 ± 0.006 & 0.007 ± 0.006 & 0.012 ± 0.025 & 0.025 ± 0.018     & 0.219 ± 0.148 & 0.221 ± 0.160 \\
TR1   & 0.007 ± 0.005 & 0.007 ± 0.005 & 0.008 ± 0.006 & 384.484 ± 305.665 & 0.505 ± 0.288 & 0.524 ± 0.294 \\
TR2   & 0.006 ± 0.005 & 0.006 ± 0.005 & 0.007 ± 0.006 & 468.756 ± 475.490 & 0.492 ± 0.421 & 0.503 ± 0.421 \\
TR3   & 0.005 ± 0.004 & 0.005 ± 0.004 & 0.006 ± 0.005 & 262.503 ± 201.940 & 0.618 ± 0.488 & 0.624 ± 0.486 \\
TR4   & 0.005 ± 0.005 & 0.005 ± 0.005 & 0.005 ± 0.005 & 342.893 ± 179.226 & 0.295 ± 0.161 & 0.300 ± 0.164 \\
TR5   & 0.009 ± 0.007 & 0.009 ± 0.007 & 0.010 ± 0.008 & 341.326 ± 155.828 & 0.477 ± 0.284 & 0.483 ± 0.285 \\
TR6   & 0.003 ± 0.002 & 0.003 ± 0.002 & 0.003 ± 0.002 & 355.299 ± 219.485 & 0.268 ± 0.214 & 0.275 ± 0.227 \\
\hline
\textbf{Media} & \textbf{0.007 ± 0.005} & \textbf{0.007 ± 0.005} & \textbf{0.008 ± 0.007} & \textbf{134.727 ± 96.133} & \textbf{0.319 ± 0.478} & \textbf{0.316 ± 0.272} \\
\hline
\end{tabular}
}
\end{addmargin*}
\end{table}
<!-- #else -->
|        | BND           | BNF           | BO            | K                 | ON            | OO            |
|:-------|:--------------|:--------------|:--------------|:------------------|:--------------|:--------------|
| EMH01  | 0.004 ± 0.003 | 0.004 ± 0.003 | 0.004 ± 0.003 | 0.069 ± 0.283     | 0.138 ± 0.113 | 0.137 ± 0.110 |
| EMH02  | 0.004 ± 0.002 | 0.004 ± 0.002 | 0.004 ± 0.003 | 0.019 ± 0.019     | 0.140 ± 0.094 | 0.147 ± 0.167 |
| EMH03  | 0.009 ± 0.008 | 0.009 ± 0.008 | 0.010 ± 0.008 | 0.038 ± 0.030     | 0.368 ± 0.398 | 0.385 ± 0.460 |
| EMH04  | 0.010 ± 0.008 | 0.010 ± 0.008 | 0.011 ± 0.009 | 0.043 ± 0.031     | 0.335 ± 0.281 | 0.341 ± 0.392 |
| EMH05  | 0.009 ± 0.006 | 0.009 ± 0.006 | 0.010 ± 0.007 | 0.041 ± 0.030     | 0.307 ± 0.308 | 0.365 ± 0.660 |
| EV101  | 0.011 ± 0.006 | 0.011 ± 0.006 | 0.011 ± 0.006 | 0.044 ± 0.024     | 0.222 ± 1.958 | 0.136 ± 0.080 |
| EV102  | 0.011 ± 0.005 | 0.011 ± 0.005 | 0.011 ± 0.005 | 0.040 ± 0.022     | 0.277 ± 0.183 | 0.276 ± 0.188 |
| EV103  | 0.011 ± 0.007 | 0.011 ± 0.007 | 0.014 ± 0.009 | 0.039 ± 0.025     | 0.358 ± 2.249 | 0.246 ± 0.173 |
| EV201  | 0.003 ± 0.002 | 0.003 ± 0.002 | 0.003 ± 0.002 | 0.015 ± 0.012     | 0.092 ± 0.064 | 0.097 ± 0.081 |
| EV202  | 0.007 ± 0.006 | 0.007 ± 0.006 | 0.012 ± 0.025 | 0.025 ± 0.018     | 0.219 ± 0.148 | 0.221 ± 0.160 |
| TR1    | 0.007 ± 0.005 | 0.007 ± 0.005 | 0.008 ± 0.006 | 384.484 ± 305.665 | 0.505 ± 0.288 | 0.524 ± 0.294 |
| TR2    | 0.006 ± 0.005 | 0.006 ± 0.005 | 0.007 ± 0.006 | 468.756 ± 475.490 | 0.492 ± 0.421 | 0.503 ± 0.421 |
| TR3    | 0.005 ± 0.004 | 0.005 ± 0.004 | 0.006 ± 0.005 | 262.503 ± 201.940 | 0.618 ± 0.488 | 0.624 ± 0.486 |
| TR4    | 0.005 ± 0.005 | 0.005 ± 0.005 | 0.005 ± 0.005 | 342.893 ± 179.226 | 0.295 ± 0.161 | 0.300 ± 0.164 |
| TR5    | 0.009 ± 0.007 | 0.009 ± 0.007 | 0.010 ± 0.008 | 341.326 ± 155.828 | 0.477 ± 0.284 | 0.483 ± 0.285 |
| TR6    | 0.003 ± 0.002 | 0.003 ± 0.002 | 0.003 ± 0.002 | 355.299 ± 219.485 | 0.268 ± 0.214 | 0.275 ± 0.227 |
| Media  | 0.007 ± 0.005 | 0.007 ± 0.005 | 0.008 ± 0.007 | 134.727 ± 96.133  | 0.319 ± 0.478 | 0.316 ± 0.272 |
<!-- #endif -->

### Resultados específicos

Presentamos a continuación algunos gráficos para dar una idea cualitativa del
funcionamiento de los sistemas. Las figuras fueron obtenidas utilizando BNF, ON
y K sobre el dataset EV201 que es correctamente procesado por las tres
implementaciones. La \figref{fig:timing-comparisson} presenta una comparación de
tiempos de procesamiento. La \figref{fig:trajectories-comparisson-3d} muestra la
forma general de las trayectorias estimadas mientras que la
\figref{fig:trajectories-comparisson-2d} presenta algunos detalles sobre
ORB-SLAM3. Por último se pueden ver los valores de $ATE_i$ en los distintos
tiempos de la trayectoria de Basalt (BNF) en la
\figref{fig:basalt-trajectory-ate}.

\fig{fig:timing-comparisson}{source/figures/timing-comparisson.png}{Tiempos de cómputo}{%
Tiempos de cómputo de BNF, ON y K sobre el dataset EV201. Notar que Basalt tiene
más información sobre las distintas etapas de su pipeline interna simplemente
porque fue el más estudiado. Notar que ORB-SLAM3 presenta problemas de
congestión y que los tiempos de Kimera son bastante estables en comparación a
Basalt a pesar de ser mayores. Por no usar OpenCV, Basalt requiere (por ahora)
copiar los cuadros de entrada y ese tiempo puede visualizarse en rosa en el gráfico.
}

\fig{fig:trajectories-comparisson-3d}{source/figures/trajectories-comparisson-3d.pdf}{Trayectorias 3D}{%
Trayectorias de los tres sitemas comparados a la groundtruth. Considerar que
estas trayectorias están alineadas con Umeyama para minimizar sus diferencias y
por esta razón no coinciden sus inicios ni finales.
}

\fig{fig:trajectories-comparisson-2d}{source/figures/trajectories-comparisson-2d.pdf}{Trayectorias 2D}{%
Vista del plano XY de la trayectoria a derecha. A izquierda se hace zoom a una
porción de la trayectoria para mostrar cómo un momento de loop closure que en
ORB-SLAM3 cuando el mapa fue actualizado durante la corrida genera una
corrección brusca que es indeseable en XR.
}

\fig{fig:basalt-trajectory-ate}{source/figures/basalt-trajectory-ate.pdf}{ATE de Basalt}{%
Abajo se muestra el error $ATE_i$ para cada timestamp $i$ de Basalt. Además este error
se mapea en el color de la trayectoria en la figura de arriba.
}
<!--
TODO: More ideas

AR Datasets:
- AR datasets (referenced in HybVIO paper)
- http://vr-ih.com/vrih/resource/article/unzip/1555468247915/2018.0011/2018.0011/2018.0011_NormalPdf.pdf
- https://github.com/AaltoVision/ADVIO

COLMAP:
- Idea of using COLMAP as ground truth for custom datasets?
- Este paper tiene una forma similar de generar groundtruth con offline processing:
  https://www.researchgate.net/publication/312019498_ON_CONSTRUCTION_OF_A_RELIABLE_GROUND_TRUTH_FOR_EVALUATION_OF_VISUAL_SLAM_ALGORITHMS
- https://arxiv.org/pdf/2202.08894.pdf: "COLMAP is able to reconstruct an
  accurate trajectory on every sequence of this dataset. For this
  reason, including the inertial measurements in the estimation
  process does not bring any significant benefit."
-->
