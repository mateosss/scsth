# Plan de Índice

Mi plan de todos los temas que estaría bueno tratar y como distribuirlos.

Notación:

- [TODO]: Puede empezar a hacerse
- [WAIT]: Habría que avanzar sobre los TODOs antes de hacerlo
- [WONTDO]: No se va a hacer
- [AUTO]: Se autogenera
- [WHAT]: Creo que haría falta pero no tengo idea como escribir esta sección
- [UNCERTAIN]: Todavía no estoy seguro si esta sección aplicaría al escrito
- [TOREAD]: Necesita aprenderse o leerse antes de poder escribirlo
- [DOING]: Se está haciendo
- [DRAFT]: Ya está escrito el draft
- [DONE]: Ya se terminó

---

## Índice

- [DONE] Portada
- [TODO] Resumen (y abstract en inglés)
- [AUTO] Índice
- [AUTO] Lista de figuras
- [AUTO] Lista de tablas
- [AUTO] Lista de abreviaturas
- [AUTO] Lista de fragmentos (listings?), algoritmos y otras?
- [DONE] Introducción
  - [DONE] Contexto/motivación (mencionar algo de las comunidades con las que trabajé,
        mencionar que CV es muy trial and error, oversights pueden costar horas)
  - [TODO] Estructura de la tesis
- [TODO] Preliminares y fundamentos teóricos
  - [WONT] IMU: modelos y calibración
    - [WONT] Matriz de alineación
    - [WONT] Proceso de Wiener (random walk & gaussian white noise)
  - [WONT] Cámara: modelos y calibración
    - [WONT] Modelo pinhole (project, unproject, intrinsic parameters, range)
    - [WONT] Modelo de distorsión radial-tangential (Brown-Conrady)
    - [WONT] Modelo de distorsión equidistant / modelo kannala-brandt (que es una camara fisheye)
    - [WONT] Otras características en una cámara (global shutter, vignetting, frequency,
          exposure, gain, hw sync, ver paper TUM-VI para otras caracteristicas)
  - [WONT] Conjuntos de Datos: EuRoC, TUM-VI, Kitti, synthetic datasets (listar
        características particulares, layout de los datasets, utilidad, algunos
        scores, traer tabla comparativa del paper de TUM-VI?)
  - [DONE] Cuadrados mínimos
    - [DONE] Definición del problema no-lineal
    - [DONE] Algoritmo de Gauss-Newton
    - [WONTDO] Algoritmo de Levenberg-Marquardt
  - [DONE] Cuaterniones
  - [DONE] Grupos de Lie para transformaciones 2D y 3D
    - [DONE] Definición
    - [DONE] Operadores (Exp y Log, hat y vee) y Propiedades
    - [DONE] SO(3), SE(3), SO(2), SE(2)
  - [WONT] Grafo de factores
- [TODO] Sistemas Estudiados
  - [DONE] Introducción: Panorama de sistemas (cuales, metricas, rendimiento,
        licencias (GPL), soluciones privativas, comunidades, actividad (graficos de
        actividad/estrellas/etc?), por que se eligieron los sistemas que se
        eligieron)
  - [WONTDO] Kimera
  - [TOREAD|DOING] Basalt
    - [DOING] VIO
      - [DONE] optical flow
      - [DONE] measure
      - [DOING] optimization
      - [DOING] marginalization
    - [WONTDO] VIM
      - [WONTDO] Global map optimization
      - [WONTDO] Non-linear factor recovery
      - [WONTDO] Non-linear factors for distribution approximation
    - [WONTDO] Modelo de Cámara Double Sphere
  - [WONTDO] ORB-SLAM3
- [TODO] Contribuciones (intro: explicar que es monado/openxr/khronos/collabora)
  - [DRAFT] Contexto
  - [DRAFT] Tracking por SLAM para Monado
    - [DRAFT] Interfaz externa (slam_tracker.hpp: what it does, how it works, cv::Mat, dynamic features)
    - [DRAFT] Implementaciones de la interfaz (Forks: Basalt, ORB-SLAM3, Kimera,
          mencionar peculiaridades como el fork de monado para orbslam3, el no uso
          de mapeo global en Basalt, los problemas de Kimera, etc)
    - [DRAFT] Clase adaptadora (t_tracker_slam: pose correction, debug utilities, euroc recorder, etc)
    - [DRAFT] Predicción (explicar los distintos niveles)
    - [DRAFT] Filtrado (explicar los distintos tipos, mencionar kalman?)
  - [DRAFT] Controladores en Monado
    - [DRAFT] Controlador para dispositivos RealSense (rs_source, D455 and others)
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
    - [WONT] cJSON Wrapper
  - [WONT] Contribuciones pendientes
    - [WONT] Autoexposición
    - [WONT] Interpolación de muestras de IMU
    - [WONT] Cámaras OAK-D / Luxonis / Depth-aI
- [TODO] Resultados
- [DONE] Conclusion
- [AUTO] Bibliografía
