# A Time-series Data Generation Tool for Risk Assessment of Robotic Applications
Yuliang Ma*, Apurv Patel, Don Kurian, Julien Siebert, Silvia Vock, and Andrey Morozov

{yuliang.ma@ias.uni-stuttgart.de}

This work has been accepted for publication in the Proceedings of the 35th European Safety and Reliability & the 33rd Society for Risk Analysis Europe Conference (ESREL SRA-E 2025).

#<img src="/source/Hazard_demo.png" height="220" />
#<img src="/source/framework.png" height="360" />

## Abstract
Robotic systems increasingly rely on artificial intelligence (AI) to enhance their capabilities in performing complex
tasks across various domains. The development and evaluation of AI systems usually require high-quality datasets.
In addition to normal datasets, faulty datasets are critical for enabling anomaly detection and failure prevention,
which are essential for ensuring the safety and reliability of safety-critical robotic applications. However, faults are
rare in real-world environments. Although fault injection techniques allow for the manual injection of configurable
faults, deploying such methods directly in real-world settings is rather risky. As such, it is important to develop
a data generation tool which is low-cost, safe, and efficient. To address this, we developed a time-series data
generation tool for the risk assessment of robotic applications. In this paper, we used Robot Operating System (ROS)
Quigley et al. (2009) as the middleware. This ROS-based simulation tool integrates three key modules: (1) a Gazebobased scene generator that can configure different working scenarios (e.g., drilling and welding) by adjusting endeffectors, workpieces, and hand positions; (2) an online fault injector that can introduce faults into robotic systems
with configurable parameters; and (3) a risk monitor that records faulty data and safety violations in real time by
measuring the distance between hands and end-effectors. Proposed tool facilitates the generation of time-series fault
data and helps identify faults that may pose risks in human-robot collaboration scenarios. Additionally, the proposed
simulation tool enables fast and safe deployment for other robot-related research areas, e.g., deep learning-based
anomaly detection, failure prediction, and risk assessment.

## Citation
Y. Ma, Z. Jin, Q. Liu, I. Mamaev and A. Morozov, "Deep Learning-based Proactive Hazard Prediction for Human-Robot Collaboration with Sensor Malfunctions," 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), Hangzhou, China, 2025, pp. 6328-6335, doi: 10.1109/IROS60139.2025.11246277.



'roslaunch panda_gazebo start_workscene.launch' for drilling world launch.
'roslaunch panda_gazebo start_workscene_welding.launch' for welding launch

rosrun panda_gazebo modify_geometry.py
rosrun panda_gazebo randomize_workpiece_position.py
rosrun panda_gazebo randomize_hole_position.py
rosrun panda_gazebo randomize_welding_line.py
rosrun panda_gazebo randomize_hand_position.py


roslaunch panda_gazebo put_robot_in_world.launch load_gripper:=false gripper:=drill/(welding)

rosrun panda_gazebo ee_location.py


moveit control code:
'rosrun pick_and_place pick_and_place_opencv' for drilling
'rosrun pick_and_place pick_and_place_welding' for welding.

NB: modify_geometry shall be done at first.

