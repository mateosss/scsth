---
theme: seriph
class: text-center
highlighter: shiki
lineNumbers: false
colorSchema: light
info: |
  ## Localización visual-inercial en tiempo real para aplicaciones de XR

  Por Mateo de Mayo.

  Más información [aquí](https://github.com/mateosss/scsth).
drawings:
  persist: true
title: Tesis visual-inercial
---

<!-- TODO@mateosss: what's the info field? -->

### *Localización visual-inercial en tiempo real para aplicaciones de XR*

<br>

*Trabajo especial de Licenciatura en Ciencias de la Computación*

| **Autor**  |  Mateo de Mayo |
|---:|:---|
| **Director**  |  Dr. Nicolás Wolovick |
| **Trabajo Completo**  |  [bit.ly/tesis-xr](https://bit.ly/tesis-xr) |

<div width="100%" style="bottom: 0">
<img src="res/famaf-unc.svg" width="200" style="margin: auto"/>

<i>Facultad de Matemática, Astronomía, Física y Computación</i>
<br>
<i>Universidad Nacional de Córdoba</i>
</div>

<style>
  table {
    margin-bottom: 4rem;
  }

  h3 {
    margin-top: 2rem;
    color: var(--slidev-theme-primary) !important;
  }

</style>

<!--
1. Me presento
2. Qué es esta presentación?
3. Presento al tribunal
-->

---
layout: cover
background: none
---
# Demostración 1

Cámara Intel RealSense D455

![](res/realsensed455.jpg)

<style>
  img {
    width: 60%;
    margin: auto;
    margin-top: 5rem;
  }
</style>

---
layout: cover
background: none
---

<iframe style="margin:auto" width="800" height="450" src="https://www.youtube.com/embed/g1o2xADr5Fw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---
layout: cover
background: none
---
# Introducción

Entendiendo el nombre de este trabajo.

---

# XR - Realidad extendida

<center><h3>Localización visual-inercial en tiempo real para aplicaciones de <u>XR</u></h3></center>

![](res/xrspectrum.png)

<div grid="~ cols-2 gap-2" m="-t-2">
<v-click><img src="res/pokemongo.jpg" border="rounded" style="height: 180px"/></v-click>
<v-after><img src="res/beatsaber.jpg" border="rounded" style="height: 180px; margin-left: auto"/></v-after>
</div>

---

# The Khronos Group

<center><h3>Localización visual-inercial en tiempo real para <u>aplicaciones</u> de XR</h3></center>

<br>

<br>

<img src="res/khronos.jpg" border="rounded"/>

<!--
Consorcio de industria sin fines de lucro.
-->
---

# OpenXR

<center><h3>Localización visual-inercial en tiempo real para <u>aplicaciones</u> de XR</h3></center>

<br>
<br>

<img src="res/openxr.png" border="rounded"/>

<!--
Gran adopción (~170 y principales fabricantes)
-->

---

# Monado y Collabora

<center><h3>Localización visual-inercial en tiempo real para <u>aplicaciones</u> de XR</h3></center>

<br>
<br>

<img src="res/openxr.png" border="rounded"/>

<!--
- Consultora open source
- Pasantía de 6 meses
- Integrar soluciones de la academia
-->

---


# Localización - Tracking

<center><h3><u>Localización</u> visual-inercial en tiempo real para aplicaciones de XR</h3></center>

<br>
<br>

<div grid="~ cols-3 gap-2" m="-t-2">
<img src="res/mocap.jpg" border="rounded" style="height: 180px"/>
<img src="res/acoustic-tracking.png" border="rounded" style="height: 180px; margin-left: auto"/>
<img src="res/optitrack-big.png" border="rounded" style="height: 180px; margin-left: auto"/>
<img src="res/lighthouse.jpg" border="rounded" style="height: 180px; margin-left: auto"/>
<img src="res/lighthouse-basestations.jpg" border="rounded" style="height: 180px; margin-left: auto"/>
<img src="res/vive-trackers.jpg" border="rounded" style="height: 180px; margin-left: auto"/>
</div>

<!--
- Optitrack grande 360k USD, chico 10k, una 700 (USD)
- 1 lighhouse 100usd
-->

---

# Visual-inercial - Sensores

<center><h3>Localización <u>visual-inercial</u> en tiempo real para aplicaciones de XR</h3></center>

<br>
<br>
<br>

<div grid="~ cols-3 gap-2" m="-t-2">
<img src="res/camera-sensor.jpg" border="rounded" style="height: 140px; margin: auto"/>
<img src="res/imu.png" border="rounded" style="height: 140px"/>
<img src="res/rpy.jpg" border="rounded" style="height: 140px; margin: auto"/>
</div>

<br>
<br>
<br>

<v-clicks>

- **IMU**: muestras ruidosas propioceptivas con acelerómetro y giroscopio (cf.
  sistema vestibular).
- **Cámaras estéreo**: muestras de referencias exteroceptivas (cf. sistema visual).
- **Sistemas académicos** - SLAM, VIO, SfM.

</v-clicks>

<!--
- sistema vestibular: utrículo y sáculo
- fusion de sensores inteligente
- áreas: CV, optimizacion, probabilidad, filtrado de señales,
-->

---
layout: cover
background: none
---
# Ideas Teóricas

Dos ideas fundamentales: transformaciones y optimización.

---

# Ideas Teóricas

En este trabajo decidimos enfocarnos en dos.

<v-clicks>

- **Transformaciones** - Formalizaciones que nos permiten representar y manipular relaciones espaciales.

- **Cuadrados Mínimos** - Método central de optimización (convexa).

</v-clicks>

---

# Transformaciones

Intuición del concepto.

<img src="res/transforms.svg" style="margin: auto"/>

<v-clicks>

- Traslaciones y rotaciones.
- Posición y orientación.

</v-clicks>

---

# Transformaciones

*Definición:* un grupo es un conjunto $G$ con una operación binaria $\circ : G
\times G \rightarrow G$ tal que $\forall a, b, c \in G$:

<v-clicks>

1. Es cerrada: $a \circ b \in G$
2. Es asociativa: $(a \circ b) \circ c = a \circ (b \circ c)$
3. Tiene neutro: $\exists!\ e \in G: e \circ a = a \circ e = a$
4. Tiene inverso: $\exists a^{-1} \in G: a \circ a^{-1} = a^{-1} \circ a = e$

</v-clicks>

<v-click>

*Esta idea encaja con nuestra intuición de traslaciones, rotaciones y transformaciones.*

</v-click>

<!-- TODO@mateosss: imagen de cubo de rubik -->

---

# Transformaciones

En la práctica usamos las siguientes representaciones.

- **Traslaciones** - Vectores en $\R^n$ (caso $n = 2$ es válido y lo usamos)
- **Rotaciones** - Ángulos Euler, ángulo-axial, cuaterniones, matrices de
  rotación $SO(n)$.
- **Transformaciones** - Matriz homogénea $SE(n)$.
- **Infinitesimales** - Grupos y álgebras de Lie: $SE(n)$, $\mathfrak{se(n)}$, $SO(n)$, $\mathfrak{so(n)}$.

<!-- TODO@mateosss: imagenes que ayuden a entender mejor las representaciones

Grupos y algebras de Lie no son triviales, pero usarlas es mas sencillo y hay algunas demostraciones que ayudan a entenderlo en el escrito.
- Manifold/variedad: al hacer zoom se parece a R^n
- Smooth manifold: no hay partes bruscas
- Grupo de Lie: smooth manifold en donde la operacion del grupo es diferenciable
- Álgebra de Lie: espacio R^n de las posibles "velocidades" sobre la identidad del grupo
-->

---

# Cuadrados Mínimos

Cómo fusionar la información de los distintos tipos de muestras?

<v-clicks>

- En la literatura clásica: filtros Kalman.
- Recientemente: optimización por cuadrados mínimos.
- Un sistema tiene usualmente varios aspectos en los que se puede aplicar optimización:
  - Calibración de los sensores.
  - Reproyección de puntos en la escena (cuando no existe expresión cerrada).
  - Bundle adjustment.
  - Flujo óptico.
  - Alineamiento de trayectorias para métricas.

</v-clicks>

---

# Cuadrados Mínimos - Planteo

Encontrar $\hat{x}$ tal que $E(\hat{x})$ sea mínimo.

$m$ restricciones, estimación $x \in \R^n$, residuales $r_i : \R^n \rightarrow \R$.

$$
E(x) = \sum_{i=1}^m{r_i(x) ^ 2} = \| r(x) \| ^ 2
$$

<v-click>

#### Caso Lineal - $Ax \sim b$

$$
E(x) = \sum_{i=1}^m{(Ax - b)_i^2} = \| Ax - b \| ^ 2
$$

</v-click>

<v-click>

#### Caso no lineal - $f(x) \sim 0$

$$
E(x) = \sum_{i=1}^m{f_i(x)^2} = \| f(x) \| ^ 2
$$

</v-click>

<v-click>

*Correspondencia con estimadores MAP (cf. de máxima verosimilitud)*.

</v-click>

---

# Cuadrados Mínimos - Soluciones

#### Caso Lineal - $Ax \sim b$ - Solución directa.

$$
\begin{align}
\hat{x} &= A^{\dagger} b \nonumber \\
\text{con} \  A^{\dagger} &= (A^T A)^{-1} A^T \nonumber
\end{align}
$$

<v-click>

#### Caso no lineal - $f(x) \sim 0$ - Solución iterativa.

**Dado** $x^{(0)}$ inicial suficientemente cercano a la solución.

1. **Linealizar**. Dado $A_k$ el jacobiano de $f$ alrededor de $x^{(k)}$:

$$
f^{(k)}(x) = f(x^{(k)}) + A_k (x - x^{(k)})
$$

1. **Actualizar**. Resolviendo con la solución para el caso lineal.
$$
x^{(k+1)} = x^{(k)} - A_k^{\dagger} f(x^{(k)})
$$

</v-click>


<v-click>

*Esto es el algoritmo de Gauss-Newton, existen otros: Levenberg-Marquardt, método dogleg de Powell.*

</v-click>

---
layout: cover
background: none
---
# Sistemas Integrados

Y las problemáticas de lidiar con software desarrollado en la academia.

---

# Sistemas

<v-clicks>

1. Muchos sistemas con objetivos varios. Publicaciones con métodos poco claros, bias en las métricas.
2. Sistemas integrados (~25kloc):
    1. **Kimera-VIO**: del MIT, licencia BSD-2 (~200ms).
    2. **ORB-SLAM3**: de la Unizar, licencia GPL-3, supuesto estado del arte (~40ms).
    3. **Basalt**: de la TUM, licencia BSD-3 (~10ms).
3. Basalt el más adecuado para XR.

</v-clicks>

---

# Basalt - Preintegración de muestras de la IMU

Frecuencias y ecuaciones de mecanización.

![](res/sample-frequencies.svg)

$$
\begin{align}
(\Delta \mathbf{R}_{t_i}, \Delta \mathbf{v}_{t_i}, \Delta
\mathbf{p}_{t_i}) := (\mathbf{I}, \mathbf{0}, \mathbf{0})
\\
\Delta \mathbf{R}_{t+1} := \Delta \mathbf{R}_t exp(\mathbf{\omega}_{t+1} \Delta t)\\
\Delta \mathbf{v}_{t+1} := \Delta \mathbf{v}_t + \Delta{\mathbf{R}_t}
\mathbf{a}_{t+1} \Delta t
\\
\Delta \mathbf{p}_{t+1} := \Delta \mathbf{p}_t + \Delta \mathbf{v}_t \Delta t
\\
\Delta \mathbf{s}_{t} := (\Delta \mathbf{R}_{t}, \Delta \mathbf{v}_{t}, \Delta
\mathbf{p}_{t})
\\
\Delta \mathbf{s} := \Delta \mathbf{s}_{t_j}
\end{align}
$$

---

# Basalt - Detección de features

Detección de características de la escena con `cv::FAST`.

<br>
<br>
<br>
<br>
<br>

<div grid="~ cols-1 gap-2" m="-t-2">
<img border="rounded" src="res/fastfeatures.jpg" style="margin: auto"/>
</div>

---

# Basalt - Flujo óptico

Optical flow con el Lukas-Kanade tracker y optimización para encontrar $T \in
SE(2)$ con residuales:

$$
r_i =
  \frac{I_{t + 1}(\mathbf{T} \mathbf{x}_i)}{\overline{I_{t + 1}}} -
  \frac{I_{t}(\mathbf{x}_i)}{\overline{I_{t}}}
  \ \ \ \ \forall \mathbf{x}_i \in \Omega
$$

<div grid="~ cols-1 gap-2" m="-t-2">
<img border="rounded" src="res/basalt-patches.png" style="margin: auto"/>
</div>
---

# Basalt - Flujo óptico

Optical flow con el Lukas-Kanade tracker y optimización para encontrar $T \in
SE(2)$ con residuales:

$$
r_i =
  \frac{I_{t + 1}(\mathbf{T} \mathbf{x}_i)}{\overline{I_{t + 1}}} -
  \frac{I_{t}(\mathbf{x}_i)}{\overline{I_{t}}}
  \ \ \ \ \forall \mathbf{x}_i \in \Omega
$$

<div grid="~ cols-1 gap-2" m="-t-2">
<img border="rounded" src="res/opticalflow.webp" style="margin: auto"/>
</div>

---

# Basalt - Triangulación de landmarks

<img border="rounded" src="res/stereo-triangulation.jpg" style="margin: auto; height:90%"/>

---

# Basalt - Bundle Adjustment

Grafo de factores implícito en Basalt, explícito en otros sistemas con `g2o` o `GTSAM`.

<img border="rounded" src="res/factorgraph.png" style="margin: auto; height:80%"/>

<!-- Aquí ocurre la optimización por gauss newton -->
---
layout: cover
background: none
---
# Contribuciones

Los merge requests que surgieron producto de este trabajo.

---

# `slam_tracker.hpp`

<div class="flex gap-8">
<div class="w-2/3">

```c
class slam_tracker {
public:
  // (1) Constructor y funciones de inicio/fin
  slam_tracker(string config_file);
  void start();
  void stop();

  // (2) Métodos principales de la interfaz
  void push_imu_sample(timestamp t, vec3 accelerometer, vec3 gyroscope);
  void push_frame(timestamp t, cv::Mat frame, bool is_left);
  bool try_dequeue_pose(timestamp &t, vec3 &position, quat &rotation);

  // (3) Características dinámicas opcionales
  bool supports_feature(int feature_id);
  void* use_feature(int feature_id, void* params);

private:
  // (4) Puntero a la implementación (patrón PIMPL)
  void* impl;
}
```

</div>

<div class="w-1/3" v-click>
<ul>
<li>Documenta precondiciones</li>
<li>Forks separados de Monado</li>
<li>Problemas con GPL</li>
<li>ILLIXR Consortium</li>
<li>SLAMBench</li>
</ul>
</div>
</div>

---

# Predicción

Las aplicaciones OpenXR siempre piden información en el futuro.

![](res/prediction-timeline.png)

---

# Predicción de poses

Solución: preintegrar muestras recientes de la IMU.

<div>

![](res/prediction.svg)

</div>

<style>
img {
    position: absolute;
    bottom: -20px;
    width: 90%;
}
</style>

---

# Filtrado de poses

Cómo eliminar el ruido o jitter de las estimaciones.

<iframe src="https://cristal.univ-lille.fr/~casiez/1euro/InteractiveDemo/"/>

<style>
    iframe {
      --zoom: 0.75;
      border: 4px solid var(--slidev-theme-primary);
      border-radius: 5px;
      width: calc(100% * 1 / var(--zoom));
      height: calc(100% * 1 / var(--zoom) - 5rem);
      -ms-zoom: var(--zoom);
      -moz-transform: scale(var(--zoom));
      -moz-transform-origin: 0 0;
      -o-transform: scale(var(--zoom));
      -o-transform-origin: 0 0;
      -webkit-transform: scale(var(--zoom));
      -webkit-transform-origin: 0 0;
    }
</style>

---

# Flujo de datos

<img src="res/dataflow.svg"/>

<style>
img {
  width: calc(100% - 2rem);
  position: absolute;
  left: 1rem;
  top: 10rem;
}
</style>


---
layout: two-cols
---

# Controladores

<v-click>

- Intel RealSense D455
  - Extenderlo más allá de la T265.
  - Global shutter.
  - Cámaras e IMU precalibradas.
  - Modo de muestreo configurable.

</v-click>

<br>

<v-click>

- Windows Mixed Reality - Samsung Odyssey+
  - Ingeniería inversa y trabajo con la comunidad.
  - Calibración poco común (Basalt MR).
  - Cámaras con poco solapamiento.
  - Stereo 640x480@30fps - IMU 4x250Hz.

</v-click>

::right::

<img border="rounded" src="res/devices-ody-d455.jpg"/>
<br>
<img border="rounded" src="res/northstar.jpg">

---
layout: cover
background: none
---
# Demostración 2

Casco Samsung Odyssey+

![](res/odysseyplus.jpg)

<style>
  img {
    width: 60%;
    margin: auto;
    margin-top: 5rem;
  }
</style>

---

# Todo lo demás

Otras contribuciones misceláneas.

1. Modelo radial-tangencial de 8 parámetros para Basalt.
2. Reproductor EuRoC.
3. Capturador EuRoC.
4. Automatización de generación de métricas.
5. Herramientas de análisis de métricas.
6. Datasets personalizados.

---
layout: cover
background: none
---

# Métricas

Algunos resultados que se resumen en: Basalt gana.

---
layout: image
image: ./res/datasets-preview.svg
---
---

# Métricas promedio


|        | BND   | BNF   | BO   | K      | ON     | OO     |
|:-------|:------|:------|:-----|:-------|:-------|:-------|
| Completitud [%] | 100%  | 100%  | 100% | 83.42% | 96.88% | 97.64% |
| Tiempos [ms]  | 1186.25 ± 566.77  | 8.13 ± 1.91   | 13.26 ± 3.86   | 42.69 ± 5.74 | 34.01 ± 8.62  | 36.09 ± 11.86 |
| Error absoluto [m]  | 0.070 ± 0.030 | 0.070 ± 0.030 | 0.072 ± 0.030 | 1935.6 ± 1093.8     | 1.845 ± 1.527  | 0.747 ± 0.508 |
| Error relativo [m]  | 0.007 ± 0.005 | 0.007 ± 0.005 | 0.008 ± 0.007 | 134.727 ± 96.133  | 0.319 ± 0.478 | 0.316 ± 0.272 |

<style>
  table {
    transform: scale(0.86) translate(-8rem, 5rem);
    width: 125% !important;
  }
</style>

---

# Tiempos - Basalt

<br>
<br>
<br>
<br>
<img src="res/timing-basalt.svg" border="rounded"/>

---

# Precisión de tracking - Basalt
.

<img src="res/basalt-trajectory-ate.svg" border="rounded">

<style>
  img {
    height: 400px;
    margin: auto;
  }
</style>

---

# Problema con las métricas usuales ATE/RTE

<img src="res/metrics-are-off.png" border="rounded">

---

# Conclusiones

<v-clicks>

- Los cascos WMR son de los primeros en poder ser con un stack de software completamente libre.
- Todavía hay mucho trabajo por hacer para acercarse a las soluciones propietarias.
- Se sentaron las bases de infraestructura para facilitar este trabajo.

</v-clicks>
