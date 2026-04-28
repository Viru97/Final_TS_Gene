# 🤖 TS Gene: Time-series Data Generation Tool for Risk Assessment of Robotic Applications

[![ROS Version](https://img.shields.io/badge/ROS_2-Jazzy-green.svg)]()
[![OS](https://img.shields.io/badge/OS-Ubuntu%2024.04-orange.svg)]()
[![Simulation](https://img.shields.io/badge/Simulation-Gazebo_Harmonic-blue.svg)]()
[![Paper](https://img.shields.io/badge/Paper-ESREL--SRA--E2025-purple)](https://rpsonline.com.sg/proceedings/esrel-sra-e2025/pdf/ESREL-SRA-E2025-P6239.pdf)

> **Publication:** This work has been accepted for publication in the Proceedings of the 35th European Safety and Reliability & the 33rd Society for Risk Analysis Europe Conference (ESREL SRA-E 2025).  
> **Authors:** Yuliang Ma*, Apurv Patel, Don Kurian, Julien Siebert, Silvia Vock, and Andrey Morozov  
> **Contact:** [yuliang.ma@ias.uni-stuttgart.de](mailto:yuliang.ma@ias.uni-stuttgart.de)

---

## 📖 Abstract

Robotic systems increasingly rely on artificial intelligence (AI) to enhance their capabilities in performing complex tasks across various domains. The development and evaluation of AI systems usually require high-quality datasets. In addition to normal datasets, faulty datasets are critical for enabling anomaly detection and failure prevention, which are essential for ensuring the safety and reliability of safety-critical robotic applications. However, faults are rare in real-world environments. 

Although fault injection techniques allow for the manual injection of configurable faults, deploying such methods directly in real-world settings is rather risky. As such, it is important to develop a data generation tool which is low-cost, safe, and efficient. 

To address this, we developed a time-series data generation tool for the risk assessment of robotic applications utilizing the **Robot Operating System (ROS)** as middleware. This ROS-based simulation tool integrates three key modules:
1. **Gazebo-based Scene Generator:** Configures different working scenarios (e.g., drilling and welding) by dynamically adjusting end-effectors, workpieces, and hand positions.
2. **Online Fault Injector:** Introduces systematic faults into robotic systems with configurable parameters.
3. **Risk Monitor:** Records faulty data and safety violations in real-time by measuring the spatial distance between human hands and robot end-effectors.

This tool facilitates the generation of time-series fault data and helps identify risks in Human-Robot Collaboration (HRC) scenarios. Additionally, it enables fast and safe deployment for other robot-related research areas, such as deep learning-based anomaly detection, failure prediction, and risk assessment.

---

## 🚀 Quick Start & Execution Guide

*(Note: The commands below have been updated to reflect the ROS 2 Jazzy and Gazebo Harmonic architecture).*

### Step 1: Initialize the Work Scene
Start by launching the core Gazebo simulation environment. Choose either the drilling or welding scenario:

**For Drilling:**
```bash
ros2 launch panda_gazebo start_workscene.launch.py
```

**For Welding:**
```bash
ros2 launch panda_gazebo start_workscene_welding.launch.py
```

### Step 2: Configure Environment Geometry

> ⚠️ **IMPORTANT:** The geometry modification script must be run before any randomizations.

```bash
ros2 run panda_gazebo modify_geometry.py
```

### Step 3: Randomize the Scene

Use the following nodes to generate highly diverse datasets by randomizing the positions of objects and human workers in the environment:

```bash
ros2 run panda_gazebo randomize_workpiece_position.py
ros2 run panda_gazebo randomize_hole_position.py
ros2 run panda_gazebo randomize_welding_line.py
ros2 run panda_gazebo randomize_hand_position.py
```

### Step 4: Spawn the Robot

Inject the Franka Emika Panda robot into the configured world and attach the appropriate tool:

```bash
ros2 launch panda_gazebo put_robot_in_world.launch.py load_gripper:=false gripper:=drill  # Use 'welding' for the weld tool
```

### Step 5: Start Data Collection & Control

Launch the End-Effector (EE) location tracker to monitor distances for the Risk Monitor:

```bash
ros2 run panda_gazebo ee_location.py
```

Finally, trigger the MoveIt 2 motion planning and computer vision execution nodes based on your chosen scenario:

**For Drilling Execution:**
```bash
ros2 run pick_and_place pick_and_place_opencv
```

**For Welding Execution:**
```bash
ros2 run pick_and_place pick_and_place_welding
```

---

## 🛠️ Architecture Highlights

- **panda_gazebo:** Houses the core simulation scenes, randomization scripts, and Gazebo launch files.
- **pick_and_place:** Contains the MoveIt 2 C++ planning nodes and OpenCV-based manipulation logic.
- **obstacles:** Manages dynamic human animations and custom Gazebo plugins for collision/risk tracking.
- **badgers:** Integrated Python library for systematic fault injection and data drift augmentation.