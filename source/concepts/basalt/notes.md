### Scractchpad

- [ ] concept: nonlinear regression, gauss-newton algorithm
- [ ] VIO:
  - [ ] KLT Tracking: FAST, KLT, _inverse-compositional approach_, patch
        dissimilarity norm, _ZNCC_, LSSD, estimate T in _SE(2)_, _outiler filtering
        peculiarity_
  - [ ] VI BA: _IMU preintegration_, KLT tracking error, T*WI in \_SE(3)*,
        static projection function from calibration, landmarks in keyframes
    - [ ] Repr. of Unit Vectors in 3D: bearing vector, efficiency, graph
    - [ ] Reprojection Error: residual, _numerical stability_
    - [ ] IMU Error: pseudemeasurement [8], bias-correction, updates to initial
          state, f(s, a, w), _g(ba, bg)_, _jacobian update_, _linearization point_,
          _residuals_, _gravity in residuals_, _covariance matrix for weight of
          residuals_, _[8]_
  - [ ] Optimization and Partial Marginalization: _Nonlinear energy function_,
        _E_m_, what happens when a new frame/keyframe is added, _Markov blanket_,
        _vector space of xi_, _schur complement_, _energy term_, _first estimate
        jacobians_, _nullspace properties of the linearlized marginalization prior_,
        _fixed linearization point_.
- [ ] VI Mapping: _implicit loop closure with keypoint matching_, two layer
      VIO/BA, non-linear factors
  - [ ] Global Map Optimization: ORB, reprojection error, E*nfr, state s,
        keyframe marginalization, \_Markov blanket*, _approximate distribution_
  - [ ] Non-Linear Factor Recovry: distrubition approximation of markov blanket,
        sparser topology, _residual linearization_, _gaussian distribution_,
        _minimize KLD_, _H and formulas_
  - [ ] Non-Linear Factors for Distribution Approximation: dense factor,
        pairwaise pose factors, roll-pitch factor, absolute position factor, yaw
        factor, _information matrices_, drop yaw and absolute position factors, _new
        E^G_nfr_,
- [ ] Evaluation: ATE RMS, EuRoC
  - [ ] System Paramters: KLT, 50pixels, each cell one feature, window size 7,
        tempostate 3, new keyframe selection
  - [ ] Accuracy: Table 1, VIO vs MAPPING, VI DSO vs ORB-SLAM-VI. ORB-SLAM3
        similar excfor pim
  - [ ] Factor Weighting: _using vs not using weights_
  - [ ] Timing: 2.5 smaller state, highly parallel, 4x faster
- [ ] Conclusions

[1]: Visual Inertial ORB-SLAM: https://arxiv.org/pdf/1610.05949.pdf

# Basalt#2: The Double Sphere Camera Model

- [ ] Related work: central projection, project, unproject, omega, theta,
      calibration pattern, bearing vector, intrinsics
- [ ] Camera models: pinhole, kb, eucm, and specially DS (also ucm and fov):
  - [ ] for each: intuition, intrinsics, project, unproject, omega, theta
- [ ] Calibration: how to, local subpixel refinement, robust Huber norm, least
      squares gauss newton, weighting matrix, initialization of method [5], UPnP
      algorithm [8]
- [ ] Evaluation: reprojection error, computation time, qualitative results,
      different UCM (I doubt)

# Basalt#3: The TUM VI Benchmark for Evaluating Visual-Inertial Odometry

- General
  - small number of high-quality datasets (probably because MoCap is expensive)
  - photometric calibration
  - 16 bit color depth
  - exposure times: center of exposure is timestamp, external light sensor,
    automatic exposure algorithms, least squares fit
  - linear response function
  - vignette calibration
  - IMU calibration (axis scaling and misalignment)
  - IMU temperature for temperature-dependant noise models
  - Camera-IMU time-synchronization in hardware: time offset of 5.3ms due to
    readout delay of IMU measurements.
  - Time offsets and spatial offsets (extrinsics)
  - MoCap: expensive, one room setup
- Calibration
  - Camera: slow movements in front of calibration grid for motion blur,
  - IMU and hand-eye: extrinsics between Camera-IMU and MoCap-IMU, concurrent
    optimization of: 7 bullet points. _hand-eye calibration_. Mg and Ma
    matrices, 6 entries in Ma, ba-bg not necessary. reasonable approximate
    precalibration of ba-bg.
  - IMU noise parameters: IMU model, allan deviation.
  - Photometric Calibration: for good intensity matching for direct methods,
    vignette calibration, image formation model, how the dataset looks.
- Dataset: type of sequences, calibrated vs raw formats, usage of 512x512 images
  instead of full res
- Evaluation metrics: RMS ATE and RMS RTE

# Basalt#4 and #5 spline calibration and square root marginalization, were way over my head.

# Code

- usage of tbb: parallel_for, queues, concurrent_unordered_map
- vio.cpp

  ```c++
  config.load();
  calib.load();
  OpticalFlowBase opt_flow = OpticalFlowFactory::getOpticalFlow(config, calib);
  VioEstimatorBase vio = VioEstimatorFactory::getVioEstimator(config, calib, g, use_imu, use_double);
  vio.initialize(ba=0, bg=0);

  opt_flow.output_queue = &vio->vision_data_queue;
  if (show_gui) vio->out_vis_queue = &pangolin_vis;
  vio->out_state_queue = &out_state_queue;
  if (save_marg) vio->out_marg_queue = &marg_data_saver;

  thread t1(image_feeder)
  thread t2(imu_feeder)
  thread t3(vis_consumer)
  thread t4(state_consumer)
  thread t5(queue_printer)
  while(true) draw();


  vio->initialize();

  ```

- optical_flow.cpp

  ```c++
  // PatchOpticalFlow vs FrameToFrameOpticalFlow vs MultiscaleFrameToFrameOpticalFlow
  new FrameToFrameOpticalFlow<float, Pattern51>(config, calib) {
    // From OpticalFlowBase:
    tbb::queue<Input = {t_ns, [img_data]}> input_queue;
    // Compact because saved as 2x3 instead of 3x3
    tbb::queue<Output = {
      t_ns, observations[2]: {KeypointId, AffineCompact2D}, pyramid_levels: [{KeypointId, size_t}], input_images: Input
    }> output_queue;
    MatrixXf patch_coord; // Patch coordinates

  private:
    t_ns;
    frame_counter;
    last_keypoint_id;
    vio_config;
    vio_calib;
    Output transforms;
    ManagedImagePyr[2] pyramid;
    ManagedImagePyr[2] old_pyramid;
    Matrix44 essential; // transform from camera 0 to camera 1
    thread processing_thread; // runs processingLoop;

  public:
    processingLoop() { while(true) processFrame(input_queue.pop()); }
    processFrame() {
      if (firstFrame) {
        // initialization of fields and
        pyramid.generateMipMaps(frame); // TODO: Here is another entire frame copy!!!
        addPoints();
        filterPoints();
      } else {
        old_pyramid = pyramid;
        pyramid.generateMipMaps(frame);
        for(i : cameras) trackPoints(old_pyramid[i], pyramid[i], transform.observations[i], new_transform.observations[i])
        transform = new_transform;
        addPoints();
        filterPoints();
      }
      output_queue.push(transform);
    }
    addPoints() {
      class KeypointsData {
        corners: [vec2]; angles: [double]; descriptors: [bitset<256>];
        p3d: [vec4]; hashes: [FeatureHash = bitset<256>]; bow_vector: [{FeatureHash, double}];
      };
      Keypointsdata kd;
      detectKeypoints(kd, pyramid[0].lvl(0)) { // only for camera 0, multiscale_* variant seem to detectKeypoints in other pyramid levels as well
        // heuristic detail: they only add up to num_cell_points, but when a cell already has at least one kp, they dont bother to reach num_cell_points again
        // call cv::FAST for each cell
        // limit to best num_cell_points=1 point per cell
        // fill only kd.corner with that keypoint, but clear angles and descriptors
        // cornerSubPix refinement code commented out (cf. Kimera)
      };

      if (stereo) {
        trackPoints(img0, img1, kd.corners, out_corners); // Track kp of right image
      }
    }
    filterPoints() {
      if (!stereo) return;

      KeypointId[] kpid = [ids of keypoints that appear in both camera observations];
      Vec2[] proj0 = [positions of kpid in cam0];
      Vec2[] proj1 = [positions of kpid in cam1];
      Vec4[] p3d0 = cam0.unproject(proj0); // TODO: Why vec4?
      Vec4[] p3d1 = cam1.unproject(proj1);
      for (p0, p1 in [p3d0, p3d1]) {
        if (p0 or p1 unsuccessful projection) lm_to_remove.append(kpid[i]);
        if (epipolar_error(p0, p1) > 0.005) lm_to_remove.append(kpid[i]);
      }
      for (id: lm_to_remove) transforms.observations[1].erase(id); // Only from cam1
    }
    trackPoints(pyr1, pyr2, kps1, &kps2) {
      tbb:map<KeypointId, Affine2d> result;
      for<tbb>(id1, aff1: kps1) {
        Affine aff2 = aff1;
        bool valid = trackPoint(pyr1, pyr2, aff1, &aff2);
        if (!valid) continue;
        aff1_recovered = aff2
        bool valid = trackPoint(pyr2, pyr1, aff2, &aff1_recovered)
        if (!valid) continue;
        float dist2 = (aff1 - aff1_recovered).squaredNorm();
        if(dist2 < optical_flow_max_recovered_dist2) kps2[id] = aff2;
      }
    }
    trackPoint(pyr1, pyr2, aff1, out_aff2) {
      out_aff2.A().setIdentity();
      for(level = 3 - 1; level >= && patch_valid; level--) {
        float scale = 2 ** level;
        out_aff2.b() /= scale;
        // TODO: Heavy stuff, computes interpolated intensity and x-y gradients for each point in pattern51
        // then compute jacobian (with a weird operation to grad.row(i) and an offset to pattern coordinates)
        // then computes (H_inv * J)^T whatever that is, with H being something like the hessian? H = J^2
        // uses ldlt (cholesky) and solveInPlace() (which solver?) for calculating H_inv
        PatchT p(pyr1.lvl(level), aff1.b() / scale);
        patch_valid &= p.valid; // valid means, mean intensity is not zero, intensity (data) and (H_inv*J)T matrices are valid
        if (patch_valid) {
          patch_valid &= trackPointAtLevel(pyr2.lvl(level), p, &out_aff2);
        }
        out_aff.b() *= scale;
      }
      out_aff2.A() = aff1.A() * out_aff2.A();
    }
    trackPointAtLevel(img2, p, out_aff2) {
      for (iteration = 0; patch_valid && iteration < 5; iteration++) { // gauss newton
        VectorP res;
        Matrix2P transformed_pat = out_aff2 * p::pattern2;
        patch_valid &= p.residual(img2, transformed_pat, &res); // compares with the norm in the paper the mean intensity of current p compared to
        if (patch_valid) {
          Vector3 inc = -p.H_se2_inv_J_se2_T * res;
          patch_valid &= inc.allNonNaN();
          patch_valid &= inc.lpNorm<infinity>() < 1e6; // avoid very large increments for some reason, infinity norm is just the max component
          if (patch_valid) {
            out_aff2 = out_aff2 * SE2::exp(inc);
            patch_valid &= img2.inboundswithpadding2(out_aff2);
          }
        }
      }
    }
  }
  ```

- epipolar geometry definitiuons: https://en.wikipedia.org/wiki/Epipolar_geometry
  - essential and fundamental matrices
- image rectification is not more than aligning epipolar lines
- a lot of cpu image manipulation that could be done in GPU
- pyramidal tracking LK seems to be the same as opencv calcOpticalFlowPyrLK
  - https://docs.opencv.org/4.x/dc/d6b/group__video__track.html#ga473e4b886d0bcc6b65831eb88ed93323
  - citation:
    https://www.semanticscholar.org/paper/Pyramidal-implementation-of-the-lucas-kanade-Bouguet/aa972b40c0f8e20b07e02d1fd320bc7ebadfdfc7?p2df
  - weird, see improvementts and variation section here: https://en.wikipedia.org/wiki/Kanade%E2%80%93Lucas%E2%80%93Tomasi_feature_tracker
    it seems to recommend checking against non-previous frame, but basalt checks
    against previous, weird.
- LK tracker could be nice to explain as it is also used in Kimera.
  http://www.inf.fu-berlin.de/inst/ag-ki/rojas_home/documents/tutorials/Lucas-Kanade2.pdf
- Sophus: SE, SO, exp, expmat, hat, vee
- Explicar el cv::FAST corner detector
