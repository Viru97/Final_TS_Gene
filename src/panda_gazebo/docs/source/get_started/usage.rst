==========
How to use
==========

The :panda-gazebo:`panda_gazebo <>` package contains three types of launch files: **world**, **robot** and **simulation** launch files.

**World launch files**

World launch files start Gazebo and load a world where the Panda robot can be trained. *They don't spawn the robot*.

    - ``start_reach_world.launch``: Provides a clear environment for reach task training with the robot.
    - ``start_push_world.launch``: Positions the Panda robot and a box on a table for push task simulations.
    - ``start_pick_and_place_world.launch``: Includes a table and cube, creating a scenario for pick-and-place exercises.
    - ``start_slide_world.launch``: Contains a puck and a designated target area to practice precision sliding tasks.

**Robot launch file**

The ``put_robot_in_world.launch`` robot launch files spawn the Panda robot in Gazebo and load the required control services. The robot currently contains three control
modes that can be selected using the ``control_mode`` argument:

    - ``trajectory``: The robot is controlled using joint position trajectories.
    - ``position``: The robot is controlled using joint position commands.
    - ``effort``: The robot is controlled using joint effort commands.    

.. Note::

    You can test different control modes using the
    :mod:`joint_efforts_dynamic_reconfigure_server` and
    :mod:`joint_positions_dynamic_reconfigure_server` helper nodes.
    In the ROS 2 port these are command helper nodes (not ROS 1 dynamic
    reconfigure servers) that publish effort/position commands and send gripper
    actions.

    Furthermore, you can explore trajectory control using the `MoveIt! package`_ or `rqt_joint_trajectory_controller package`_. To enable `MoveIt!`, set the
    ``use_moveit`` launch file argument to ``true``. Once enabled, you can control the robot through the `RViz Motion Planning`_ panel. For detailed instructions on how to
    use `MoveIt!`_, consult the `MoveIt! tutorials`_.

.. _`MoveIt! package`: https://moveit.ros.org/
.. _`rqt_joint_trajectory_controller package`: https://wiki.ros.org/rqt_joint_trajectory_controller
.. _`RViz Motion Planning`: https://ros-planning.github.io/moveit_tutorials/doc/quickstart_in_rviz/quickstart_in_rviz_tutorial.html
.. _`MoveIt!`: https://ros-planning.github.io/moveit_tutorials/
.. _`MoveIt! tutorials`: https://ros-planning.github.io/moveit_tutorials/

**Simulation launch file**

The ``start_simulation.launch`` launch file combines the two other launch files to start the gazebo world and spawns the Panda robot.

Usage instructions
------------------

You can launch any launch files using the ``ros2 launch`` command-line tool.
For example, to start a Gazebo simulation of the Panda robot:

.. code-block:: bash

    ros2 launch panda_gazebo start_simulation.launch.py
