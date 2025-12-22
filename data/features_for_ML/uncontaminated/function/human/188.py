def get_cfgs():
    env_cfg = {
        "num_actions": 8, #总关节数量
        "urdf":"assets/urdf/CJ-003/urdf/CJ-003-wheelfoot.urdf",
        "mjcf":"assets/mjcf/CJ-003/CJ-003-wheelfoot.xml",
        # joint names
        "default_joint_angles": {  # [rad]
            "left_hip_joint":0.0,
            "left_thigh_joint": 0.0,
            "left_calf_joint": 0.0,
            "right_hip_joint":0.0,
            "right_thigh_joint": 0.0,
            "right_calf_joint": 0.0,
            "left_wheel_joint": 0.0,
            "right_wheel_joint": 0.0,
        },
        "joint_init_angles": {  # [rad]
            "left_hip_joint":0.0,
            "left_thigh_joint": 0.0,
            "left_calf_joint": 0.0,
            "right_hip_joint":0.0,
            "right_thigh_joint": 0.0,
            "right_calf_joint": 0.0,
            "left_wheel_joint": 0.0,
            "right_wheel_joint": 0.0,
        },
        "joint_names": [
            "left_hip_joint",
            "left_thigh_joint",
            "left_calf_joint",
            "right_hip_joint",
            "right_thigh_joint",
            "right_calf_joint",
            "left_wheel_joint",
            "right_wheel_joint",
        ],
        "joint_type": {  # joint/wheel
            "left_hip_joint": "joint",
            "left_thigh_joint": "joint",
            "left_calf_joint": "joint",
            "right_hip_joint": "joint",
            "right_thigh_joint": "joint",
            "right_calf_joint": "joint",
            "left_wheel_joint": "wheel",
            "right_wheel_joint": "wheel",
        },
        # lower upper
        "dof_limit": {
            "left_hip_joint":[-0.5, 1.0], # [-0.31416, 1.0]
            "left_thigh_joint": [0.0, 1.57],
            "left_calf_joint": [-2.0, 0.0],   
            "right_hip_joint":[-1.0, 0.5],
            "right_thigh_joint": [0.0, 1.57],
            "right_calf_joint": [-2.0, 0.0],
            "left_wheel_joint": [0.0, 0.0],
            "right_wheel_joint": [0.0, 0.0],
        },
        "safe_force": {
            "left_hip_joint": 25.0,
            "left_thigh_joint": 25.0,
            "left_calf_joint": 25.0,
            "right_hip_joint": 25.0,
            "right_thigh_joint": 25.0,
            "right_calf_joint": 25.0,
            "left_wheel_joint": 6.0,
            "right_wheel_joint": 6.0,
        },
        # PD
        "joint_kp": 30.0,
        "joint_kv": 0.8,
        "wheel_kv": 1.0,
        "damping": 0.01,
        # "stiffness":0.0, #不包含轮
        "armature":0.002,
        # termination 角度制    obs的angv弧度制
        "termination_if_roll_greater_than": 25,  # degree
        "termination_if_pitch_greater_than": 25, #15度以内都摆烂，会导致episode太短难以学习
        "termination_if_base_connect_plane_than": True, #触地重置
        "connect_plane_links":[ #触地重置link
            "base_link",
            "left_calf_Link",
            "left_thigh_Link",
            "right_calf_Link",
            "right_thigh_Link",
                ],
        "foot_link":[   #足端信息
            "left_wheel_Link",
            "right_wheel_Link",
        ],
        # base pose
        "base_init_pos":{
            "urdf":[0.0, 0.0, 0.7],#稍微高一点点
            "mjcf":[0.0, 0.0, 0.7],
            },
        "base_init_quat": [1.0, 0.0, 0.0, 0.0],#0.996195, 0, 0.0871557, 0
        "episode_length_s": 20.0,
        "resampling_time_s": 4.0,
        "joint_action_scale": 0.5,
        "wheel_action_scale": 10.0,
        "simulate_action_latency": True,
        "clip_actions": 100.0,
        "convexify":True,   #是否启动凸优化网格
        "decimate_aggressiveness": 4,    #优化等级0-8 0：无损 2：原始几何体 5：有明显变化 8： 大变特变
    }
    obs_cfg = {
        # num_obs = num_slice_obs + history_length * num_slice_obs + num_commands
        "num_obs": 286, #在rsl-rl中使用的变量为num_obs表示state数量
        "num_slice_obs": 28,
        "history_length": 9,
        "obs_scales": {
            "lin_vel": 2.0,
            "ang_vel": 0.25,
            "dof_pos": 1.0,
            "dof_vel": 0.05,
            # "dof_pos_cmd": 5.0,
        },
        "noise":{
            "use": True,
            #[高斯,随机游走]
            "ang_vel": [0.01,0.01],
            "dof_pos": [0.01,0.01],
            "dof_vel": [0.01,0.01],
            "gravity": [0.01,0.01],
        }
    }
    # 名字和奖励函数名一一对应
    reward_cfg = {
        "only_positive_rewards": True,
        "tracking_linx_sigma": 0.2, 
        "tracking_liny_sigma": 0.6, 
        "tracking_ang_sigma": 0.8, 
        # "tracking_height_sigma": 0.005,  
        "tracking_similar_legged_sigma": 0.05,  
        "tracking_gravity_sigma": 0.1,
        "feet_distance":[0.3, 0.6], #脚间距范围 m
        "reward_scales": {
            "tracking_lin_x_vel": 1.0,#1.5
            "tracking_lin_y_vel": 0.0,
            "tracking_ang_vel": 1.0, #1.5
            "tracking_leg_length": -6.0,   #身高/膝关节/髋关节(thigh)/足端到base  高速情况下会产生对抗
            "lin_vel_z": -0.02, #大了影响高度变换速度 -0.001
            "joint_action_rate": -0.01,
            "wheel_action_rate": -0.01,#-0.01
            # "similar_to_default": 0.0,
            "projected_gravity": -12.0,  #-12
            "similar_legged": 0.0,  #不带hip
            # "joint_vel": -0.001,
            "dof_acc": -1e-7,
            "dof_force": -1e-6,
            "ang_vel_xy": -0.02,
            "collision": -0.0015,  #base接触地面碰撞力越大越惩罚，数值太大会摆烂
            # "terrain":0.1,
            "feet_distance": -100.0,
            "survive": 2.0,
            "tsk": -3.0, #高速对抗
        },
    }
    command_cfg = {
        "num_commands": 6,
        "lin_vel_x_range": [-1.0, 1.0], #修改范围要调整奖励权重
        "lin_vel_y_range": [-0.0, 0.0], 
        "ang_vel_range": [-6.0, 6.0],   #修改范围要调整奖励权重
        "leg_length_range": [0.0, 1.0],   #两条腿
        "tsk_range": [-0.3, 0.3],   #左右
        "high_speed": False,    #跟踪高速要开启这个 防止两个速度在高速情况下对抗 高速情况下存活率会变低是正常现象
        "inverse_linx_angv": 1.0,    #前进速度和角速度反比 linx <= inverse_linx_angv / angv
        "inverse_tsk": 3.0,    #std = inverse_tsk / angv 这个数值可以用std=1时估计inverse_tsk
        "inverse_leg_length": 3.0,   #std = inverse_leg_length / angv
    }
    # 课程学习，奖励循序渐进 待优化
    curriculum_cfg = {
        "curriculum_lin_vel_step":0.005,   #比例
        "curriculum_ang_vel_step":0.0005,   #比例
        "curriculum_lin_vel_min_range":0.3,   #比例
        "curriculum_ang_vel_min_range":0.03,   #比例
        "lin_vel_err_range":[0.35,0.5],  #课程误差阈值
        "ang_vel_err_range":[0.5,1.0],  #课程误差阈值
        "damping_descent":False,
        "dof_damping_descent":[0.2, 0.005, 0.001, 0.4],#[damping_max,damping_min,damping_step（比例）,damping_threshold（存活步数比例）]
    }
    #域随机化 friction_ratio是范围波动 mass和com是偏移波动 等到模型存活达到70%再开启域随机化
    domain_rand_cfg = { 
        "friction_ratio_range":[0.2 , 1.6],
        "random_base_mass_shift_range":[-1.5 , 1.5], #质量偏移量
        "random_other_mass_shift_range":[-0.1, 0.1],  #质量偏移量
        "random_base_com_shift":0.05, #位置偏移量 xyz
        "random_other_com_shift":0.01, #位置偏移量 xyz
        "random_KP":[0.8, 1.2], #比例
        "random_KV":[0.8, 1.2], #比例
        "random_default_joint_angles":[-0.03,0.03], #rad
        "damping_range":[0.8, 1.2], #比例
        "dof_stiffness_range":[0.0 , 0.0], #范围 不包含轮 [0.0 , 0.0]就是关闭，关闭的时候把初始值也调0
        "dof_armature_range":[0.0 , 0.008], #范围 额外惯性 类似电机减速器惯性 有助于仿真稳定性
    }
    #地形配置
    terrain_cfg = {
        "terrain":True, #是否开启地形
        "train":"agent_train_gym",
        "eval":"agent_eval_gym",    # agent_eval_gym/circular
        "respawn_points":[
            [-5.0, -5.0, 0.0],    #plane地形坐标，一定要有，为了远离其他地形
            [5.0, 5.0, 0.0],
            [15.0, 5.0, 0.08],
        ],
        "horizontal_scale":0.1,
        "vertical_scale":0.001,
        "vertical_stairs":False,
        "v_stairs_height":0.1,  # 阶梯高度
        "v_stairs_width":0.25,  # 阶梯宽度
        "v_plane_size":0.8,  # 平台尺寸
        "v_stairs_num":10       # 阶梯数量
    }
    return env_cfg, obs_cfg, reward_cfg, command_cfg, curriculum_cfg, domain_rand_cfg, terrain_cfg