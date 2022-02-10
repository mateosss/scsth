------------

From section II of the Kimera paper [kimera], its implementation can be described with the following procedures.
Note that much of the jargon still needs to be studied.

1. VIO Frontend: processes raw sensor data
  1. IMU: On-manifold preintegration between keyframes ([OMP])
  2. Vision: At each keyframe does a, c, and d while b is done for in-between frames.
    1. Detects Shi-Tomasi corners
    2. Tracks them with Lukas-Kanade tracker
    3. Finds left-right stereo matches
    4. Performs Geometric verification
      - Mono with 5-point RANSAC or
      - Stereo with 3-point RANSAC
      - Optionally use IMU rotation for 2- and 1-point RANSAC respectively
2. VIO Backend: manages the factor graph (can be thought of as a graph of all processed measurements)
  1. Updates the factor graph (usually "fixed-lag smoother" but can optionally be "full-smoothing") in realtime with preintegrated IMU and visual measurements (frontend output)
  2. Uses processed IMU and vision models from [OMP] (implemented in gtsam)
  3. Solves the factor graph with iSAM2 from gtsam. At each iSAM2 iteration:
    - Vision model ("structureless" [OMP])
      1. Estimate 3D position of 2D features (uses [DLT])
      2. Degenerate points (without enough information) removed
      3. Outlier points (large "reprojection error") removed
      4. Eliminates corresponding 3D feature points from VIO state (?)
      5. States outside "smoothing horizon" discarded with gtsam.
3. Kimera-RPGO: Robust Pose Graph Optimization module. It is a separate component that provides loop closure (LC) and consistency of poses.
  1. Loop closure detection:
    - Uses DBoW2, which uses bag-of-word method for detecting possible LCs.
    - Reject some outlier LCs with geometric verification from the frontend, outliers due to perceptual aliasing can remain.
    - Pass remaining LCs to the Robust PGO described below.
  2. Robust PGO:
    1. Store odometry (factor graph edges) from Kimera-VIO
    2. Store loop closures
    3. Select consistent LCs (with a customized [PCM] method detailed in the Kimera [paper][kimera])
    4. Run gtsam over the factor graph and loop closures.



[OMP]: https://arxiv.org/pdf/1512.02363.pdf
[DLT]: https://en.wikipedia.org/wiki/Direct_linear_transformation
[PCM]: http://robots.engin.umich.edu/publications/jmangelson-2018a.pdf
[kimera]: https://arxiv.org/pdf/1910.02490.pdf

---

The Kimera `Pipeline` has a `VisionImuFrontend` that is its frontend.
Furthermore, this class has an `ImuFrontend` which purely manages the sensor
"preintegration". This process, also called sensor fusion in other contexts, is
about having some kind of estimator for unknown variables of interest (like the
pose and velocity of the robot) that are progressively updated with new
measurements.

This "aggregator" (or integrator) of measurements is located in
`ImuFrontend.pim_` (short for preintegration measurements). Each IMU measurement
of accelerometer and gyroscope data is fed into the `pim` alongside its time
delta. This preintegrator then uses some method for updating its internal
information, and can at any point be queried for its estimation of the robot's
velocity and pose (location and rotation). The authors of Kimera have
implemented their own research algorithm `ManifoldPreintegration` into GTSAM and
so Kimera is using it directly from GTSAM. In later versions of GTSAM a new
algorithm Tangent Preintegration [seems to
supersede](https://gtsam.org/notes/IMU-Factor.html) the `ManifoldPreintegration`
though Kimera is still using it.

An important explanation for GTSAM is that it stores what is called a //[factor
graph](https://gtsam.org/2020/06/01/factor-graphs.html)// which is just a graph
which has the estimated //variables// as its vertices (in this case the
landmarks and robot measured poses), and its //factors// as edges. The factors
of these graphs would be any "relationship" between variables, and in the
context of SLAM, the different measurements that affect the estimation of the
robot's position like the robot's own internal IMU measurements //(odometry)//
and the positions of the landmarks, would be the factors/edges in the graph.
Hopefully [this image](https://gtsam.org/assets/fg-images/image1.png) makes it
clearer, the cyan dots represent the estimated robot positions during the
trajectory, and the blue dots the estimated fixed landmarks position.

As of now the `ImuFrontend` only adds IMU measurements to the `pim`, this will
most likely be used by the backend to get estimations for the robot odometry
steps, and each of these steps will be a factor/edge in the graph (like the
edges that connect each cyan dot in the
[image](https://gtsam.org/assets/fg-images/image1.png)).

There is more theory to go into like [manifolds and Lie
groups](https://gtsam.org/notes/GTSAM-Concepts.html) but for now, this level of
detail for this component is good enough.

---

After the `ImuFrontend` updates the `pim` with the sensor measurements, the
frontend can use the `pim` estimations to know the relative rotation of the
camera since the last frame. This rotation alongside the current frame (the
frame image itself) is passed to the `MonoVisionImuFrontend::processFrame()`
method (or the analogous for stereo) which is the last core step the Kimera
frontend has to do before passing its results to the backend.

`processFrame` does the processing of the camera images and corresponds to the
second point of this task description.

Let's suppose Kimera is already running and features of previous frames have
been already detected. When a new frame is consumed by the frontend, the first
thing `processFrame` will do is feature tracking. For this, Kimera implements a
`Tracker` class with a `featureTracking` method that takes as arguments the
previous and current frame alongside the frames delta rotation estimated from
the `pim`. The previous frame already has features or keypoints detected, they
are 2D floats (Kimera [does
not](https://github.com/MIT-SPARK/Kimera-VIO/blob/641576fd86bdecbd663b4db3cb068f49502f3a2c/include/kimera-vio/frontend/Frame.h#L179-L180)
currently use descriptors), these previous keypoints will be used as the
starting point to compute the keypoints in the new image (the "optical flow").
The tracking method that computes the new keypoints will be
[cv::calcOpticalFlowPyrLK](https://docs.opencv.org/3.4/dc/d6b/group__video__track.html#ga473e4b886d0bcc6b65831eb88ed93323)
which is the Lukas-Kanade (LK) tracker using a
["pyramidal"](https://www.semanticscholar.org/paper/Pyramidal-implementation-of-the-lucas-kanade-Bouguet/aa972b40c0f8e20b07e02d1fd320bc7ebadfdfc7?p2df)
performance optimization. Before calling it, it predicts where the new points
should be with `predictSparseFlow` which uses the rotation given by the `pim`,
this prediction is then passed as the initial value for the iterative LK
tracker. For each one of the previous keypoints, the algorithm returns a new
keypoint if it can find it and also an `error` flat of how accurate the new
keypoint might be (Kimera is not using this `error`, they have a
[To Do](https://github.com/MIT-SPARK/Kimera-VIO/blob/641576fd86bdecbd663b4db3cb068f49502f3a2c/src/frontend/Tracker.cpp#L132)
on that). Once the new keypoints are predicted, they are saved into the current
`Frame` container for usage in the next frame. They are also displayed in the
visualizer.

## In the next comments, I will talk more about other sections of `processFrame`.

After doing the feature tracking from the last to the current frame, i.e.
determining the correspondent keypoint locations in the new frame,
`processFrame` does what is called //geometric verification// (GV) between the
last **key**frame and the current frame. GV in this context will be the task of
determining the camera position given the two sets of keypoints (for the
keyframe and current frame) and Kimera can use many of the OpenGV solvers that
do this (GV in OpenGV means geometric //vision//).

GV is a similar problem to the Perspective-//n//-Point which given //n// 3D
landmarks positions and their 2D projections determine the location of the
viewing camera. However, here we don't really have the 3D positions of the
landmarks, only their 2D projection keypoints. What Kimera then does is:

1. **Undistorts the keypoints:** by using `cv::undistortPoints`. Very roughly
   stated undistorting is a procedure that should "clean" the keypoints of any
   deformation that the camera physical properties introduce. These properties
   are specified in configuration files before execution and can be obtained for
   a particular camera setup by using something like
   [Kalibr](https://github.com/ethz-asl/kalibr).

2. **Obtain 3D "Bearing Vectors":** once an undistorted keypoint (x, y), the 3D
   vector (x, y, 1) normalized acts as a //bearing vector// which is a 3D vector
   that points from the camera center towards the landmark in 3D space
   (//bears// towards the landmark).

3. **Setup the OpenGV solver:** OpenGV has many defined "problems" with their
   correspondent solvers, Kimera uses some of these for its different possible
   camera setups. In particular, for mono-inertial SLAM, it uses the "Central
   Relative Pose" (CRP) problem type illustrated in [this
   image](https://laurentkneip.github.io/opengv/relative_central.png). In this
   problem, given two cameras (the keyframe and the current frame), a set of
   bearing vectors each (the red vectors), OpenGV can return the delta
   translation (cyan vector) and rotation (blue line) between the cameras. The
   model for this problem needs a different number of knowns to be able to
   compute a solution. The CRP problem is a good fit for the mono camera
   scenario, and it usually needs only "5 points" //(I think those would be 5
   bearing vectors)//. As we already have a rotation estimate (blue line in
   [image](https://laurentkneip.github.io/opengv/relative_central.png)) thanks
   to the `pim` we can give it to OpenGV and then it will only need "2 points"
   to complete the model. Unfortunately, we can't just pick two bearing vectors
   at random because feature detection and tracking is a task that usually has
   many incorrect keypoints detected, which are called //outliers//. As such
   many of our keypoints are outliers. RANSAC (RANdom SAmple Consensus) is a
   technique that addresses this issue, it lets you solve a model that requires
   //n// parameters when you have a sample of //N// possible candidates //(N >>
   n)// in which some might be outliers by solving the model many times with
   random samples of 2 bearing vectors (in Kimera about 100 times) and keeping
   the most fitting model. And so that's a rough idea of how OpenGV works,
   Kimera passes the bearing vectors and the `pim` rotation to the
   `TranslationOnlySacProblem` OpenGV class (or others depending on your
   camera-imu setup) and then just calls its `computeModel` method.

4. **Mark outlier keypoints:** Finally, after computing the model we have our
   final camera pose ready to use for the backend. As the model was solved using
   RANSAC it also marked some of the bearing vectors as outliers and as such
   Kimera marks all the landmarks corresponding to those bearing vectors as
   invalid so they will not be used in future frames.

It would be good to clarify that I didn't go deep into how the distortion models
nor how the OpenGV solvers work, so I might be having some misunderstandings.
Another thing to consider is that steps 1 and 2 were done in the
`featureTracking` method at the same time as feature creation.

---

While feature tracking is good for discovering new frames based on old features,
the first frame needs to do a full `featureDetection` from scratch.

Kimera implements a `FeatureDetector` class with the possibility to use multiple
OpenCV detectors (like FAST and ORB), but by default it uses the
`cv::GFTTDetector` (Good Features To Track) also called the Shi-Tomasi corner
detector, this in conjunction with the Lucas-Kanade tracker are sometimes called
the [Kanade–Lucas–Tomasi (KLT) feature
tracker](https://en.wikipedia.org/wiki/Kanade–Lucas–Tomasi_feature_tracker). The
details of the GFTT algorithm are out of scope.

After detecting possible features, many of them could be very close to each
other, for this Kimera runs a //non-max suppression//, which is basically an
overlapping detection of these features (considered as circles) where if there
is too much overlap, the features with the lesser scores (non-max) are
discarded. This overlapping detection could be done with something like KDTrees,
Kimera uses RangeTree by default (algorithms copied from another MIT licensed
project).

The final step that is enabled by default on feature detection is //subpixel
corner refinement// which is an iterative method (that seems quite expensive)
for making the detected keypoints coordinates have more precision than just
integers. For this it uses
[cv::cornerSubPix](https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga354e0d7c86d0d9da75de9b9701a9a87e).

Lastly, it is worth mentioning that feature detection does not only happen at
the start of Kimera but also on every //keyframe// (there are about five
keyframes per second by default and on every keyframe the `pim` is reset as
well). As non-first keyframes will already have some keypoints predicted thanks
to the `featureTracking`, those are masked when doing `featureDetection` so as
to not re-detect them. Features also have an age property and when they surpass
a maximum age (25 frames by default) they are invalidated. Feature detection has
a maximum number of features to look for (300 by default) and performance-wise
sometimes it happens that too few features are detected (about 20) and in those
cases the RANSAC algorithm instead of taking less than ten iterations as usual
it takes its maximum amount of iterations (100 by default).
