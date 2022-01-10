# Plan de Índice

Mi plan de todos los temas que estaría bueno tratar y como distribuirlos.

Notación:

- [TODO]: Puede empezar a hacerse
- [WAIT]: Habría que avanzar sobre los TODOs antes de hacerlo
- [AUTO]: Se autogenera
- [WHAT]: Creo que haría falta pero no tengo idea como escribir esta sección
- [UNCERTAIN]: Todavía no estoy seguro si esta sección aplicaría al escrito
- [TOREAD]: Necesita aprenderse o leerse antes de poder escribirlo
- [DOING]: Se está haciendo
- [DRAFT]: Ya está escrito el draft
- [DONE]: Ya se terminó

---

## Índice

- [TODO] Portada
- [TODO] Resumen (y abstract en inglés)
- [TODO] Agradecimientos
- [AUTO] Índice
- [AUTO] Lista de figuras
- [AUTO] Lista de tablas
- [AUTO] Lista de abreviaturas
- [TODO] Introducción
  - [TODO] Contexto/motivación (mencionar algo de las comunidades con las que trabajé,
        mencionar que CV es muy trial and error, oversights pueden costar horas)
  - [WHAT] Trabajos relacionados? @thaytan CV1
  - [TODO] Estructura de la tesis
- [TODO] Preliminares y fundamentos teóricos
  - [TODO] IMU: modelos y calibración
    - [DRAFT] Matriz de alineación
    - [TODO] Proceso de Wiener (random walk & gaussian white noise)
  - [TODO] Cámara: modelos y calibración
    - [TODO] Modelo pinhole (project, unproject, intrinsic parameters, range)
    - [WAIT] Modelo de distorsión radial-tangential (Brown-Conrady)
    - [WAIT] Modelo de distorsión equidistant / modelo kannala-brandt (que es una camara fisheye)
    - [TODO] Otras características en una cámara (global shutter, vignetting, frequency,
          exposure, gain, hw sync, ver paper TUM-VI para otras caracteristicas)
  - [TODO] Conjuntos de Datos: EuRoC, TUM-VI, Kitti, synthetic datasets (listar
        características particulares, layout de los datasets, utilidad, algunos
        scores, traer tabla comparativa del paper de TUM-VI?)
  - [WAIT] Cuadrados mínimos
    - [WAIT] Definición del problema no-lineal
    - [WAIT] Algoritmo de Gauss-Newton
    - [WAIT] Algoritmo de Levenberg-Marquardt
  - [TOREAD] Grupos de Lie para transformaciones 2D y 3D
    - [TOREAD] Definición
    - [TOREAD] Operadores y Propiedades
    - [TOREAD] SO(3), SE(3), SO(2), SE(2)
    - [UNCERTAIN|TOREAD] ¿gauss newton / jacobianos en manifolds?
  - [TOREAD] Grafo de factores
  - [TODO] Monado y OpenXR (y Khronos y Collabora)
- [TODO] Sistemas Estudiados
  - [TODO] Introducción: Panorama de sistemas (cuales, metricas, rendimiento,
        licencias (GPL), soluciones privativas, comunidades, actividad (graficos de
        actividad/estrellas/etc?), por que se eligieron los sistemas que se
        eligieron)
  - [TOREAD] Kimera
  - [TOREAD|DOING] Basalt
    - [ ] Modelo de Cámara Double Sphere
  - [TOREAD] ORB-SLAM3
- [TODO] Contribuciones (intro: explicar que es monado/openxr/khronos/collabora)
  - [TODO] SLAM tracker para Monado
    - [TODO] Interfaz externa (slam_tracker.hpp: what it does, how it works, cv::Mat, dynamic features)
    - [TODO] Implementaciones de la interfaz (Forks: Basalt, ORB-SLAM3, Kimera,
          mencionar peculiaridades como el fork de monado para orbslam3, el no uso
          de mapeo global en Basalt, los problemas de Kimera, etc)
    - [TODO] Clase adaptadora (t_tracker_slam: pose correction, debug utilities, euroc recorder, etc)
    - [TODO] Predicción (explicar los distintos niveles)
    - [TODO] Filtrado (explicar los distintos tipos, mencionar kalman?)
  - [TODO] Controladores en Monado
    - [TODO] Controlador para dispositivos RealSense (rs_source, D455 and others)
    - [TODO] Controlador para dispositivos WMR (wmr_source, Odyssey+ and others)
      - [TODO] Atenuación exponencial para sincronización temporal
      - [TODO] Problemas específicos de calibración: camaras con poco solapamiento,
            intrinsics para modelo raro radtan8 (referenciar a las contribuciones
            explicadas abajo)
      - [TODO] Trabajo con la comunidad, ingeniería inversa, thaytan camera
            streams, exposure setting, analisis de exposure en sistema privativo,
            analisis de parámetros extrínsicos, lectura de paquetes USB binarios
    - [TODO] Problemas pendientes (hwclock sync, generic calibration, )
  - [TODO] Otras contribuciones
    - [TODO] Reproductor y grabador de datasets en formato EuRoC
    - [WAIT] Modelo de cámara radtan8 en Basalt (project/unproject and
          jacobians, jacobi solver, OpenCV, newton solver) (habría que hacer avanzar el MR)
    - [WAIT] Offset para cámaras con bajo solapamiento en Basalt (para WMR) (MR no hecho
      todaví)
    - [MAYBENOT] Controlador Qwerty
    - [MAYBENOT] cJSON Wrapper
  - [MAYBENOT] Contribuciones pendientes
    - [MAYBENOT] Autoexposición
    - [MAYBENOT] Interpolación de muestras de IMU
    - [MAYBENOT] Cámaras OAK-D / Luxonis / Depth-aI
- [WHAT|WAIT] Resultados? creo que solo tengo resultados cualitativos como: el video,
  quizás podría replicar resultados online como los de HybVIO en EuRoC. Podría
  testear mis algoritmos de predicción y filtrado haciendo que algunos frames
  (1/4) en EuRoC se skipeen y comparandolos con la version no skipeada?. RMS
  ATE, RTE, ATO, RTO, etc. (hablarlo mejor con nico)
- [TODO] Conclusion
- [AUTO] Referencias
