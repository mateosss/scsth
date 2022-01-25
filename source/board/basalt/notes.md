### Scractchpad

<!-- TODO: Review if all items and their keywords were addressed in the writeup -->

- [ ] concept: nonlinear regression, gauss-newton algorithm
- [ ] VIO:
  - [x] KLT Tracking: FAST, KLT, _inverse-compositional approach_, patch
        dissimilarity norm, _ZNCC_, LSSD, estimate T in _SE(2)_,
        _outlier filtering peculiarity_
        - inverse-compositional approach: https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0910/zhao.pdf
        - ZNCC: https://martin-thoma.com/zero-mean-normalized-cross-correlation/
  - [ ] VI BA: _IMU preintegration_, KLT tracking error, _T\_WI in \_SE(3)_,
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

- optical_flow.cpp:OpticalFlowFactory::getOpticalFlow

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

---------------------

```cpp
vio_estimator.cpp:VioEstimatorFactory::getVioEstimator();
new SqrtKeypointVioEstimator<float>(g, cam, config) : VioEstimatorBase, SqrtBundleAdjustmentBase: BundleAdjustmentBase {

public: // VioEstimatorBase
  atomic<int64_t> last_processed_t_ns;
  atomic<bool> finished;
  // Input
  tbb::queue<OpticalFlow::Output> *vision_data_queue;
  tbb::queue<ImuData<double>> *imu_data_queue;
  // Output
  tbb::queue<PoseVelBiasState<double>> *out_state_queue;
  tbb::queue<MargData> *out_marg_queue;
  tbb::queue<VioVisualizationData> *out_vis_queue;
private: // BundleAdjustmentBase (and SqrtBundleAdjustmentBase)
  map<TS, PoseStateWithLine> frame_poses;
  map<TS, PoseVelBiasStateWithLin> frame_states;
  LadmarkDatabase<float> lmdb;
  float obs_std_dev = vioconfig;
  float huber_thresh = vioconfig;
  Calibration calib;
private:
  bool take_kf = true;
  int frames_after_kf = 0;
  set<int64_t> kf_ids;

  TS last_state_t_ns;
  map<TS, IntegratedImuMeasurement> imu_meas;
  Vec3 g;

  //Input
  map<int64_t, OpticalFlow::Output> prev_opt_flow_res; // Frame window
  map<int64_t, int> num_points_kf;

  MargLinData<float>{
    bool is_sqrt = true;
    AbsOrderMap {
      map<TS, {int, int}> abs_order_map;
      size_t items = 0;
      size_t total_size = 0;
    } order;
    MatXX H = [10000 for position and yaw, 3.16 for ba, 10 for bg, else 0];
    MatX1 b = 0;
  } marg_data;
  MargLinData<float> nullspace_marg_data; // for debugging; marg version without prior(?)

  Vec3 gyro_bias_sqrt_weight = 1 / calib.gyro_bias_std;
  Vec3 accel_bias_sqrt_weight = 1 / calib.accel_bias_std;
  size_t max_states = vioconfig(3);
  size_t max_kfs = vioconfig(7);

  SE3 T_w_i_init;

  bool initialized = false;
  bool opt_started = false;

  VioConfig config;

  constexpr float vee_faactor = 2;
  constexpr float initial_vee = 2;
  float lambda=vioconfig, min_lambda=vioconfig, max_lambda=vioconfig, lambda_vee = 2;

  thread processing_thread;

  ExecutionStats stats_all_
  ExecutionStats stats_sums_;

  SqrtKeypointVioEstimator(Vec3 g, Calibration calib, VioConfig config) {
    // set defaults values for fields;
  }

  initialize(ba = bg={0,0,0}) {
    processing_thread.run(ba, bg);
  }

  thread processing_thread(ba, bg) {
    OpticalFlow::Output prev_frame;

    IntegratedImuMeasurement<float>::Ptr meas;

    const Vec3 accel_cov = calib.accel_noise_std ** 2; // Note: they are constant
    const Vec3 gyro_cov = calib.gyro_noise_std ** 2;

    ImuData data = imu_data_queue.pop().calibrated();

    while (true) {
      OpticalFlow::Output curr_frame = vision_data_queue.pop() or break;

      if (!initialized) { // Initialize
        while(data.t_ns < curr_frame.t_ns) data = imu_data_queue.pop().calibrated();
        Vec3 vel_w_i_init = ZERO;
        T_w_i_init.quaternion = FromTwoVectors(data.accel, +Z);
        T_w_i_init.position = ZERO;

        int64_t t = curr_frame.t_ns;
        imu_meas[t] = IntegratedImuMeasurement(t, bg, ba);
        frame_states[t] = PoseVelBiasStateWithLin(t, T_w_i_init, vel_w_i_init, bg, ba, true);
        marg_data.order.abs_order_map[t] = {0, POSE_VEL_BIAS_SIZE}
        marg_data.order.items = 1;
        marg_data.order.total_size = POSE_VEL_BIAS_SIZE;
        last_state_t_ns = t;

        initialized = true;
      }

      if (prev_frame) { // Preintegrate measurements

        // Start preintegration from prev_frame and its bias state
        PoseVelBiasStateWithLin last_state = frame_states.at(last_state_t_ns);
        meas = new IntegratedImuMeasurement(prev_frame.t_ns, last_state.getState().bias);

        // Discard old IMU samples
        while (data.t_ns <= prev_frame.t_ns>) data = imu_data_queue.pop();
        data = calibrated(data);

        // Interframe integration
        while (data.t_ns <= curr_frame.t_ns) {
          meas.integrate(*data, accel_cov, gyro_cov);
          data = imu_data_queue.pop().calibrated();
          if (!data) break;
        }

        // Create fake last measurement
        if (meas.get_start_t_ns() + meas.get_dt_ns() < curr_frame.t_.ns) {
          if (!data) break;
          fake_data = data; fake_data.t_ns=curr_frame.t_ns;
          meas->integrate(fake_data, accel_cov, gyro_cov); // XXX
        }
      }

      measure(curr_frame, meas); // XXX
      prev_frame = curr_frame;
    }

    finished = true;
  }

  measure(OpticalFlow::Output curr_frame, IntegratedImuMeasurement meas) {
    Timer t_total;

    // Predict new state from last_state and preintegrated meas
    PoseVelBiasState last_state = frame_states[last_state_t_ns].getState();
    PoseVelBiasState next_state = last_state; // Reuses bias from last_state
    meas->predictState(last_state, g, next_state);
    TS t = last_state_t_ns = next_state.t_ns = curr_frame.t_ns;
    frame_states[t] = PoseVelBiasStateWithLin(next_state); // XXX
    imu_meas[last_state.t_ns] = meas;

    // save results
    prev_opt_flow_res[t] = curr_frame;

    // Make new residual for existing keypoints

    // Update existing landmarks in landmark database with new observations for those kps
    int connected0 = 0;
    map<TS, int> num_points_connected; // Used in marg. Amount of observations a kf has connected to itself for already-existing landmarks
    set<int> unconnected_obs0; // Observations of kps that are not in the lmdb
    for (int i = 0; i < NUM_CAMS; i++) {
      TimeCamId camframe = {t, i}; // frame t of camera i
      for ([kpid, kppos] in curr_frame.observations[i]) {
        if (!lmdb.landmarkExists(kpid)) if (i == 0) unconnected_obs0.emplace(kpid);
        else {
          TimeCamId kp_hostkf = lmdb.getLandmark(kpid).host_kf_id; // kps are "hosted" in a keyframe

          Keypoint kobs = {kpid, kppos.translation()};
          lmdb.addObservation(camframe, kobs);

          num_points_connected[kp_hostkf.frame_id]++;
          if (i == 0) connected0++;
        }
      }
    }

    // Decide if and take a keyframe
    bool few_connected_lms = connected0 / (connected0 + unconnected_obs0) < vioconfig(0.7); // less than 70% connected
    bool nonkf_limit = frames_after_kf > vioconfig(5);
    take_kf = few_connected_lms and nonkf_limit;
    if (take_kf) { // keyframing: triangulate new landmarks from stereo pair. Register left cam kf
      take_kf = false;
      frames_after_kf = 0;
      kf_ids.emplace(t);

      TimeCamId tcidl = {t, 0}; // Left camera current frame
      int num_points_added = 0;
      for (int lm_id : unconnected_obs0) {
        // Observations of lm_id in prev_opt_flow_res
        map<TimeCamId, Keypoint> kp_obs;
        for (stereoframe in prev_opt_flow_res)
          for (frame in stereoframe)
            if (frame.observations.has(lm_id) as {kpipd, kppos})
              kp_obs[{frame.ts, frame.cam}]: {lm_id, kppos}

        // Triangulate
        for ({fts, fcam, kppos} : kp_obs) {
          TimeCamId tcido = {fts, fcam}; // Keypoint observation camera-frame
          Vec2 p0 = curr_frame.observations[0][lm_id].translation();
          Vec2 p1 = prev_opt_flow_res[fts].observations[fcam][lm_id].translation();

          Vec4 p0_3d = calib.intrinsics[0].unproject(p0);
          Vec4 p1_3d = calib.intrinsics[fcam].unproject(p1);
          if (any unprojection fails) continue;

          SE3 T_i0_i1 = frame_poses[t].inverse() * frame_poses[fts]; // Transform current imu0 to observer imu1
          SE3 T_0_1 = calib.T_i_c[0].inverse() * T_i0_i1 * calib.T_i_c[fcam]; // From left cam to imu0, from imu0 to imu1, from imu1 to observer cam. i.e., From left cam to observer cam.
          // T_0_1: Moves a point in left cam-frame to a point in observer cam-frame
          // Or equivalently, changes coordinates of p1 to be in left cam-frame (should be p0)

          if (T_0_1.translation().norm < vioconfig(0.05)) continue;

          Vec4 p0_triangulated = triangulate(p0_3d, p1_3d, T_0_1); // TODO: JacobiSVD. I'm pretty sure this is DLT. TODO: learn and explain it. See pag91, algorithm4.1 of Multiple view geometry... book. Appendix 4 of that book is GOLD. in there there is an explanation of SVD in page 585

          if (p0_triangulated is good) { // Register landmark
            Landmark kpt_pos = {
              host_kf_id = tcidl,
              direction=StereographicParam::project(p0_triangulated),
              inv_dist=p0_triangulated[3]
            }; // TODO: See more on Stereographic project
            lmdb.addLandmark(lm_id, kpt_pos);
            num_points_added++;
            for (every obs in kp_obs) lmdb.addObservation(obs);
            break;
          }
        }
      }
      num_points_kf[t] = num_points_added;
    } else {
      frames_after_kf++;
    }

    // ONLY-ON-SQRT: Get landmarks from lmdb that are not in curr_frame
    set<KeypointId> lost_landmarks;
    if (vioconfig(vio_marg_lost_landmarks, true)) {
      lost_landmarks = {kpids in lmdb that do not appear in curr_frame left nor right}
    }

    optimize_and_marg(num_points_connected, lost_landmarks); // TODO

    out_state_queue.push(frame_states[t]);
    out_vis_queue.push(built_data_for_visualizer_from_frame_states_t);
  }
};

```

```C++
class IntegratedImuMeasurement {
  static void propagateState(PoseVelState curr_state, ImuData data, PoseVelState &out_next_state, &jacobians = nullptr);
  void integrate(ImuData data, Vec3 accel_gyro_cov) {propagateState(delta_state_, data_corrected, delta_state_)};
  void predictState(PoseVelState state0, Vec3 g, PoseVelState& out_state1);
  Vec9 residual(state0, g, state1, curr_bg_ba, /, out_jacobians=nullptr);
};

class PoseVelStateWithLin {};

class Landmark {
  Vec2 direction; // bearing vector towards point
  float inv_dist; // invers distance towards there. 0 means infinitely far I think.

  TimeCamId host_kf_id; // What is the keyframe hosting this kp
  map<TimeCamId, Vec2> obs; // In which frames this kp has been observed, and what coordinates
};

class Keypoint {
  int kpt_id;
  Vec2 pos;
};
```

```cpp
optimize() {
  if (frame_states.size() <= 4) return; // initial frame_states are computed with pims

  AbsOrderMap aom;
  for ({t, pose} in frame_poses) { // frame_poses (s_k) is empty before marginalize. Is for keyframes.
    aom.abs_ordder_map[t] = {aom.total_size, POSE_SIZE};
    aom.total_size += POSE_SIZE;
    aom.items++;
  }
  for ({t, state} in frame_states) { // frame_states (s_f) is for all frames
    aom.abs_order_map[t] = {aom.total_size, POSE_VEL_BIAS_SIZE};
    aom.total_size += POSE_VEL_BIAS_SIZE;
    aom.items++;
  }

  for (int iter; iter < vioconfig(7); iter++) {
    double rld_error;
    vector<RelLinData> rld_vec;
    linearizeHelper(rld_vec, lmdb.getObservations(), rld_error);

    LinearizeAbsReduce<DenseAccumulator> lopt(aom);
    tbb::parallel_reduce(rld_vec, lopt);

    double marg_prior_error = 0;
    double imu_error = 0;
    double bg_error = 0;
    double ba_error = 0;
    linearizeAbsIMU(aom, lopt.accom.getH(), lopt.accum.getB(), imu_error, bg_error, ba_error, frame_states, imu_meas, gyro_bias_weight, accel_bias_weight, g);
    linearizeMargPrior(marg_order, marg_H, marg_b, aom, lopt.accum.getH(), lopt.accum.getB(), marg_prior_error);

    double error_total = rld_error + imu_error + marg_prioer_error + ba_error + bg_error;

    lopt.accum.setup_solver();
    VectorX Hdiag = lopt.accum.Hdiagonal();

    bool converged = false;

    // Gauss-Newton iteration
    // By default it uses gauss newton, although Levenverg-Marquardt is implemented
    VectorX Hdiag_lambda = Hdiag * vioconfig(100);
    Hdiag_lambda = max(Hdiag_lambda, vioconfig(100));
    VectorX inc = lopt.accum.solve(&Hdiag_lambda);
    double max_inc = inc.abs().maxCoeff();
    if (max_inc < 1e-4) converged = true;

    // Apply increment to poses
    for ({t, pose} in frame_poses) {
      int idx = aom.abs_order_map[t].total_size;
      pose.applyInc(-inc.segment<POSE_SIZE>(idx));
    }

    // Apply increment to states
    for ({t, state} in frame_states) {
      int idx = aom.abs_order_map[t].total_size;
      state.applyInc(-inc.segment<POSE_VEL_BIAS_SIZE>(idx));
    }

    // Update points
    for@parallel (rld in rld_vec) updatePoints(aom, rld, inc); // TODO
  }
}

void linearizeHelper(vector<RelLinData>& rld_vec, const obs, double& error) {

  vector<FrameId> obs_kfs = obs.keys();
  rld_vec = {RelLinData(num_kps=lmdb.landmarks.size(), num_rel_poses=obs[h].size()) for h : obs_kfs};

  for@parallel (i in range(obs_kfs)) {
    FrameId h = obs_kfs[i];
    RelLinData rld = rld_vec[i];
    for ({t, kps} in obs[h]) {
      if (h != t) {
        rld.append({h, t});
        PoseStateWithLine state_h = getPoseStateWithLin(h); // Prioritize keyframe poses, then regular states
        PoseStateWithLine state_t = getPoseStateWithLin(t);
        Mat66 d_rel_d_h, d_rel_d_t;
        SE3 T_t_h = computeRelPose(state_h.getPoseLin(), state_t.getPoseLin(), T_i_c[h], T_i_c[t], &d_rel_d_h, &d_rel_d_t);
        rld.d_rel_d_h.append(d_rel_d_h);
        rld.d_rel_d_t.append(d_rel_d_t);
        if (state_h.isLinearized() or state_t.isLinearized()) {
          T_t_h = computeRelPose(state_h.getPoseNonLin(), state_t.getPoseNonLin(), T_i_c[h], T_i_c[t]);
        }

        Mat44 T_t_h = T_t_h.matrix();
        FrameRelLinData frld;

        Camera cam = cameraOf(t);
        for (kp in kps) {
          // ...
          // Same as the procedure done in the else below but with the following linearize call:
          linearizePoint(kp, lm, T_t_h, cam, &res, &d_res_d_xi, &d_res_d_p);
          // ...
          // And updates frld like this
          frld.Hpp += obs_weight * d_res_d_xi.transpose() * d_res_d_xi;
          frld.bp += obs_weight * d_res_d_xi.transpose() * res;

          frld.Hpl.append(obs_weight * d_res_d_xi.transpose() * d_res_d_p);
          frld.lm_id.append(lm);

          rld.lm_to_obs[lm].append(rld.Hpppl.size(), frld.lm_id.size() - 1);
        }
        rld.Hpppl.append(frld);
      } else {
        Camera cam = cameraOf(t);
        for (kp in kps) {
          Landmark lm = lmdb.getLandmark(kp);

          Vec2 res;
          Matrix23 d_res_d_p;
          linearizePointSameFrame(kp, lm, cam, &res, &d_res_d_p);

          // So this is the weight matrix?
          double e = res.norm();
          double huber_weight = min(vioconfig(1.0), vioconfig(1.0) / e);
          double obs_weight = huber_weight / vioconfig(0.5)**2;
          rld.error += (2 - huber_weight) * obs_weight * res.transpose() * res;

          rld.Hll[kp] += obs_weight * d_res_d_p.transpose() * d_res_d_p;
          rld.bl[kp] += obs_weight * d_res_d_p.transpose() * res;
        }
      }
    }
  }

  for (RelLinData rld : rld_vec) &error += rld.error;

}

bool linearizePoint(Keypoint kp, Landmark lm, Mat44 T_t_h, Camera cam, Vec2 &res, Mat26 &d_res_d_xi, Mat23 &d_res_d_p) {
  Vec4 p3_h = StereographicParam::unproject(lm.dir);
  p3_h[3] = lm.inv_distance;
  Vec4 p3_t = T_t_h * p3_h;
  Vec2 p2 = cam.project(p3_t);
  if (any failed) return false;

  *res = p2 - kp.pos;
  *d_res_d_xi = computeJacobian();
  *d_res_d_p = computeJacobian();
  return true;
}

bool linearizePointSameFrame(Keypoint kp, Landmark lm, Camera cam, Vec2 &res, Mat23 &d_res_d_p) {
  Vec3 p3 = StereographicParam::unproject(lm.dir);
  Vec2 p2 = cam.project(p3);
  if (any failed) return false;

  *res = p2 - kp.pos;
  *d_res_d_p = computeJacobian();
  return true;
}

struct AbsOrderMap {
  map<Timestamps, pair<TOTAL_SIZE: int, SIZE: int>> abs_order_map;
  items = 0;
  total_size = 0;
}

struct RelLinData : RelLinDataBase {
  // RelLinDataBase:
  vector<FrameId, FrameId> order;
  vector<Matrix66> d_rel_d_h;
  vector<Matrix66> d_rel_d_t;

  // RelLinData
  map<int, Matrix33> Hll;
  map<int, Vector> bl;
  map<int, vector<LandmarkId, LandmarkId>> lm_to_obs;
  vector<FrameRelLinData> Hpppl;
  double error;
}

struct FrameRelLinData {
  Matrix66 Hpp;
  Vector6 bp;
  vector<LandmarkId> lm_id;
  vector<Matrix63> Hpl;
}
```
