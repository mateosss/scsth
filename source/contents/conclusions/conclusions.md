# Conclusiones

## Resultados {#evaluation}

### Tiempos

<!-- #if 1 -->

\begin{table}[h]
\begin{addmargin*}[-0.2\textwidth]{-0.2\textwidth}
\resizebox{1.4\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
 \multicolumn{7}{c}{Tiempos de ejecución por cuadro [ms]} \\[3pt]
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
\caption[Autem usu id]{Autem usu id.}
\label{tab:moreexamples}
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

### Completitud

<!-- #if 1 -->
\begin{table}[h]
\resizebox{\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
 \multicolumn{7}{c}{Completitud de ejecución} \\[3pt]
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
\caption[Autem usu id]{Autem usu id.}
\label{tab:moreexamples}
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

### Precisión absoluta

<!-- #if 1 -->
\begin{table}[h]
\begin{addmargin*}[-0.2\textwidth]{-0.2\textwidth}
\resizebox{1.4\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
 \multicolumn{7}{c}{Error absoluto de la trayectoria (APE) [m]} \\[3pt]
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
\caption[Autem usu id]{Autem usu id.}
\label{tab:moreexamples}
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

### Precisión relativa

<!-- #if 1 -->
\begin{table}[h]
\begin{addmargin*}[-0.2\textwidth]{-0.2\textwidth}
\resizebox{1.4\textwidth}{!}{
\begin{tabular}{ |l||l|l|l|l|l|l|  }
 \multicolumn{7}{c}{Error relativo de la trayectoria (RPE con intervalos de 6 cuadros) [m]} \\[3pt]
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
\caption[Autem usu id]{Autem usu id.}
\label{tab:moreexamples}
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

\begin{mdframed}[backgroundcolor=shadecolor]
Estuve con esto toda la semana pasada pero tuve un problema en como tomé las
mediciones y tengo que arreglarlo. En general como es algo bastante particular
no es que hay resultados de cosas “definitivas”, es más bien mostrar un poco
cualitativamente con números que tal andan las cosas.

Las medidas que me van a importar son de performance, de precisión de la
trayectoria absoluta y relativa (esta ultima no es comun que se mida pero es muy
importante en XR!).
Ya hice todos los datasets y los scripts para generar los gráficos, pero por un
error que cometí voy a necesitar hacer todas las corridas de vuelta (y eso ahora es un
proceso bastante manual desgraciadamente).

El resumen de los resultados creo que va a ser: Basalt debería dar buenos resultados en
performance y en precisión de movimientos relativos. Mientras que orb-slam3
debería dar mejores resultados en precisión absoluta de la trayectoria por que
hace full SLAM. Kimera-VIO está de adorno.

Como no tengo MoCaps para medir la trayectoria absoluta y comparar (salen unos 10k USD un setup basico \url{https://www.optitrack.com/systems/}),
planeo usar un software que se
llama COLMAP que se toma su tiempo (unas horas de procesamiento) para integrar todas las mediciones en lugar
de ser en tiempo real. Mi esperanza es que esa trayectoria debería ser bastante
razonable como groundtruth, al menos para dar una idea cualitativa de como anda
el sistema.

Si no también está el video \url{https://youtu.be/g1o2xADr5Fw}
\end{mdframed}

## Conclusiones y trabajo futuro

En este trabajo se estudiaron distintos sistemas de SLAM/VIO en el contexto de
localización en tiempo real para XR. Vimos algunos de los conceptos
fundamentales que estos utilizan como el algoritmo de Gauss Newton para resolver
problemas de optimización no lineal, de los cuales el área de visión por
computadora está plagado, y SLAM no es la excepción. También vimos las distintas
formas de representar transformaciones y rotaciones en dos y tres dimensiones:
ángulos euler, cuaterniones, ángulo axial, matrices de rotación y una mirada
práctica sobre los grupos de Lie $SO(n)$ y $SE(n)$ junto a sus álgebras de Lie
$\so(n)$ y $\se(n)$.

Posteriormente nos adentramos en la implementación de la capa de odometría
visual-inercial de Basalt. Esto permitió ver de primera mano los distintos tipos
de algoritmos que se reúnen en este tipo de sistemas. Se integró Kimera-VIO,
ORB-SLAM3 y Basalt a Monado, el runtime OpenXR de código libre. Para esto hizo
falta diseñar una interfaz eficiente que generaliza de forma razonable estos
sistemas. Se analizaron los problemas de implementación particulares a considerar
para XR como la predicción y filtrado de poses, o como lidiar con la
imperfección de los sensores de cámara e IMU. Se contribuyeron a Monado todas
estas mejoras, incluyendo la extensión de dos controladores de dispositivos que
ahora son capaces de aprovechar este tipo de tracking. Uno de ellos es una
plataforma VR de producción comercial que ahora puede ser utilizada por usuarios
entusiastas que deseen utilizar este tipo de hardware en GNU/Linux con un stack
de software completamente libre.

Este proyecto plantea las bases de infraestructura en Monado para este tipo de
sistemas, pero aún hay mucho por hacer y por mejorar para lograr tracking con
calidades similares a las que se encuentran en productos comerciales. Se plantea
como trabajo futuro:\newline

- Mejorar la experiencia de usuario para al utilizar el SLAM tracker en Monado.
  El trabajo realizado actualmente puede resultar un poco complejo de instalar y
  configurar para un usuario inexperto.

- Permitir el uso de múltiples implementaciones de SLAM/VIO de forma dinámica.
  Es decir, poder tener distintas implementaciones corriendo en simultáneo y
  localizando a distintos dispositivos.

- Hay espacio de mejora en el rendimiento de las implementaciones. En general,
  en este trabajo nos limitamos a hacer lo justo y necesario para que el
  tracking funcione a tiempos razonables y no retrase el pipeline de Monado. Más
  aún, parece existir poca cantidad de trabajos que apliquen unidades de cómputo
  masivamente paralelas, como lo son las GPU, al problema de localización
  visual-inercial. Creemos que existen posibles ganancias de eficiencia en esta
  línea de trabajo.

- Sería bueno extender Basalt para soportar algún tipo de mapeo global en tiempo
  real que permita tener trayectorias consistentes que no tiendan a moverse
  lentamente con el tiempo. Discusiones de esto referenciada en una nota al
  pie[^basalt-issue-vim].

- Sería bueno mejorar las formas de testeo y evaluación de sistemas SLAM en
  Monado, poder automatizarlas e integrarlas en los procesos de integración
  continua del proyecto. Esto permitiría el impacto que nuevos cambios traen al
  rendimiento y la precisión del sistema.

- Existen pocos conjuntos de datos para SLAM aptos para XR (p. ej. TUM-VI
  [@schubertBasaltTUMVI2018]), y ante la dificultad de producirlos, sería ideal
  aprovecharse de las herramientas fotorrealistas que son fácilmente accesibles
  en la actualidad para la generación de datos sintéticos.

- Existen métodos de predicción más eficientes que podrían adaptarse a Monado en
  lugar del método ad hoc desarrollado en este trabajo. En particular el mismo
  trabajo de preintegración de muestras de IMU utilizado en Basalt
  [@forsterOnManifoldPreintegrationRealTime2017] puede ser un muy buen punto de
  partida para un método de predicción más preciso.

- Finalmente, muchos de los módulos que forman parte de estos sistemas son
  útiles de manera individual. La integración de estos en Monado podría
  beneficiar a distintos controladores que quieran hacer uso de algoritmia de
  visión por computadora específica en otros contextos.

[^basalt-issue-vim]: <https://gitlab.com/VladyslavUsenko/basalt/-/issues/69>
