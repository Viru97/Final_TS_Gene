#!/usr/bin/env python3
import sys
import subprocess
import rospy
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QStackedWidget, \
    QLineEdit, QMessageBox, QFrame, QFormLayout, QComboBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import time
import yaml
import random
from sensor_msgs.msg import JointState
# from joint_state_publisher.msg import my_message
# from gui.msg import MycustomMSG
from std_msgs.msg import Int32
from std_msgs.msg import Float32

joint_index = Int32()
fault_amplitude = Float32()
fault_duration = Float32()
start_time = Float32()
# from gui.msg import MyMessage
import threading

class Logos(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a horizontal layout for the logos
        self.layout = QHBoxLayout()  # Instantiate the layout

        # Create QLabel for each logo
        self.logo_ias = QLabel(self)
        self.logo_baua = QLabel(self)
        self.logo_iese = QLabel(self)

        # Load pixmap for each logo
        pixmap_ias = QPixmap('/home/apurv/Downloads/IAS_LOGO.png')
        pixmap_baua = QPixmap('/home/apurv/Downloads/Baua_logo.png')
        pixmap_iese = QPixmap('/home/apurv/Downloads/IESE_logo.png')

        # Scale the IAS logo to 300x300
        scaled_pixmap_ias = pixmap_ias.scaled(450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        scaled_pixmap_iese = pixmap_iese.scaled(450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        scaled_pixmap_baua = pixmap_baua.scaled(450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Set pixmaps on the QLabel widgets
        self.logo_ias.setPixmap(scaled_pixmap_ias)  # Use the scaled pixmap for IAS logo
        self.logo_baua.setPixmap(scaled_pixmap_baua)
        self.logo_iese.setPixmap(scaled_pixmap_iese)

        # Optional: scale the logos if needed
        self.logo_ias.setScaledContents(False)
        self.logo_baua.setScaledContents(False)
        self.logo_iese.setScaledContents(False)

        # Add the QLabel widgets (with pixmaps) to the layout
        self.layout.addWidget(self.logo_ias)  # Add QLabel, not QPixmap
        self.layout.addWidget(self.logo_baua)
        self.layout.addWidget(self.logo_iese)

        # Set the layout for the Logos widget
        self.setLayout(self.layout)

        
class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Logo setup
        self.logos = Logos()
        # Main page layout
        # self.label = QLabel("Please select mode")
        self.button_generator = QPushButton("Generator Mode")
        self.button_demonstrator = QPushButton("Demonstrator Mode")
        # self.image = QLabel(self)
        # pixmap = QPixmap('/home/apurv/Pictures/IAS_LOGO.jpg')
        # self.image.setPixmap(pixmap)
        # self.image.setScaledContents(False)
        # self.resize(pixmap.width(), pixmap.height() + 100)

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        # layout.addWidget(self.image)
        # layout.addWidget(self.label)
        layout.addWidget(self.button_generator)
        layout.addWidget(self.button_demonstrator)
        self.setLayout(layout)


class GeneratorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # Time series data generator page layout
        # self.label = QLabel("This is the Generator Mode page")
        self.button_1 = QPushButton("Welding")
        self.button_2 = QPushButton("Drilling")
        self.button_back = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        # layout.addWidget(self.label)
        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)
        layout.addWidget(self.button_back)
        self.setLayout(layout)


class DemonstratorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # demonstrator page layout
        # self.label = QLabel("This is the Demonstrator Mode page, Please select task")
        self.button_welding = QPushButton("Welding")
        self.button_drilling = QPushButton("Drilling")
        self.button_back = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        # layout.addWidget(self.label)
        layout.addWidget(self.button_welding)
        layout.addWidget(self.button_drilling)
        layout.addWidget(self.button_back)
        self.setLayout(layout)


class DrillingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # Scene generator page layout
        self.label = QLabel("Drilling Task")
        # self.text_length = QLineEdit(self)
        # self.text_length.setPlaceholderText("Workpiece Length")
        # self.text_width = QLineEdit(self)
        # self.text_width.setPlaceholderText("Workpiece Width")

        # self.button_accept = QPushButton("Accept")
        self.button_randomize_geometry = QPushButton("Randomize Geometry")
        self.button_randomize_position = QPushButton("Randomize Position")
        self.button_next = QPushButton("Next")
        self.button_back = QPushButton("Back")
        self.button_kill = QPushButton("Kill Gazebo")

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        # layout.addWidget(self.text_length)
        # layout.addWidget(self.text_width)
        # layout.addWidget(self.button_accept)
        layout.addWidget(self.button_randomize_geometry)
        layout.addWidget(self.button_randomize_position)
        layout.addWidget(self.button_next)
        layout.addWidget(self.button_back)
        layout.addWidget(self.button_kill)
        self.setLayout(layout)
        
class WeldingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # Scene generator page layout
        self.label = QLabel("Welding Task")
        # self.text_length = QLineEdit(self)
        # self.text_length.setPlaceholderText("Workpiece Length")
        # self.text_width = QLineEdit(self)
        # self.text_width.setPlaceholderText("Workpiece Width")

        # self.button_accept = QPushButton("Accept")
        self.button_welding_randomize_geometry = QPushButton("Randomize Geometry")
        self.button_welding_randomize_position = QPushButton("Randomize Position")
        self.button_welding_next = QPushButton("Next")
        self.button_welding_back = QPushButton("Back")
        self.button_welding_kill = QPushButton("Kill Gazebo")

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        # layout.addWidget(self.text_length)
        # layout.addWidget(self.text_width)
        # layout.addWidget(self.button_accept)
        layout.addWidget(self.button_welding_randomize_geometry)
        layout.addWidget(self.button_welding_randomize_position)
        layout.addWidget(self.button_welding_next)
        layout.addWidget(self.button_welding_back)
        layout.addWidget(self.button_welding_kill)
        self.setLayout(layout)


# class DrillingRandomWorkpiecePositionPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         self.label = QLabel("Drilling Task, Please configure Workpiece position")

#         self.button_randomize = QPushButton("randomize")
#         self.button_kill = QPushButton("Kill Gazebo")
#         self.button_accept = QPushButton("Accept")
#         self.button_back = QPushButton("Back")

#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.button_randomize)
#         layout.addWidget(self.button_accept)
#         layout.addWidget(self.button_kill)
#         layout.addWidget(self.button_back)
#         self.setLayout(layout)


class SetHolesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.logos = Logos()

        self.label = QLabel("Drilling Task")

        self.button_randomize_holes = QPushButton("Randomize Drill Location")
        self.button_randomize_hands = QPushButton("Randomize Hands Location")
        self.button_kill = QPushButton("Kill Gazebo")
        self.button_accept = QPushButton("Next")
        self.button_back = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.addWidget(self.button_randomize_holes)
        layout.addWidget(self.button_randomize_hands)
        layout.addWidget(self.button_accept)
        layout.addWidget(self.button_back)
        layout.addWidget(self.button_kill)
        self.setLayout(layout)


class SetWeldingLinePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.logos = Logos()

        self.label = QLabel("Welding Task")

        self.button_welding_randomize_line = QPushButton("Randomize Welding Path")
        self.button_welding_randomize_hands = QPushButton("Randomize Hand Location")
        self.button_welding_kill = QPushButton("Kill Gazebo")
        self.button_welding_next = QPushButton("Next")
        self.button_welding_back = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.addWidget(self.button_welding_randomize_line)
        layout.addWidget(self.button_welding_randomize_hands)
        layout.addWidget(self.button_welding_next)
        layout.addWidget(self.button_welding_back)
        layout.addWidget(self.button_welding_kill)
        self.setLayout(layout)


class DrillingExecutionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # Logos (Make sure Logos is properly defined)
        self.logos = Logos()  # Ensure the Logos class is well-structured

        # Labels
        self.label = QLabel("Drilling Task")
        self.label_1 = QLabel("Fault Information\nFault Duration:")
        self.label_2 = QLabel("Fault Amplitude:")
        self.label_3 = QLabel("Fault Location:")
        self.label_T = QLabel("Fault Time:")

        # Buttons
        self.button_add_robot = QPushButton("Add Robot")
        self.button_start = QPushButton("Start Execution")
        self.button_stop = QPushButton("Stop")
        self.button_kill = QPushButton("Kill Gazebo")
        self.button_back = QPushButton("Back")
        self.button_fault_generator = QPushButton("Generate Fault")
        self.button_fault_injector = QPushButton("Inject Fault")
        self.button_fault_remover = QPushButton("Remove Fault")

        # Frames and layouts for structuring UI components
        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.label)
        layout_1.addWidget(self.button_add_robot)
        layout_1.addWidget(self.button_start)
        layout_1.addWidget(self.button_stop)
        layout_1.addWidget(self.button_back)
        layout_1.addWidget(self.button_kill)
        self.frame_1 = QFrame(self)
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setLayout(layout_1)

        layout_2 = QVBoxLayout()
        self.label_4 = QLabel(self)
        self.label_4.setText('Please select Fault Mode')
        self.dropdown = QComboBox(self)
        self.dropdown.addItem('Bias')
        self.dropdown.addItem('Noise')
        self.dropdown.currentIndexChanged.connect(self.fault_options)

        layout_2.addWidget(self.label_4)
        layout_2.addWidget(self.dropdown)
        layout_2.addWidget(self.button_fault_generator)
        layout_2.addWidget(self.button_fault_injector)
        layout_2.addWidget(self.button_fault_remover)
        self.frame_2 = QFrame(self)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setLayout(layout_2)

        layout_3 = QVBoxLayout()
        layout_3.addWidget(self.label_1)
        layout_3.addWidget(self.label_2)
        layout_3.addWidget(self.label_3)
        layout_3.addWidget(self.label_T)
        self.frame_3 = QFrame(self)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setLayout(layout_3)

        # Main layout to hold all the frames
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.frame_1)
        main_layout.addWidget(self.frame_2)
        main_layout.addWidget(self.frame_3)

        # Outer layout that combines the logos and the main content
        layout = QVBoxLayout()
        layout.addWidget(self.logos)  # Ensure Logos is a valid QWidget
        layout.addLayout(main_layout)  # Use addLayout instead of addWidget for layouts

        self.setLayout(layout)

    def fault_options(self):
        selected_option = self.dropdown.currentText()
        self.label_4.setText(f'Selected: {selected_option}')


class WeldingExecutionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # Logos (Make sure Logos is properly defined)
        self.logos = Logos()  # Ensure the Logos class is well-structured

        # Labels
        self.label = QLabel("Welding Task")
        self.label_1 = QLabel("Fault Information\n\nFault Duration:")
        self.label_2 = QLabel("Fault Amplitude:")
        self.label_3 = QLabel("Fault Location:")
        self.label_T = QLabel("Fault Time:")

        # Buttons
        self.button_welding_add_robot = QPushButton("Add Robot")
        self.button_welding_start = QPushButton("Start Execution")
        self.button_welding_stop = QPushButton("Stop")
        self.button_welding_kill = QPushButton("Kill Gazebo")
        self.button_welding_back = QPushButton("Back")
        self.button_welding_fault_generator = QPushButton("Generate Fault")
        self.button_welding_fault_injector = QPushButton("Inject Fault")
        self.button_welding_fault_remover = QPushButton("Remove Fault")

        # Frames and layouts for structuring UI components
        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.label)
        layout_1.addWidget(self.button_welding_add_robot)
        layout_1.addWidget(self.button_welding_start)
        layout_1.addWidget(self.button_welding_stop)
        layout_1.addWidget(self.button_welding_back)
        layout_1.addWidget(self.button_welding_kill)
        self.frame_1 = QFrame(self)
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setLayout(layout_1)

        layout_2 = QVBoxLayout()
        self.label_4 = QLabel(self)
        self.label_4.setText('Please select Fault Mode')
        self.dropdown = QComboBox(self)
        self.dropdown.addItem('Bias')
        self.dropdown.addItem('Noise')
        self.dropdown.currentIndexChanged.connect(self.fault_options)

        layout_2.addWidget(self.label_4)
        layout_2.addWidget(self.dropdown)
        layout_2.addWidget(self.button_welding_fault_generator)
        layout_2.addWidget(self.button_welding_fault_injector)
        layout_2.addWidget(self.button_welding_fault_remover)
        self.frame_2 = QFrame(self)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setLayout(layout_2)

        layout_3 = QVBoxLayout()
        layout_3.addWidget(self.label_1)
        layout_3.addWidget(self.label_2)
        layout_3.addWidget(self.label_3)
        layout_3.addWidget(self.label_T)
        self.frame_3 = QFrame(self)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setLayout(layout_3)

        # Main layout to hold all the frames
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.frame_1)
        main_layout.addWidget(self.frame_2)
        main_layout.addWidget(self.frame_3)

        # Outer layout that combines the logos and the main content
        layout = QVBoxLayout()
        layout.addWidget(self.logos)  # Ensure Logos is a valid QWidget
        layout.addLayout(main_layout)  # Use addLayout instead of addWidget for layouts

        self.setLayout(layout)

    def fault_options(self):
        selected_option = self.dropdown.currentText()
        self.label_4.setText(f'Selected: {selected_option}')
        
class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gazebo_process = None
        self.put_robot_in_gazebo = None
        self.execution_process = None
        self.drilling_flag = None  # Ensure the flag is initialized
        self.welding_flag = None  # Ensure the flag is initialized
        self.fault_location = None
        self.fault_amplitude = None
        self.fault_duration = None
        self.start_time = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Time Series Data Generator")
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of each page
        self.pages = {
            'main': MainPage(),
            'generator': GeneratorPage(),
            'demonstrator': DemonstratorPage(),
            'drilling': DrillingPage(),
            'drilling_set_holes': SetHolesPage(),
            'drilling_execution': DrillingExecutionPage(),
            'welding': WeldingPage(),
            'welding_set_line': SetWeldingLinePage(),
            'welding_execution': WeldingExecutionPage(),
        }

        # Add pages to the stacked widget
        for page in self.pages.values():
            self.stacked_widget.addWidget(page)

        # Connect buttons
        self.connect_buttons()

        # Show the main page initially
        self.stacked_widget.setCurrentWidget(self.pages['main'])

    def connect_buttons(self):
        # Main Page Buttons
        self.pages['main'].button_generator.clicked.connect(self.go_to_generator_page)
        self.pages['main'].button_demonstrator.clicked.connect(self.go_to_demonstrator_page)

        # Time Series Page Buttons
        self.pages['generator'].button_back.clicked.connect(self.go_to_main_page)

        # Scene Generator Page Buttons
        self.pages['demonstrator'].button_drilling.clicked.connect(self.go_to_drilling_page)
        self.pages['demonstrator'].button_welding.clicked.connect(self.go_to_welding_page)
        self.pages['demonstrator'].button_back.clicked.connect(self.go_to_main_page)

        # Drilling Page Buttons
        # self.pages['drilling'].button_accept.clicked.connect(self.configure_workpiece)
        self.pages['drilling'].button_randomize_geometry.clicked.connect(self.randomize_geometry)
        self.pages['drilling'].button_randomize_position.clicked.connect(self.randomize_position)
        self.pages['drilling'].button_next.clicked.connect(self.go_to_set_holes_page)
        self.pages['drilling'].button_back.clicked.connect(self.go_to_demonstrator_page)
        self.pages['drilling'].button_kill.clicked.connect(self.kill_gazebo)


        self.pages['welding'].button_welding_randomize_geometry.clicked.connect(self.randomize_geometry)
        self.pages['welding'].button_welding_randomize_position.clicked.connect(self.randomize_position)
        self.pages['welding'].button_welding_next.clicked.connect(self.go_to_set_welding_line_page)
        self.pages['welding'].button_welding_back.clicked.connect(self.go_to_demonstrator_page)
        self.pages['welding'].button_welding_kill.clicked.connect(self.kill_gazebo)

        # # Random Position Page Buttons
        # self.pages['random_position'].button_randomize.clicked.connect(self.randomize_position)
        # self.pages['random_position'].button_accept.clicked.connect(self.go_to_set_holes_page)
        # self.pages['random_position'].button_back.clicked.connect(self.go_to_drilling_page)
        # self.pages['random_position'].button_kill.clicked.connect(self.kill_gazebo)

        # Set Holes Page Buttons
        self.pages['drilling_set_holes'].button_randomize_holes.clicked.connect(self.randomize_holes)
        self.pages['drilling_set_holes'].button_randomize_hands.clicked.connect(self.randomize_hands)
        self.pages['drilling_set_holes'].button_accept.clicked.connect(self.go_to_drilling_execution_page)
        self.pages['drilling_set_holes'].button_back.clicked.connect(self.go_to_drilling_page)
        self.pages['drilling_set_holes'].button_kill.clicked.connect(self.kill_gazebo)



        self.pages['welding_set_line'].button_welding_randomize_line.clicked.connect(self.randomize_line)
        self.pages['welding_set_line'].button_welding_randomize_hands.clicked.connect(self.randomize_hands)
        self.pages['welding_set_line'].button_welding_next.clicked.connect(self.go_to_welding_execution_page)
        self.pages['welding_set_line'].button_welding_back.clicked.connect(self.go_to_welding_page)
        self.pages['welding_set_line'].button_welding_kill.clicked.connect(self.kill_gazebo)

        # Execution Page Buttons
        self.pages['drilling_execution'].button_add_robot.clicked.connect(self.add_drilling_robot)
        self.pages['drilling_execution'].button_start.clicked.connect(self.start_drilling_execution)
        self.pages['drilling_execution'].button_stop.clicked.connect(self.stop_drilling_execution)
        self.pages['drilling_execution'].button_back.clicked.connect(self.go_to_set_holes_page)
        self.pages['drilling_execution'].button_kill.clicked.connect(self.kill_gazebo)
        
        self.pages['drilling_execution'].button_fault_generator.clicked.connect(self.fault_generator)
        self.pages['drilling_execution'].button_fault_injector.clicked.connect(self.fault_injector)
        
        self.pages['welding_execution'].button_welding_add_robot.clicked.connect(self.add_welding_robot)
        self.pages['welding_execution'].button_welding_start.clicked.connect(self.start_welding_execution)
        self.pages['welding_execution'].button_welding_stop.clicked.connect(self.stop_welding_execution)
        self.pages['welding_execution'].button_welding_back.clicked.connect(self.go_to_set_welding_line_page)
        self.pages['welding_execution'].button_welding_kill.clicked.connect(self.kill_gazebo)
        
        self.pages['welding_execution'].button_welding_fault_generator.clicked.connect(self.fault_generator)
        self.pages['welding_execution'].button_welding_fault_injector.clicked.connect(self.fault_injector)

    def go_to_main_page(self):
        self.stacked_widget.setCurrentWidget(self.pages['main'])
        print("Switched to MainPage")

    def go_to_demonstrator_page(self):
        current_widget = self.stacked_widget.currentWidget()
        class_name = type(current_widget).__name__
        
        if class_name == "DrillingPage":
            self.kill_gazebo()
        self.stacked_widget.setCurrentWidget(self.pages['demonstrator'])

    def go_to_generator_page(self):
        self.stacked_widget.setCurrentWidget(self.pages['generator'])
        print("Switched to GeneratorPage")

    def go_to_drilling_page(self):
        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, DemonstratorPage):
            self.launch_gazebo('roslaunch', 'panda_gazebo', 'start_workscene.launch')
        self.stacked_widget.setCurrentWidget(self.pages['drilling'])

    def go_to_welding_page(self):
        current_widget = self.stacked_widget.currentWidget()
        class_name = type(current_widget).__name__

        self.stacked_widget.setCurrentWidget(self.pages['welding'])
        if class_name == "DemonstratorPage":
            self.launch_gazebo('roslaunch', 'panda_gazebo', 'start_workscene_welding.launch')    
        # else:
        #     print(f"This is not the MainPage, it's {class_name}.")
        

    # def go_to_drilling_random_workpiece_position_page(self):
    #     self.stacked_widget.setCurrentWidget(self.pages['drilling_random_position'])

    def go_to_set_holes_page(self):
    # Check if the current widget is the ExecutionPage
        self.stacked_widget.setCurrentWidget(self.pages['drilling_set_holes'])

        if isinstance(self.stacked_widget.currentWidget(), DrillingExecutionPage):
            self.remove_robot()

    def go_to_set_welding_line_page(self):
        # Check if the current widget is the ExecutionPage
        self.stacked_widget.setCurrentWidget(self.pages['welding_set_line'])

        if isinstance(self.stacked_widget.currentWidget(), WeldingExecutionPage):
                self.remove_robot()

    def go_to_drilling_execution_page(self):
        if self.drilling_flag:
            self.stacked_widget.setCurrentWidget(self.pages['drilling_execution'])


    def go_to_welding_execution_page(self):
            if self.flag:
                self.stacked_widget.setCurrentWidget(self.pages['welding_execution'])
        
    def launch_gazebo(self, *args):
        try:
            self.gazebo_process = subprocess.Popen(args)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error launching Gazebo: {e}")

    def kill_gazebo(self):
        if self.gazebo_process:
            self.gazebo_process.terminate()
            try:
                self.gazebo_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.gazebo_process.kill()
            finally:
                self.gazebo_process = None
                subprocess.run(['pkill', '-f', 'gzserver'], check=False)
                subprocess.run(['pkill', '-f', 'gzclient'], check=False)
            rospy.logwarn('Gazebo Terminated')

    def randomize_geometry(self):
        self.run_command(['rosrun', 'panda_gazebo', 'modify_geometry.py'])
        # self.run_command(['rosrun', 'panda_gazebo', 'randomize_workpiece_position.py'])

    def randomize_position(self):
        # self.run_command(['rosrun', 'panda_gazebo', 'modify_geometry.py'])
        self.run_command(['rosrun', 'panda_gazebo', 'randomize_workpiece_position.py'])

    def randomize_holes(self):
        self.run_command(['rosrun', 'panda_gazebo', 'randomize_hole_position.py'])
        self.drilling_flag = True
        return self.drilling_flag
    
    def randomize_line(self):
        self.run_command(['rosrun', 'panda_gazebo', 'randomize_welding_line.py'])
        self.welding_flag = True
        return self.welding_flag
    
    def randomize_hands(self):
        self.run_command(['rosrun', 'panda_gazebo', 'randomize_hand_position.py'])
    
    def run_command(self, command):
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def add_drilling_robot(self):
        if self.put_robot_in_gazebo:
            QMessageBox.critical(self, "Robot is already in the scene")
        else:

            try:
                # subprocess.Popen(['rqt_plot'])
                self.put_robot_in_gazebo = subprocess.Popen(
                    ['roslaunch', 'panda_gazebo', 'put_robot_in_world.launch', 'load_gripper:=false', 'gripper:=drill']
                )
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Error adding robot: {e}")
                
    def add_welding_robot(self):
        if self.put_robot_in_gazebo:
            QMessageBox.critical(self, "Robot is already in the scene")
        else:

            try:
                # subprocess.Popen(['rqt_plot'])
                self.put_robot_in_gazebo = subprocess.Popen(
                    ['roslaunch', 'panda_gazebo', 'put_robot_in_world.launch', 'load_gripper:=false', 'gripper:=welding']
                )
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Error adding robot: {e}")

    def start_drilling_execution(self):
        try:
            self.execution_process = subprocess.Popen(['rosrun', 'pick_and_place', 'drilling.py'])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error starting execution: {e}")

    def start_welding_execution(self):
            try:
                self.execution_process = subprocess.Popen(['rosrun', 'pick_and_place', 'welding.py'])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting execution: {e}")


    def stop_drilling_execution(self):
        if self.execution_process:
            self.execution_process.terminate()
            try:
                self.execution_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                rospy.logwarn("Execution did not terminate gracefully, killing it forcefully")
                self.execution_process.kill()
            finally:
                self.execution_process = None
            rospy.logwarn("Drilling execution terminated")

        else:
            rospy.logwarn("No execution process running.")
            

    def stop_welding_execution(self):
        # Stop execution logic here
        if self.execution_process:
            # Attempt to terminate the process gracefully
            self.execution_process.terminate()
            try:
                self.execution_process.wait(timeout=5)  # Wait for up to 10 seconds for the process to terminate
            except subprocess.TimeoutExpired:
                print("Execution did not terminate gracefully, killing it forcefully.")
                self.execution_process.kill()  # Force kill if it doesn't terminate
            finally:
                # Ensure the process is cleaned up
                self.execution_process = None

            rospy.logwarn("Execution process terminated.")
        else:
            rospy.logwarn("No execution process running.")
            

    def fault_generator(self):

        global joint_index, fault_amplitude, fault_duration, start_time
        try:
            with open("/home/baua/Final_TS_Gene/spike_config.yaml", 'r') as file:
                data = yaml.safe_load(file)
                fault_duration_min = data['fault_duration_min']
                fault_duration_max = data['fault_duration_max']
                fault_amplitude_min = data['fault_amplitude_min']
                fault_amplitude_max = data['fault_amplitude_max']
                fault_joints = data['joint_names']

            self.fault_duration = round(random.uniform(fault_duration_min, fault_duration_max), 2)
            self.fault_amplitude = round(random.uniform(fault_amplitude_min, fault_amplitude_max), 2)
            self.fault_location = random.choice(fault_joints)
            self.joint_index = fault_joints.index(self.fault_location)
            self.start_time = rospy.get_time() + round(random.uniform(2 , 30))

            fault_duration.data = self.fault_duration
            fault_amplitude .data= self.fault_amplitude
            joint_index.data = self.joint_index
            start_time.data = self.start_time

            current_widget = self.stacked_widget.currentWidget()
            class_name = type(current_widget).__name__

            if class_name == "DrillingExecutionPage":
                self.pages['drilling_execution'].label_1.setText(f"Fault Information\n\nFault Duration: {self.fault_duration}")
                self.pages['drilling_execution'].label_2.setText(f"Fault Amplitude: {self.fault_amplitude}")
                self.pages['drilling_execution'].label_3.setText(f"Fault Location: {self.fault_location}")
                self.pages['drilling_execution'].label_T.setText(f"Fault Time: {self.start_time}")
            elif class_name == "WeldingExecutionPage":
                self.pages['welding_execution'].label_1.setText(f"Fault Information\n\nFault Duration: {self.fault_duration}")
                self.pages['welding_execution'].label_2.setText(f"Fault Amplitude: {self.fault_amplitude}")
                self.pages['welding_execution'].label_3.setText(f"Fault Location: {self.fault_location}")
                self.pages['welding_execution'].label_T.setText(f"Fault Time: {self.start_time}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating fault: {e}")

        rospy.logwarn('Fault created successfully')

        return self.joint_index, self.fault_amplitude, self.fault_duration, self.start_time
    
    def fault_injector(self):
        global pub_state
        sub.unregister()
        pub.unregister()  # Assuming pub is your publisher; define it globally if needed

        pub_state = False
        rospy.logwarn('launching fault injector node')

        fault_thread = threading.Thread(target=lambda: self.run_command(['rosrun', 'joint_state_publisher', 'fault_injector']))
        fault_thread.start()
        # data = my_message()
        # joint_index_msg = Int32()
        # fault_amplitude_msg = Float32()
        # fault_duration_msg = Float32()
        # start_time_msg = Float32()
        # data.joint_index = self.joint_index
        # data.fault_amplitude = self.fault_amplitude
        # data.fault_duration = self.fault_duration
        # data.start_time = self.start_time        
        
        # global joint_index, fault_amplitude, fault_duration, start_time
        # joint_index_msg = joint_index
        # fault_amplitude_msg = fault_amplitude
        # fault_duration_msg = fault_duration
        # start_time_msg = start_time

        # rate = rospy.Rate(2)
        # while not rospy.is_shutdown():
        while pub_index.get_num_connections() == 0 or pub_amplitude.get_num_connections == 0 or pub_duration.get_num_connections == 0 or pub_time.get_num_connections == 0 :
            rospy.loginfo("Waiting for subscribers...")
            rospy.sleep(0.01)
        for i in range(20):
            print(fault_duration.data)
            # pub2.publish(data)  # Publish to ROS topics
            pub_index.publish(joint_index)  # Publish to ROS topics
            pub_amplitude.publish(fault_amplitude)  # Publish to ROS topics
            pub_duration.publish(fault_duration)  # Publish to ROS topics
            pub_time.publish(start_time)  # Publish to ROS topics
            rospy.sleep(0.1)
        rospy.logwarn('Fault inserted successfully')
        return pub_state

    def remove_fault():
        pass



# ROS-related code for publisher and subscriber
def joint_callback(jointstate: JointState):
    
    pub.publish(jointstate)

    # if pub_state:
        # pub.publish(jointstate)

            # pub2.publish(data)  # Publish to ROS topics
    # pub_index.publish(joint_index)  # Publish to ROS topics
    # pub_amplitude.publish(fault_amplitude)  # Publish to ROS topics
    # pub_duration.publish(fault_duration)  # Publish to ROS topics
    # pub_time.publish(start_time)  # Publish to ROS topics


def ros_spin():
    rospy.spin()


if __name__ == "__main__":


    rospy.init_node("Run")

    # Publisher for /faulty_joint_states
    pub = rospy.Publisher('/faulty_joint_states', JointState, queue_size=100)
    pub_state = True
    # pub2 = rospy.Publisher('fault_data', my_message, queue_size=100)
    pub_index = rospy.Publisher('fault_index', Int32, queue_size=50)
    pub_duration = rospy.Publisher('fault_duration', Float32, queue_size=50)
    pub_amplitude = rospy.Publisher('fault_amplitude', Float32, queue_size=50)
    pub_time = rospy.Publisher('fault_time', Float32, queue_size=50)

    # Subscriber for /joint_states
    sub = rospy.Subscriber('/joint_states', JointState, callback=joint_callback)

    # Start ROS spin in a separate thread
    ros_thread = threading.Thread(target=ros_spin)
    ros_thread.start()

    # GUI-related code
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('/home/apurv/Downloads/icon.png'))
    win = Gui()
    win.show()
    sys.exit(app.exec_())