#!/usr/bin/env python3
import os
import sys
import subprocess
import rospy
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QStackedWidget, \
    QLineEdit, QMessageBox, QFrame, QFormLayout, QComboBox, QCheckBox, QSizePolicy, QButtonGroup, QProgressBar, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
import time
import yaml
import random
from sensor_msgs.msg import JointState
# from joint_state_publisher.msg import my_message
# from gui.msg import MycustomMSG
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from gazebo_msgs.srv import DeleteModel
import datetime
joint_index = Int32()
fault_amplitude = Float32()
fault_duration = Float32()
start_time = Float32()
fault_type = Int32()
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
        self.label = QLabel("Modes:")
        # font = QFont()
        # font.setPointSize(16)  # Set the font size to 16
        # self.label.setFont(font)

        # self.label.setFixedSize(500, 100)  # Width: 200px, Height: 100px
        self.button_generator = QPushButton("Generator")
        self.button_generator.setFixedSize(400,80)
        self.button_demonstrator = QPushButton("Demonstrator")
        self.button_demonstrator.setFixedSize(400,80)

        # self.image = QLabel(self)
        # pixmap = QPixmap('/home/apurv/Pictures/IAS_LOGO.jpg')
        # self.image.setPixmap(pixmap)
        # self.image.setScaledContents(False)
        # self.resize(pixmap.width(), pixmap.height() + 100)

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        # layout.addWidget(self.image)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)
        layout.addWidget(self.button_generator)
        layout.setAlignment(self.button_generator, Qt.AlignCenter)
        layout.addWidget(self.button_demonstrator)
        layout.setAlignment(self.button_demonstrator, Qt.AlignCenter)

        self.setLayout(layout)


class GeneratorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # demonstrator page layout
        self.label = QLabel("Tasks:")
        # font = QFont()
        # font.setPointSize(16)  # Set the font size to 16
        # self.label.setFont(font)
        self.button_welding = QPushButton("Welding")
        self.button_welding.setFixedSize(400,80)

        self.button_drilling = QPushButton("Drilling")
        self.button_drilling.setFixedSize(400,80)

        self.button_back = QPushButton("Back")
        self.button_back.setFixedSize(150,80)
        self.button_back.setIconSize(self.button_back.sizeHint())  # Optionally, set the icon size to match button size
        self.button_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))


        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)
        layout.addWidget(self.button_welding)
        layout.setAlignment(self.button_welding, Qt.AlignCenter)
        layout.addWidget(self.button_drilling)
        layout.setAlignment(self.button_drilling, Qt.AlignCenter)

        # layout.addWidget(self.button_back)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_back)
        h_layout.setAlignment(self.button_back, Qt.AlignLeft)
        layout.addLayout(h_layout)
        self.setLayout(layout)
    


class DemonstratorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # demonstrator page layout
        self.label = QLabel("Tasks:")
        # font = QFont()
        # font.setPointSize(16)  # Set the font size to 16
        # self.label.setFont(font)
        self.button_welding = QPushButton("Welding")
        self.button_welding.setFixedSize(400,80)

        self.button_drilling = QPushButton("Drilling")
        self.button_drilling.setFixedSize(400,80)

        self.button_back = QPushButton("Back")
        self.button_back.setFixedSize(150,80)
        self.button_back.setIconSize(self.button_back.sizeHint())  # Optionally, set the icon size to match button size
        self.button_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))


        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)
        layout.addWidget(self.button_welding)
        layout.setAlignment(self.button_welding, Qt.AlignCenter)
        layout.addWidget(self.button_drilling)
        layout.setAlignment(self.button_drilling, Qt.AlignCenter)

        # layout.addWidget(self.button_back)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_back)
        h_layout.setAlignment(self.button_back, Qt.AlignLeft)
        layout.addLayout(h_layout)
        self.setLayout(layout)

class Drill_GeneratorPage(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.logos = Logos()  # Ensure the Logos class is well-structured

        self.button_go = QPushButton("Go")
        self.button_go.setFixedSize(150, 80)

        # "Back" button
        self.button_back = QPushButton("Back")
        self.button_back.setFixedSize(150, 80)
        self.button_back.setIconSize(self.button_back.sizeHint())
        self.button_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))

        # Labels
        self.label = QLabel("1) Runs:")
        self.label_1 = QLabel("2) Fault Duration:")
        self.label_2 = QLabel("3) Fault Amplitude:")
        self.label_3 = QLabel("4) Fault Type:")
        self.label_4 = QLabel("5) Fault Location:")

        self.run_value = 0
        self.run_label = QLabel(str(self.run_value))
        self.run_label.setFixedSize(80, 80)
        self.run_label.setAlignment(Qt.AlignCenter)

        # Adding border around the run label
        self.run_label.setStyleSheet("""
            QLabel {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
            }
        """)

        self.button_up = QPushButton("▲")
        self.button_down = QPushButton("▼")

        # Set a fixed size for smaller buttons
        self.button_up.setFixedSize(50, 40)
        self.button_down.setFixedSize(50, 40)

        # Set size policy to fixed
        self.button_up.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_down.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        arrow_layout = QVBoxLayout()
        arrow_layout.setSpacing(5)  # Adjust spacing if necessary
        arrow_layout.addWidget(self.button_up, alignment=Qt.AlignLeft)
        arrow_layout.addWidget(self.button_down, alignment=Qt.AlignLeft)

        self.button_up.clicked.connect(self.increase_run_value)
        self.button_down.clicked.connect(self.decrease_run_value)

        duration_min_label = QLabel("Min:")
        duration_max_label = QLabel("Max:")

        self.duration_min = QLineEdit()
        self.duration_min.setFixedSize(100, 80)
        self.duration_min.setPlaceholderText("Min")
        self.duration_min.setText("1")
          # Set default value for duration_min
        self.duration_max = QLineEdit()
        self.duration_max.setFixedSize(100, 80)
        self.duration_max.setPlaceholderText("Max")
        self.duration_max.setText("2")  # Set default value for duration_min
        # Styling for input boxes
        self.duration_min.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        self.duration_max.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        # Creating the layout for Duration
        duration_layout = QVBoxLayout()

        # Horizontal layout for Min
        min_layout = QHBoxLayout()
        min_layout.addWidget(duration_min_label, alignment=Qt.AlignLeft)
        min_layout.addWidget(self.duration_min, alignment=Qt.AlignLeft)
        duration_layout.addLayout(min_layout)

        # Horizontal layout for Max
        max_layout = QHBoxLayout()
        max_layout.addWidget(duration_max_label, alignment=Qt.AlignLeft)
        max_layout.addWidget(self.duration_max, alignment=Qt.AlignLeft)
        duration_layout.addLayout(max_layout)

        ##############
        amplitude_min_label = QLabel("Min:")
        amplitude_max_label = QLabel("Max:")

        self.amplitude_min = QLineEdit()
        self.amplitude_min.setFixedSize(100, 80)
        self.amplitude_min.setPlaceholderText("Min")
        self.amplitude_min.setText("0.1")  # Set default value for duration_min
        
        self.amplitude_max = QLineEdit()
        self.amplitude_max.setFixedSize(100, 80)
        self.amplitude_max.setPlaceholderText("Max")
        self.amplitude_max.setText("0.5")  # Set default value for duration_min

        # Styling for input boxes
        self.amplitude_min.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        self.amplitude_max.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        # Creating the layout for Amplitude
        amplitude_layout = QVBoxLayout()

        # Horizontal layout for Min
        amp_min_layout = QHBoxLayout()
        amp_min_layout.addWidget(amplitude_min_label, alignment=Qt.AlignLeft)
        amp_min_layout.addWidget(self.amplitude_min, alignment=Qt.AlignLeft)
        amplitude_layout.addLayout(amp_min_layout)

        # Horizontal layout for Max
        amp_max_layout = QHBoxLayout()
        amp_max_layout.addWidget(amplitude_max_label, alignment=Qt.AlignLeft)
        amp_max_layout.addWidget(self.amplitude_max, alignment=Qt.AlignLeft)
        amplitude_layout.addLayout(amp_max_layout)

        # Frames and layouts for structuring UI components
        layout_h1 = QHBoxLayout()
        layout_h1.addWidget(self.label)  # 1) Runs:
        layout_h1.addWidget(self.run_label)
        layout_h1.addLayout(arrow_layout)

        # Create a layout for the Fault Type label and its corresponding checkbox
        layout_h4 = QHBoxLayout()
        layout_h4.addWidget(self.label_3)  # 4) Fault Type:
        
        # Checkbox layout for Noise and Bias
        self.checkbox_noise = QCheckBox("Noise")
        self.checkbox_noise.setChecked(False)  # Set initial state
        self.checkbox_noise.stateChanged.connect(self.checkbox_state_changed)

        self.checkbox_bias = QCheckBox("Bias")
        self.checkbox_bias.setChecked(False)  # Set initial state
        self.checkbox_bias.stateChanged.connect(self.checkbox_state_changed)

        # self.checkbox_group = QButtonGroup(self)
        # self.checkbox_group.addButton(self.checkbox_noise)
        # self.checkbox_group.addButton(self.checkbox_bias)
        # self.checkbox_group.setExclusive(True)  # Ensure checkboxes act like radio buttons

        self.layout_v1 = QVBoxLayout()
        self.layout_v1.addWidget(self.checkbox_noise)
        self.layout_v1.addWidget(self.checkbox_bias)

        layout_h4.addLayout(self.layout_v1)

        layout_h2 = QHBoxLayout()
        layout_h2.addWidget(self.label_1)
        layout_h2.addLayout(duration_layout)

        layout_h3 = QHBoxLayout()
        layout_h3.addWidget(self.label_2)
        layout_h3.addLayout(amplitude_layout)

        frame_1_layout = QVBoxLayout()
        frame_1_layout.addLayout(layout_h1)  # Combined layout for Runs and Fault Type
        frame_1_layout.addLayout(layout_h2)
        frame_1_layout.addLayout(layout_h3)
        frame_1_layout.addWidget(self.button_back)

        self.frame_1 = QFrame(self)
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setLayout(frame_1_layout)

        ### frame 2 design   ###############
        # Create a combo box (dropdown)
        grid_layout = QGridLayout()

        # Title
        title = QLabel("Select Joints")
        # main_layout.addWidget(title, 0, 0, 1, 2)  # Title spans two columns

        # Grid layout for joints (Two columns)
        self.joint_grid = QGridLayout()

        # Adding joints to the grid, positioning them properly
        self.joint_grid.addWidget(QCheckBox("Joint 1"), 0, 0)
        self.joint_grid.addWidget(QCheckBox("Joint 5"), 0, 1)

        self.joint_grid.addWidget(QCheckBox("Joint 2"), 1, 0)
        self.joint_grid.addWidget(QCheckBox("Joint 6"), 1, 1)

        self.joint_grid.addWidget(QCheckBox("Joint 3"), 2, 0)
        self.joint_grid.addWidget(QCheckBox("Joint 7"), 2, 1)

        self.joint_grid.addWidget(QCheckBox("Joint 4"), 3, 0)

        # Add the joint layout to the main layout
        grid_layout.addLayout(self.joint_grid, 1, 0)

        # Button to confirm selection
        # confirm_button = QPushButton("Confirm Selection")
        # confirm_button.clicked.connect(self.confirm_selection)
        # grid_layout.addWidget(confirm_button, 2, 0, 1, 2)  # Button spans two columns

        # Set the main layout for the widget
        # self.setLayout(main_layout)

        # Connect the selection change signal to a slot

        layout_v2 = QHBoxLayout()
        layout_v2.addWidget(self.label_4)
        layout_v2.addLayout(grid_layout)

        frame_2_layout = QVBoxLayout()
        frame_2_layout.addLayout(layout_h4)
        frame_2_layout.addLayout(layout_v2)
        frame_2_layout.addWidget(self.button_go,alignment=Qt.AlignRight)

        self.frame_2 = QFrame(self)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setLayout(frame_2_layout)

        # Main layout to hold all the frames
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.frame_1)
        main_layout.addWidget(self.frame_2)

        # Outer layout that combines the logos and the main content
        outer_layout = QVBoxLayout()  # Changed to avoid confusion with layout variable
        outer_layout.addWidget(self.logos)  # Ensure Logos is a valid QWidget
        outer_layout.addLayout(main_layout)

        self.setLayout(outer_layout)

    def increase_run_value(self):
        self.run_value += 1
        self.run_label.setText(str(self.run_value))

    def decrease_run_value(self):
        if self.run_value > 0:
            self.run_value -= 1
            self.run_label.setText(str(self.run_value))

    def number_of_run(self):
        return int(self.run_value)

    def update_label(self):
        # Update the label based on the selected combo box item
        selected_joint = self.combo.currentText()
        # If there's a joint label, update it here
        pass  # Implement the functionality you need here

    def checkbox_state_changed(self):
        mode = []
        if self.checkbox_noise.isChecked():
            mode.append("Noise")
        if self.checkbox_bias.isChecked():
            mode.append("Bias")
        print(f"Selected mode: {', '.join(mode)}")
        return mode

    # def checkbox_state_changed_bias(self):
    #     # Handle the state change for the Bias checkbox
    #     pass  # Implement functionality

    def confirm_selection(self):
        # Logic to handle selected joints (only joints, not modes)
        selected_joints = []
        
        # Only find checkboxes inside the joint grid (ignoring Noise, Bias)
        for row in range(self.joint_grid.rowCount()):
            for col in range(self.joint_grid.columnCount()):
                item = self.joint_grid.itemAtPosition(row, col)
                if item is not None:  # Check if the item exists
                    widget = item.widget()
                    if isinstance(widget, QCheckBox) and widget.isChecked():
                        selected_joints.append(widget.text())

        # Logging the selected joints
        rospy.logwarn(f'Selected joints: {selected_joints}')
        
        return selected_joints

    
    def duration_amplitude(self):
        try:
            return float(self.duration_min.text()), float(self.duration_max.text()), float(self.amplitude_min.text()), float(self.amplitude_max.text())
        except ValueError:
            rospy.logwarn("Invalid input for duration or amplitude.")
            return 0, 0, 0, 0  # Handle gracefully with default values

class Welding_GeneratorPage(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.logos = Logos()  # Ensure the Logos class is well-structured

        self.button_go = QPushButton("Go")
        self.button_go.setFixedSize(150, 80)

        # "Back" button
        self.button_back = QPushButton("Back")
        self.button_back.setFixedSize(150, 80)
        self.button_back.setIconSize(self.button_back.sizeHint())
        self.button_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))

        # Labels
        self.label = QLabel("1) Runs:")
        self.label_1 = QLabel("2) Fault Duration:")
        self.label_2 = QLabel("3) Fault Amplitude:")
        self.label_3 = QLabel("4) Fault Type:")
        self.label_4 = QLabel("5) Fault Location:")

        self.run_value = 0
        self.run_label = QLabel(str(self.run_value))
        self.run_label.setFixedSize(80, 80)
        self.run_label.setAlignment(Qt.AlignCenter)

        # Adding border around the run label
        self.run_label.setStyleSheet("""
            QLabel {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
            }
        """)

        self.button_up = QPushButton("▲")
        self.button_down = QPushButton("▼")

        # Set a fixed size for smaller buttons
        self.button_up.setFixedSize(50, 40)
        self.button_down.setFixedSize(50, 40)

        # Set size policy to fixed
        self.button_up.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_down.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        arrow_layout = QVBoxLayout()
        arrow_layout.setSpacing(5)  # Adjust spacing if necessary
        arrow_layout.addWidget(self.button_up, alignment=Qt.AlignLeft)
        arrow_layout.addWidget(self.button_down, alignment=Qt.AlignLeft)

        self.button_up.clicked.connect(self.increase_run_value)
        self.button_down.clicked.connect(self.decrease_run_value)

        duration_min_label = QLabel("Min:")
        duration_max_label = QLabel("Max:")

        self.duration_min = QLineEdit()
        self.duration_min.setFixedSize(100, 80)
        self.duration_min.setPlaceholderText("Min")
        self.duration_min.setText("1")
          # Set default value for duration_min
        self.duration_max = QLineEdit()
        self.duration_max.setFixedSize(100, 80)
        self.duration_max.setPlaceholderText("Max")
        self.duration_max.setText("2")  # Set default value for duration_min
        # Styling for input boxes
        self.duration_min.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        self.duration_max.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        # Creating the layout for Duration
        duration_layout = QVBoxLayout()

        # Horizontal layout for Min
        min_layout = QHBoxLayout()
        min_layout.addWidget(duration_min_label, alignment=Qt.AlignLeft)
        min_layout.addWidget(self.duration_min, alignment=Qt.AlignLeft)
        duration_layout.addLayout(min_layout)

        # Horizontal layout for Max
        max_layout = QHBoxLayout()
        max_layout.addWidget(duration_max_label, alignment=Qt.AlignLeft)
        max_layout.addWidget(self.duration_max, alignment=Qt.AlignLeft)
        duration_layout.addLayout(max_layout)

        ##############
        amplitude_min_label = QLabel("Min:")
        amplitude_max_label = QLabel("Max:")

        self.amplitude_min = QLineEdit()
        self.amplitude_min.setFixedSize(100, 80)
        self.amplitude_min.setPlaceholderText("Min")
        self.amplitude_min.setText("0.1")  # Set default value for duration_min
        
        self.amplitude_max = QLineEdit()
        self.amplitude_max.setFixedSize(100, 80)
        self.amplitude_max.setPlaceholderText("Max")
        self.amplitude_max.setText("0.5")  # Set default value for duration_min

        # Styling for input boxes
        self.amplitude_min.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        self.amplitude_max.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                border-radius: 5px;
                font-size: 32px;
                padding: 5px;
            }
        """)

        # Creating the layout for Amplitude
        amplitude_layout = QVBoxLayout()

        # Horizontal layout for Min
        amp_min_layout = QHBoxLayout()
        amp_min_layout.addWidget(amplitude_min_label, alignment=Qt.AlignLeft)
        amp_min_layout.addWidget(self.amplitude_min, alignment=Qt.AlignLeft)
        amplitude_layout.addLayout(amp_min_layout)

        # Horizontal layout for Max
        amp_max_layout = QHBoxLayout()
        amp_max_layout.addWidget(amplitude_max_label, alignment=Qt.AlignLeft)
        amp_max_layout.addWidget(self.amplitude_max, alignment=Qt.AlignLeft)
        amplitude_layout.addLayout(amp_max_layout)

        # Frames and layouts for structuring UI components
        layout_h1 = QHBoxLayout()
        layout_h1.addWidget(self.label)  # 1) Runs:
        layout_h1.addWidget(self.run_label)
        layout_h1.addLayout(arrow_layout)

        # Create a layout for the Fault Type label and its corresponding checkbox
        layout_h4 = QHBoxLayout()
        layout_h4.addWidget(self.label_3)  # 4) Fault Type:
        
        # Checkbox layout for Noise and Bias
        self.checkbox_noise = QCheckBox("Noise")
        self.checkbox_noise.setChecked(False)  # Set initial state
        self.checkbox_noise.stateChanged.connect(self.checkbox_state_changed)

        self.checkbox_bias = QCheckBox("Bias")
        self.checkbox_bias.setChecked(False)  # Set initial state
        self.checkbox_bias.stateChanged.connect(self.checkbox_state_changed)

        # self.checkbox_group = QButtonGroup(self)
        # self.checkbox_group.addButton(self.checkbox_noise)
        # self.checkbox_group.addButton(self.checkbox_bias)
        # self.checkbox_group.setExclusive(True)  # Ensure checkboxes act like radio buttons

        self.layout_v1 = QVBoxLayout()
        self.layout_v1.addWidget(self.checkbox_noise)
        self.layout_v1.addWidget(self.checkbox_bias)

        layout_h4.addLayout(self.layout_v1)

        layout_h2 = QHBoxLayout()
        layout_h2.addWidget(self.label_1)
        layout_h2.addLayout(duration_layout)

        layout_h3 = QHBoxLayout()
        layout_h3.addWidget(self.label_2)
        layout_h3.addLayout(amplitude_layout)

        frame_1_layout = QVBoxLayout()
        frame_1_layout.addLayout(layout_h1)  # Combined layout for Runs and Fault Type
        frame_1_layout.addLayout(layout_h2)
        frame_1_layout.addLayout(layout_h3)
        frame_1_layout.addWidget(self.button_back)

        self.frame_1 = QFrame(self)
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setLayout(frame_1_layout)

        ### frame 2 design   ###############
        # Create a combo box (dropdown)
        grid_layout = QGridLayout()

        # Title
        title = QLabel("Select Joints")
        # main_layout.addWidget(title, 0, 0, 1, 2)  # Title spans two columns

        # Grid layout for joints (Two columns)
        self.joint_grid = QGridLayout()

        # Adding joints to the grid, positioning them properly
        self.joint_grid.addWidget(QCheckBox("Joint 1"), 0, 0)
        self.joint_grid.addWidget(QCheckBox("Joint 5"), 0, 1)

        self.joint_grid.addWidget(QCheckBox("Joint 2"), 1, 0)
        self.joint_grid.addWidget(QCheckBox("Joint 6"), 1, 1)

        self.joint_grid.addWidget(QCheckBox("Joint 3"), 2, 0)
        self.joint_grid.addWidget(QCheckBox("Joint 7"), 2, 1)

        self.joint_grid.addWidget(QCheckBox("Joint 4"), 3, 0)

        # Add the joint layout to the main layout
        grid_layout.addLayout(self.joint_grid, 1, 0)

        # Button to confirm selection
        # confirm_button = QPushButton("Confirm Selection")
        # confirm_button.clicked.connect(self.confirm_selection)
        # grid_layout.addWidget(confirm_button, 2, 0, 1, 2)  # Button spans two columns

        # Set the main layout for the widget
        # self.setLayout(main_layout)

        # Connect the selection change signal to a slot

        layout_v2 = QHBoxLayout()
        layout_v2.addWidget(self.label_4)
        layout_v2.addLayout(grid_layout)

        frame_2_layout = QVBoxLayout()
        frame_2_layout.addLayout(layout_h4)
        frame_2_layout.addLayout(layout_v2)
        frame_2_layout.addWidget(self.button_go,alignment=Qt.AlignRight)

        self.frame_2 = QFrame(self)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setLayout(frame_2_layout)

        # Main layout to hold all the frames
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.frame_1)
        main_layout.addWidget(self.frame_2)

        # Outer layout that combines the logos and the main content
        outer_layout = QVBoxLayout()  # Changed to avoid confusion with layout variable
        outer_layout.addWidget(self.logos)  # Ensure Logos is a valid QWidget
        outer_layout.addLayout(main_layout)

        self.setLayout(outer_layout)

    def increase_run_value(self):
        self.run_value += 1
        self.run_label.setText(str(self.run_value))

    def decrease_run_value(self):
        if self.run_value > 0:
            self.run_value -= 1
            self.run_label.setText(str(self.run_value))

    def number_of_run(self):
        return int(self.run_value)

    def update_label(self):
        # Update the label based on the selected combo box item
        selected_joint = self.combo.currentText()
        # If there's a joint label, update it here
        pass  # Implement the functionality you need here

    def checkbox_state_changed(self):
        mode = []
        if self.checkbox_noise.isChecked():
            mode.append("Noise")
        if self.checkbox_bias.isChecked():
            mode.append("Bias")
        print(f"Selected mode: {', '.join(mode)}")
        return mode

    # def checkbox_state_changed_bias(self):
    #     # Handle the state change for the Bias checkbox
    #     pass  # Implement functionality

    def confirm_selection(self):
        # Logic to handle selected joints (only joints, not modes)
        selected_joints = []
        
        # Only find checkboxes inside the joint grid (ignoring Noise, Bias)
        for row in range(self.joint_grid.rowCount()):
            for col in range(self.joint_grid.columnCount()):
                item = self.joint_grid.itemAtPosition(row, col)
                if item is not None:  # Check if the item exists
                    widget = item.widget()
                    if isinstance(widget, QCheckBox) and widget.isChecked():
                        selected_joints.append(widget.text())

        # Logging the selected joints
        rospy.logwarn(f'Selected joints: {selected_joints}')
        
        return selected_joints

    
    def duration_amplitude(self):
        try:
            return float(self.duration_min.text()), float(self.duration_max.text()), float(self.amplitude_min.text()), float(self.amplitude_max.text())
        except ValueError:
            rospy.logwarn("Invalid input for duration or amplitude.")
            return 0, 0, 0, 0  # Handle gracefully with default values


        
class ProgressPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()
        self.setWindowTitle('Progress Bar Example')
        self.setGeometry(100, 100, 300, 200)

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QProgressBar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # Set range from 0 to 100
        layout.addWidget(self.logos)
        layout.addWidget(self.progress_bar)

        # Create a button to start the progress
        self.button = QPushButton('Start Progress')
        self.button_badger = QPushButton('Badger')
        self.button.clicked.connect(self.start_progress)  # Connect button click to start_progress method
        # layout.addWidget(self.button)
        layout.addWidget(self.button_badger)

        # Set the layout for the main window
        self.setLayout(layout)

    def start_progress(self,no_of_cycle):
        # Reset the progress bar
        self.progress_bar.setValue(0)

        # Simulate progress
        for i in range(101):  # Update progress from 0 to 100
            self.progress_bar.setValue(i)
            time.sleep(0.80*no_of_cycle)
            QApplication.processEvents()  # Process events to update the UI


class DrillingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # Scene generator page layout
        self.label = QLabel("Work Piece:")
        # font = QFont()
        # font.setPointSize(16)  # Set the font size to 16
        # self.label.setFont(font)
        # self.text_length = QLineEdit(self)
        # self.text_length.setPlaceholderText("Workpiece Length")
        # self.text_width = QLineEdit(self)
        # self.text_width.setPlaceholderText("Workpiece Width")

        # self.button_accept = QPushButton("Accept")
        self.button_randomize_geometry = QPushButton("Geometry")
        self.button_randomize_geometry.setFixedSize(400,80)
        # self.button_randomize_geometry.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_randomize_position = QPushButton("Position")
        self.button_randomize_position.setFixedSize(400,80)
        # self.button_randomize_position.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_next = QPushButton("Next")
        self.button_next.setIcon(QIcon('/home/apurv/Downloads/right.png'))
        self.button_next.setFixedSize(150,80)
        self.button_next.setIconSize(self.button_next.sizeHint())  # Optionally, set the icon size to match button size
        self.button_next.setLayoutDirection(Qt.RightToLeft)  # Moves the icon to the right of the text
        # self.button_next.setStyleSheet("QPushButton { padding-left: 0px; padding-right: 0px; margin-left: 0px; }")
        self.button_next.setStyleSheet("""
            QPushButton {
                padding-left: 20px;  /* Padding for the text */
                padding-right: 10px; /* Adjust this if needed */
                padding-top: 5px;    /* Top padding */
                padding-bottom: 5px; /* Bottom padding */
                qproperty-iconSize: 50px;
            }
        """)

        # Adjust icon size to fit better
        # self.button_next.setIconSize(self.button_next.sizeHint())  # Optionally, set the icon size to match button size


        self.button_back = QPushButton("Back")
        self.button_back.setFixedSize(150,80)
        self.button_back.setIconSize(self.button_back.sizeHint())  # Optionally, set the icon size to match button size
        self.button_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))


        self.button_kill = QPushButton("Reset Gazebo")
        self.button_kill.setFixedSize(400,80)
        self.button_kill.setIcon(QIcon('/home/apurv/Downloads/close.png'))
        self.button_kill.setIconSize(self.button_kill.sizeHint())  # Optionally, set the icon size to match button size

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)
        # layout.addWidget(self.text_length)
        # layout.addWidget(self.text_width)
        # layout.addWidget(self.button_accept)
        layout.addWidget(self.button_randomize_geometry)
        layout.setAlignment(self.button_randomize_geometry, Qt.AlignCenter)

        layout.addWidget(self.button_randomize_position)
        layout.setAlignment(self.button_randomize_position, Qt.AlignCenter)

        # layout.addWidget(self.button_next)
        # layout.addWidget(self.button_back)
        # layout.addWidget(self.button_kill)
        # layout.setAlignment(self.button_kill, Qt.AlignCenter)

        h1_layout = QHBoxLayout()
        h1_layout.addWidget(self.button_back)
        h1_layout.addWidget(self.button_next)
        h1_layout.setAlignment(self.button_back, Qt.AlignLeft)
        h1_layout.setAlignment(self.button_next, Qt.AlignLeft)
        layout.addLayout(h1_layout)        
        


        self.setLayout(layout)
        
class WeldingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.logos = Logos()

        # Scene generator page layout
        self.label = QLabel("Work Piece:")
        # self.text_length = QLineEdit(self)
        # self.text_length.setPlaceholderText("Workpiece Length")
        # self.text_width = QLineEdit(self)
        # self.text_width.setPlaceholderText("Workpiece Width")

        # self.button_accept = QPushButton("Accept")
        self.button_welding_randomize_geometry = QPushButton("Geometry")
        self.button_welding_randomize_geometry.setFixedSize(400,80)
        # self.button_welding_randomize_geometry.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_welding_randomize_position = QPushButton("Position")
        self.button_welding_randomize_position.setFixedSize(400,80)
        # self.button_welding_randomize_position.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_welding_next = QPushButton("Next")
        self.button_welding_next.setIcon(QIcon('/home/apurv/Downloads/right.png'))
        self.button_welding_next.setFixedSize(150,80)
        self.button_welding_next.setIconSize(self.button_welding_next.sizeHint())  # Optionally, set the icon size to match button size
        self.button_welding_next.setLayoutDirection(Qt.RightToLeft)  # Moves the icon to the right of the text
        # self.button_next.setStyleSheet("QPushButton { padding-left: 0px; padding-right: 0px; margin-left: 0px; }")
        self.button_welding_next.setStyleSheet("""
            QPushButton {
                padding-left: 20px;  /* Padding for the text */
                padding-right: 10px; /* Adjust this if needed */
                padding-top: 5px;    /* Top padding */
                padding-bottom: 5px; /* Bottom padding */
                qproperty-iconSize: 50px;
            }
        """)

        self.button_welding_back = QPushButton("Back")
        self.button_welding_back.setFixedSize(150,80)
        self.button_welding_back.setIconSize(self.button_welding_back.sizeHint())
        self.button_welding_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))

        self.button_welding_kill = QPushButton("Reset Gazebo")
        self.button_welding_kill.setFixedSize(400,80)
        self.button_welding_kill.setIcon(QIcon('/home/apurv/Downloads/close.png'))
        self.button_welding_kill.setIconSize(self.button_welding_kill.sizeHint())  # Optionally, set the icon size to match button size



        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)
        # layout.addWidget(self.text_length)
        # layout.addWidget(self.text_width)
        # layout.addWidget(self.button_accept)
        layout.addWidget(self.button_welding_randomize_geometry)
        layout.setAlignment(self.button_welding_randomize_geometry, Qt.AlignCenter)
        layout.addWidget(self.button_welding_randomize_position)
        layout.setAlignment(self.button_welding_randomize_position, Qt.AlignCenter)
        # layout.addWidget(self.button_welding_next)
        # layout.addWidget(self.button_welding_back)
        # layout.addWidget(self.button_welding_kill)
        # layout.setAlignment(self.button_welding_kill, Qt.AlignCenter)


        h1_layout = QHBoxLayout()
        h1_layout.addWidget(self.button_welding_back)
        h1_layout.addWidget(self.button_welding_next)
        h1_layout.setAlignment(self.button_welding_back, Qt.AlignLeft)
        h1_layout.setAlignment(self.button_welding_next, Qt.AlignLeft)
        layout.addLayout(h1_layout)        
        
        self.setLayout(layout)


# class DrillingRandomWorkpiecePositionPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         self.label = QLabel("Drilling Task, Please configure Workpiece position")

#         self.button_randomize = QPushButton("randomize")
#         self.button_kill = QPushButton("Reset Gazebo")
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

        self.label = QLabel("Process:")

        self.button_randomize_holes = QPushButton("Holes")
        self.button_randomize_holes.setFixedSize(400,80)
        # self.button_randomize_holes.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_randomize_hands = QPushButton("Hands")
        self.button_randomize_hands.setFixedSize(400,80)
        # self.button_randomize_hands.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_kill = QPushButton("Reset Gazebo")
        self.button_kill.setFixedSize(400,80)
        self.button_kill.setIcon(QIcon('/home/apurv/Downloads/close.png'))
        self.button_kill.setIconSize(self.button_kill.sizeHint())  # Optionally, set the icon size to match button size


        self.button_next = QPushButton("Next")
        self.button_next.setIcon(QIcon('/home/apurv/Downloads/right.png'))
        self.button_next.setFixedSize(150,80)
        self.button_next.setIconSize(self.button_next.sizeHint())  # Optionally, set the icon size to match button size
        self.button_next.setLayoutDirection(Qt.RightToLeft)  # Moves the icon to the right of the text
        # self.button_next.setStyleSheet("QPushButton { padding-left: 0px; padding-right: 0px; margin-left: 0px; }")
        self.button_next.setStyleSheet("""
            QPushButton {
                padding-left: 20px;  /* Padding for the text */
                padding-right: 10px; /* Adjust this if needed */
                padding-top: 5px;    /* Top padding */
                padding-bottom: 5px; /* Bottom padding */
                qproperty-iconSize: 50px;
            }
        """)

        self.button_back = QPushButton("Back")
        self.button_back.setFixedSize(150,80)
        self.button_back.setIconSize(self.button_back.sizeHint())
        self.button_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)
        layout.addWidget(self.button_randomize_holes)
        layout.setAlignment(self.button_randomize_holes, Qt.AlignCenter)
        layout.addWidget(self.button_randomize_hands)
        layout.setAlignment(self.button_randomize_hands, Qt.AlignCenter)
        # layout.addWidget(self.button_next)
        # layout.addWidget(self.button_back)
        layout.addWidget(self.button_kill)
        layout.setAlignment(self.button_kill, Qt.AlignCenter)


        h1_layout = QHBoxLayout()
        h1_layout.addWidget(self.button_back)
        h1_layout.addWidget(self.button_next)
        h1_layout.setAlignment(self.button_back, Qt.AlignLeft)
        h1_layout.setAlignment(self.button_next, Qt.AlignLeft)
        layout.addLayout(h1_layout)    

        self.setLayout(layout)


class SetWeldingLinePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.logos = Logos()

        self.label = QLabel("Process:")

        self.button_welding_randomize_line = QPushButton("Line")
        self.button_welding_randomize_line.setFixedSize(400,80)

        # self.button_welding_randomize_line.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_welding_randomize_hands = QPushButton("Hands")
        self.button_welding_randomize_hands.setFixedSize(400,80)

        # self.button_welding_randomize_hands.setIcon(QIcon('/home/apurv/Downloads/random.png'))

        self.button_welding_kill = QPushButton("Reset Gazebo")
        self.button_welding_kill.setFixedSize(400,80)
        self.button_welding_kill.setIcon(QIcon('/home/apurv/Downloads/close.png'))
        self.button_welding_kill.setIconSize(self.button_welding_kill.sizeHint())  # Optionally, set the icon size to match button size


        self.button_welding_next = QPushButton("Next")
        self.button_welding_next.setIcon(QIcon('/home/apurv/Downloads/right.png'))
        self.button_welding_next.setFixedSize(150,80)
        self.button_welding_next.setIconSize(self.button_welding_next.sizeHint())  # Optionally, set the icon size to match button size
        self.button_welding_next.setLayoutDirection(Qt.RightToLeft)  # Moves the icon to the right of the text
        # self.button_next.setStyleSheet("QPushButton { padding-left: 0px; padding-right: 0px; margin-left: 0px; }")
        self.button_welding_next.setStyleSheet("""
            QPushButton {
                padding-left: 20px;  /* Padding for the text */
                padding-right: 10px; /* Adjust this if needed */
                padding-top: 5px;    /* Top padding */
                padding-bottom: 5px; /* Bottom padding */
                qproperty-iconSize: 50px;
            }
        """)

        self.button_welding_back = QPushButton("Back")
        self.button_welding_back.setFixedSize(150,80)
        self.button_welding_back.setIconSize(self.button_welding_back.sizeHint())
        self.button_welding_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))

        layout = QVBoxLayout()
        layout.addWidget(self.logos)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)

        layout.addWidget(self.button_welding_randomize_line)
        layout.setAlignment(self.button_welding_randomize_line, Qt.AlignCenter)
        layout.addWidget(self.button_welding_randomize_hands)
        layout.setAlignment(self.button_welding_randomize_hands, Qt.AlignCenter)
        # layout.addWidget(self.button_welding_next)
        # layout.addWidget(self.button_welding_back)
        layout.addWidget(self.button_welding_kill)
        layout.setAlignment(self.button_welding_kill, Qt.AlignCenter)

        h1_layout = QHBoxLayout()
        h1_layout.addWidget(self.button_welding_back)
        h1_layout.addWidget(self.button_welding_next)
        h1_layout.setAlignment(self.button_welding_back, Qt.AlignLeft)
        h1_layout.setAlignment(self.button_welding_next, Qt.AlignLeft)
        layout.addLayout(h1_layout)   

        self.setLayout(layout)


class DrillingExecutionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Logos (Make sure Logos is properly defined)
        self.logos = Logos()  # Ensure the Logos class is well-structured

        # Labels
        self.label = QLabel("Execution:")
        self.label_1 = QLabel("Fault Information:")
        self.label_2 = QLabel("\n\nFault Amplitude:")
        self.label_3 = QLabel("\n\nFault Location:")
        self.label_4 = QLabel("\n\nFault Duration:")
        self.label_T = QLabel("\n\nFault Time:")

        # Set fixed height for labels to align them
        for label in [self.label, self.label_1]:
            label.setFixedHeight(40)

        # Buttons
        self.button_start = QPushButton("Start")
        self.button_start.setFixedSize(200, 100)
        self.button_start.setIconSize(self.button_start.sizeHint())
        self.button_start.setCheckable(True)
        self.button_start.setIcon(QIcon('/home/apurv/Downloads/play.png'))

        self.button_kill = QPushButton("Kill")
        self.button_kill.setFixedSize(150, 80)
        self.button_kill.setIconSize(self.button_kill.sizeHint())
        self.button_kill.setIcon(QIcon('/home/apurv/Downloads/close.png'))

        self.button_back = QPushButton("Back")
        self.button_back.setFixedSize(150, 80)
        self.button_back.setIconSize(self.button_back.sizeHint())
        self.button_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))

        self.button_fault_generator = QPushButton("Generate Fault")
        self.button_fault_generator.setFixedSize(250, 60)
        self.button_fault_injector = QPushButton("Inject Fault")
        self.button_fault_injector.setFixedSize(250, 60)
        self.button_fault_remover = QPushButton("Remove Fault")
        self.button_fault_remover.setFixedSize(250, 60)

        # Frames and layouts for structuring UI components
        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.label)
        layout_1.addWidget(self.button_start)
        layout_1.setAlignment(self.button_start, Qt.AlignCenter)

        h1_layout = QHBoxLayout()
        h1_layout.addWidget(self.button_back)
        h1_layout.addWidget(self.button_kill)
        h1_layout.setAlignment(self.button_back, Qt.AlignLeft)
        h1_layout.setAlignment(self.button_kill, Qt.AlignRight)
        layout_1.addLayout(h1_layout)

        self.frame_1 = QFrame(self)
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setLayout(layout_1)

        layout_2 = QVBoxLayout()
        self.label_5 = QLabel(self)
        self.label_5.setText('Faults:')
        self.label_5.setFixedHeight(40)  # Fixed height for alignment

        self.dropdown = QComboBox(self)
        self.dropdown.setFixedSize(250, 60)
        self.dropdown.addItem('None')
        self.dropdown.addItem('Bias')
        self.dropdown.addItem('Noise')

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 300)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Initial picture to display
        self.update_image('/home/baua/Final_TS_Gene/src/gui/resource/None.jpg')  # Set to the default image path for None

        layout_2.addWidget(self.label_5)
        layout_2.addWidget(self.dropdown, alignment=Qt.AlignCenter)
        layout_2.addWidget(self.image_label, alignment=Qt.AlignCenter)

        layout_2.addWidget(self.button_fault_injector)  # Inject Fault button
        layout_2.setAlignment(self.button_fault_injector, Qt.AlignCenter)
        # layout_2.addWidget(self.button_fault_remover)
        # layout_2.setAlignment(self.button_fault_remover, Qt.AlignCenter)

        self.frame_2 = QFrame(self)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setLayout(layout_2)

        layout_3 = QVBoxLayout()
        layout_3.addWidget(self.label_1)
        layout_3.addWidget(self.label_2)
        layout_3.addWidget(self.label_3)
        layout_3.addWidget(self.label_4)
        layout_3.addWidget(self.label_T)
        self.frame_3 = QFrame(self)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setLayout(layout_3)

        # Add vertical spacers to center labels within each frame
        for i in range(2):  # Add two spacers
            layout_3.addStretch()

        # Main layout to hold all the frames
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.frame_1)
        main_layout.addWidget(self.frame_2)
        main_layout.addWidget(self.frame_3)

        # Outer layout that combines the logos and the main content
        layout = QVBoxLayout()
        layout.addWidget(self.logos)  # Ensure Logos is a valid QWidget
        layout.addLayout(main_layout)

        self.setLayout(layout)

    def update_image(self, image_path):
        pixmap = QPixmap(image_path)  # Load image from file
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))



    
    
    
class WeldingExecutionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Logos (Make sure Logos is properly defined)
        self.logos = Logos()  # Ensure the Logos class is well-structured

        # Labels
        self.label = QLabel("Execution:")
        self.label_1 = QLabel("Fault Information:")
        self.label_2 = QLabel("\n\nFault Amplitude:")
        self.label_3 = QLabel("\n\nFault Location:")
        self.label_4 = QLabel("\n\nFault Duration:")
        self.label_T = QLabel("\n\nFault Time:")

        # Set fixed height for labels to align them
        for label in [self.label, self.label_1]:
            label.setFixedHeight(40)

        # Buttons
        self.button_welding_start = QPushButton("Start")
        self.button_welding_start.setFixedSize(200, 100)
        self.button_welding_start.setCheckable(True)
        self.button_welding_start.setIcon(QIcon('/home/apurv/Downloads/play.png'))
        self.button_welding_start.setIconSize(self.button_welding_start.sizeHint())

        self.button_welding_kill = QPushButton("Kill")
        self.button_welding_kill.setFixedSize(150, 80)
        self.button_welding_kill.setIconSize(self.button_welding_kill.sizeHint())
        self.button_welding_kill.setIcon(QIcon('/home/apurv/Downloads/close.png'))

        self.button_welding_back = QPushButton("Back")
        self.button_welding_back.setFixedSize(150, 80)
        self.button_welding_back.setIconSize(self.button_welding_back.sizeHint())
        self.button_welding_back.setIcon(QIcon('/home/apurv/Downloads/left.png'))

        self.button_welding_fault_generator = QPushButton("Generate Fault")
        self.button_welding_fault_generator.setFixedSize(250, 60)
        self.button_welding_fault_injector = QPushButton("Inject Fault")
        self.button_welding_fault_injector.setFixedSize(250, 60)
        self.button_welding_fault_remover = QPushButton("Remove Fault")
        self.button_welding_fault_remover.setFixedSize(250, 60)

        # Frames and layouts for structuring UI components
        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.label)
        layout_1.addWidget(self.button_welding_start)
        layout_1.setAlignment(self.button_welding_start, Qt.AlignCenter)

        h1_layout = QHBoxLayout()
        h1_layout.addWidget(self.button_welding_back)
        h1_layout.addWidget(self.button_welding_kill)
        h1_layout.setAlignment(self.button_welding_back, Qt.AlignLeft)
        h1_layout.setAlignment(self.button_welding_kill, Qt.AlignRight)
        layout_1.addLayout(h1_layout)

        self.frame_1 = QFrame(self)
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setLayout(layout_1)

        layout_2 = QVBoxLayout()
        self.label_5 = QLabel(self)
        self.label_5.setText('Faults:')
        self.label_5.setFixedHeight(40)  # Fixed height for alignment

        self.dropdown = QComboBox(self)
        self.dropdown.setFixedSize(250, 60)
        self.dropdown.addItem('None')
        self.dropdown.addItem('Bias')
        self.dropdown.addItem('Noise')
        # self.dropdown.currentIndexChanged.connect(self.fault_options)
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 300)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.update_image('/home/baua/Final_TS_Gene/src/gui/resource/None.jpg')  # Set to the default image path for None

        layout_2.addWidget(self.label_5)
        layout_2.addWidget(self.dropdown, alignment=Qt.AlignCenter)
        layout_2.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # layout_2.addWidget(self.button_welding_fault_generator)  # Generate Fault button
        # layout_2.setAlignment(self.button_welding_fault_generator, Qt.AlignCenter)
        layout_2.addWidget(self.button_welding_fault_injector)  # Inject Fault button
        layout_2.setAlignment(self.button_welding_fault_injector, Qt.AlignCenter)
        # layout_2.addWidget(self.button_welding_fault_remover)  # Remove Fault button
        # layout_2.setAlignment(self.button_welding_fault_remover, Qt.AlignCenter)

        self.frame_2 = QFrame(self)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setLayout(layout_2)

        layout_3 = QVBoxLayout()
        layout_3.addWidget(self.label_1)
        layout_3.addWidget(self.label_2)
        layout_3.addWidget(self.label_3)
        layout_3.addWidget(self.label_4)
        layout_3.addWidget(self.label_T)
        self.frame_3 = QFrame(self)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setLayout(layout_3)

        # Add vertical spacers to center labels within each frame
        for i in range(2):  # Add two spacers
            layout_3.addStretch()

        # Main layout to hold all the frames
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.frame_1)
        main_layout.addWidget(self.frame_2)
        main_layout.addWidget(self.frame_3)

        # Outer layout that combines the logos and the main content
        layout = QVBoxLayout()
        layout.addWidget(self.logos)  # Ensure Logos is a valid QWidget
        layout.addLayout(main_layout)

        self.setLayout(layout)

    def update_image(self, image_path):
        pixmap = QPixmap(image_path)  # Load image from file
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))


        
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
        self.task_flag = None   # 0 = welding, 1 = drilling
        self.gazebo_killed = False
        self.fault_type = None
        self.init_ui()
        self.rosbag_directory = '/home/baua/Final_TS_Gene/'
        self.csv_output_directory = '/home/baua/Final_TS_Gene/data/'

    def init_ui(self):
        self.setWindowTitle("Time Series Data Generator")
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of each page
        self.pages = {
            'main': MainPage(),
            'generator': GeneratorPage(),
            'drill_generator': Drill_GeneratorPage(),
            'welding_generator': Welding_GeneratorPage(),
            'progress': ProgressPage(),
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
        self.pages['generator'].button_welding.clicked.connect(self.go_to_welding_page_genemode)
        self.pages['generator'].button_drilling.clicked.connect(self.go_to_drilling_page_genemode)
        self.pages['drill_generator'].button_go.clicked.connect(self.go_to_progress_page)
        self.pages['drill_generator'].button_back.clicked.connect(self.go_to_generator_page)
        # self.pages['drill_generator'].button_amplitude.connect(self.go_to_set_holes_page)
        self.pages['welding_generator'].button_go.clicked.connect(self.go_to_progress_page)
        self.pages['welding_generator'].button_back.clicked.connect(self.go_to_generator_page)
        # self.pages['welding_generator'].button_next.clicked.connect(self.go_to_set_holes_page)
        # self.pages['welding_generator'].button_back.clicked.connect(self.go_to_demonstrator_page)
        self.pages['progress'].button_badger.clicked.connect(self.badger)

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
        self.pages['drilling_set_holes'].button_next.clicked.connect(self.go_to_drilling_execution_page)
        self.pages['drilling_set_holes'].button_back.clicked.connect(self.go_to_drilling_page)
        self.pages['drilling_set_holes'].button_kill.clicked.connect(self.kill_gazebo)



        self.pages['welding_set_line'].button_welding_randomize_line.clicked.connect(self.randomize_line)
        self.pages['welding_set_line'].button_welding_randomize_hands.clicked.connect(self.randomize_hands)
        self.pages['welding_set_line'].button_welding_next.clicked.connect(self.go_to_welding_execution_page)
        self.pages['welding_set_line'].button_welding_back.clicked.connect(self.go_to_welding_page)
        self.pages['welding_set_line'].button_welding_kill.clicked.connect(self.kill_gazebo)

        # Execution Page Buttons
        # self.pages['drilling_execution'].button_add_robot.clicked.connect(self.add_drilling_robot)
        self.pages['drilling_execution'].button_start.toggled.connect(self.start_drilling_execution)
        # self.pages['drilling_execution'].button_stop.clicked.connect(self.stop_drilling_execution)
        self.pages['drilling_execution'].button_back.clicked.connect(self.go_to_set_holes_page)
        self.pages['drilling_execution'].button_kill.clicked.connect(self.kill_gazebo)
        
        self.pages['drilling_execution'].dropdown.currentIndexChanged.connect(self.fault_options)
        # print('bias selected')
        # self.bias_fault_generator()
        # if self.pages['drilling_execution'].fault_options() == 'Bias':
        #     print('bias selected')
        #     self.bias_fault_generator()
        # if self.pages['drilling_execution'].fault_options() == 'Noise':
        #     self.noise_fault_generator()     
        # if self.pages['drilling_execution'].fault_options() == 'None':
        #     self.clear_fault()
        
        # self.pages['drilling_execution'].button_fault_generator.clicked.connect(self.fault_generator)
        self.pages['drilling_execution'].button_fault_injector.clicked.connect(self.fault_injector)
        
        # self.pages['welding_execution'].button_welding_add_robot.clicked.connect(self.add_welding_robot)
        self.pages['welding_execution'].button_welding_start.clicked.connect(self.start_welding_execution)
        # self.pages['welding_execution'].button_welding_stop.clicked.connect(self.stop_welding_execution)
        self.pages['welding_execution'].button_welding_back.clicked.connect(self.go_to_set_welding_line_page)
        self.pages['welding_execution'].button_welding_kill.clicked.connect(self.kill_gazebo)
        self.pages['welding_execution'].dropdown.currentIndexChanged.connect(self.fault_options)

        # self.pages['welding_execution'].button_welding_fault_generator.clicked.connect(self.fault_generator)
        self.pages['welding_execution'].button_welding_fault_injector.clicked.connect(self.fault_injector)

    def update_image_based_on_joint(self):
        if self.joint_index is not None and self.joint_index in self.image_mapping:
            image_path = self.image_mapping[self.joint_index]
            self.update_image(image_path)
        else:
            self.update_image('/home/baua/Final_TS_Gene/src/gui/resource/None.jpg')  # Default image if no valid joint_index
    def update_image(self, image_path):
        pixmap = QPixmap(image_path)  # Load image from file
        self.pages['drilling_execution'].image_label.setPixmap(pixmap.scaled(self.pages['drilling_execution'].image_label.size(), aspectRatioMode=1))
        self.pages['welding_execution'].image_label.setPixmap(pixmap.scaled(self.pages['drilling_execution'].image_label.size(), aspectRatioMode=1))
        
    def fault_options(self):
        current_widget = self.stacked_widget.currentWidget()
        class_name = type(current_widget).__name__

        if class_name == "DrillingExecutionPage":
            selected_option = self.pages['drilling_execution'].dropdown.currentText()

        elif class_name == "WeldingExecutionPage":
            selected_option = self.pages['welding_execution'].dropdown.currentText()


        if selected_option == 'None':
            self.clear_fault()  # Clear faults
        elif selected_option == 'Bias':
            self.bias_fault_generator()  # Generate fault
            self.update_image_based_on_joint()  # Update image based on joint index
        elif selected_option == 'Noise':
            self.noise_fault_generator()  # Inject noise fault
            self.update_image_based_on_joint()  # Update image based on joint index
        return selected_option

    def go_to_main_page(self):
        self.stacked_widget.setCurrentWidget(self.pages['main'])
        print("Switched to MainPage")

    def go_to_demonstrator_page(self):
        current_widget = self.stacked_widget.currentWidget()
        class_name = type(current_widget).__name__

        # Reset Gazebo when returning from DrillingPage or WeldingPage
        if class_name in ["DrillingPage", "WeldingPage"]:
            self.kill_gazebo()

        # Navigate to the demonstrator page
        self.stacked_widget.setCurrentWidget(self.pages['demonstrator'])

        # Reset the flag
        self.gazebo_killed = False


    def go_to_generator_page(self):
        self.stacked_widget.setCurrentWidget(self.pages['generator'])
        print("Switched to GeneratorPage")

    def go_to_drilling_page(self):
        self.task_flag = 1
        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, DemonstratorPage) or self.gazebo_killed:
            # Launch Gazebo only if returning from DemonstratorPage or Gazebo was killed
            self.launch_gazebo('roslaunch', 'panda_gazebo', 'start_workscene.launch')
            self.gazebo_killed = False  # Reset the flag
        self.stacked_widget.setCurrentWidget(self.pages['drilling'])


    def go_to_welding_page(self):
        self.task_flag = 0
        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, DemonstratorPage) or self.gazebo_killed:
            # Launch Gazebo only if returning from DemonstratorPage or Gazebo was killed
            self.launch_gazebo('roslaunch', 'panda_gazebo', 'start_workscene_welding.launch')
            self.gazebo_killed = False  # Reset the flag
        self.stacked_widget.setCurrentWidget(self.pages['welding'])   
        # else:
        #     print(f"This is not the MainPage, it's {class_name}.")
        

    # def go_to_drilling_random_workpiece_position_page(self):
    #     self.stacked_widget.setCurrentWidget(self.pages['drilling_random_position'])

    def go_to_set_holes_page(self):
    # Check if the current widget is the ExecutionPage
        if isinstance(self.stacked_widget.currentWidget(), DrillingExecutionPage):
            self.remove_robot()
            rospy.logwarn('removing robot')

        self.stacked_widget.setCurrentWidget(self.pages['drilling_set_holes'])


    def go_to_set_welding_line_page(self):
        # Check if the current widget is the ExecutionPage

        if isinstance(self.stacked_widget.currentWidget(), WeldingExecutionPage):
            self.remove_robot()
            rospy.logwarn('removing robot')
        self.stacked_widget.setCurrentWidget(self.pages['welding_set_line'])

    def go_to_drilling_execution_page(self):
        if self.drilling_flag:
            self.stacked_widget.setCurrentWidget(self.pages['drilling_execution'])

        if self.put_robot_in_gazebo:
            QMessageBox.critical(self, "Robot is already in the scene")
        else:

            try:
                # subprocess.Popen(['rqt_plot'])
                self.put_robot_in_gazebo = subprocess.Popen(
                    ['roslaunch', 'panda_gazebo', 'put_robot_in_world.launch', 'load_gripper:=false', 'gripper:=drill']
                )
                time.sleep(3)
                self.execution_process = subprocess.Popen(['rosrun', 'panda_gazebo', 'ee_location_drilling.py']) ##Yuliang

            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Error adding robot: {e}")
    
    def go_to_drilling_page_genemode(self): ##yuliang
        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, GeneratorPage):

            try:
                self.launch_gazebo('rosrun', 'gui', 'generator_mode.py')
                time.sleep(3)
                self.execution_process = subprocess.Popen(['rosrun', 'panda_gazebo', 'ee_location_drilling.py']) ##Yuliang
                rospy.logerr('Setup Launched Successfully')

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting Workscene: {e}")

        self.stacked_widget.setCurrentWidget(self.pages['drill_generator'])
    
    def go_to_welding_page_genemode(self): ##yuliang
        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, GeneratorPage):

            try:
                self.launch_gazebo('rosrun', 'gui', 'generator_mode_welding.py')
                time.sleep(3)
                self.execution_process = subprocess.Popen(['rosrun', 'panda_gazebo', 'ee_location_welding.py']) ##Yuliang
                rospy.logerr('Setup Launched Successfully')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting Workscene: {e}")

        self.stacked_widget.setCurrentWidget(self.pages['welding_generator'])

    def go_to_progress_page(self):

        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, Drill_GeneratorPage):
            no_of_cycles = self.pages['drill_generator'].number_of_run()
        elif isinstance(current_widget, Welding_GeneratorPage):
            no_of_cycles = self.pages['welding_generator'].number_of_run()

        # Change the page first
        self.stacked_widget.setCurrentWidget(self.pages['progress'])

        # Start the drilling process in a new thread
        generator_drilling_exe = threading.Thread(target=self.start_drilling_generator).start()
        threads.append(generator_drilling_exe)
        self.pages['progress'].start_progress(no_of_cycles)


    def start_drilling_generator(self):

        # sub.unregister()
        # pub.unregister() 

        global joint_index, fault_amplitude, fault_duration, start_time, fault_type

        run_value = self.pages['drill_generator'].number_of_run()
        dura_min, dura_max, amp_min, amp_max = self.pages['drill_generator'].duration_amplitude()
        fault_modes = self.pages['drill_generator'].checkbox_state_changed()
        joints = self.pages['drill_generator'].confirm_selection()
        rospy.logwarn(f'{joints}')
        rospy.logwarn(f'{fault_modes}')
        fault_joints = [
            "Joint 1",
            "Joint 2",
            "Joint 3",
            "Joint 4",
            "Joint 5",
            "Joint 6",
            "Joint 7",
            "Joint 8"
        ]
        self.drilling_joint_state_process = subprocess.Popen(['rosrun', 'joint_state_publisher', 'recorder'])  # First process
        time.sleep(3) 

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.drilling_rosbag_process = subprocess.Popen(['rosbag', 'record', '-O', f'/home/baua/Final_TS_Gene/record_{timestamp}.bag', 'record'])

        for i in range(run_value):

            fault_duration.data = round(random.uniform(dura_min, dura_max), 2)
            fault_amplitude.data = round(random.uniform(amp_min, amp_max), 2)
            self.fault_location = random.choice(joints)     ########changed
            rospy.logerr(f'{self.fault_location}')
            joint_index.data = fault_joints.index(self.fault_location)
            start_time.data = rospy.get_time() + round(random.uniform(10 , 30))
            fault_name = random.choice(fault_modes)

            if fault_name == 'Bias Fault':
                fault_type.data = 1
            elif fault_name == 'Noise Fault':
                fault_type.data = 2

            try:

                # Launch the processes for drilling execution
                self.fault_injector()        
                rospy.logerr('0')

                rospy.logerr('1')

                self.drilling_process = subprocess.Popen(['rosrun', 'pick_and_place', 'drilling.py'])
                rospy.logerr('2')

                rospy.logerr('3')

                rospy.logerr('4')

                rospy.logwarn("Drilling execution started")
                rospy.logerr(f'execution {i}')
                self.drilling_process.wait()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting execution: {e}")

            finally:
                self.fault_process.terminate()
                self.fault_thread.join(timeout=1)

        self.drilling_joint_state_process.terminate()
        self.drilling_rosbag_process.terminate()


    def start_welding_generator(self):

        # sub.unregister()
        # pub.unregister() 

        global joint_index, fault_amplitude, fault_duration, start_time, fault_type

        run_value = self.pages['welding_generator'].number_of_run()
        dura_min, dura_max, amp_min, amp_max = self.pages['welding_generator'].duration_amplitude()
        fault_modes = self.pages['welding_generator'].checkbox_state_changed()
        joints = self.pages['welding_generator'].confirm_selection()
        rospy.logwarn(f'{joints}')
        rospy.logwarn(f'{fault_modes}')
        fault_joints = [
            "Joint 1",
            "Joint 2",
            "Joint 3",
            "Joint 4",
            "Joint 5",
            "Joint 6",
            "Joint 7",
            "Joint 8"
        ]
        self.drilling_joint_state_process = subprocess.Popen(['rosrun', 'joint_state_publisher', 'recorder'])  # First process
        time.sleep(3) 

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.drilling_rosbag_process = subprocess.Popen(['rosbag', 'record', '-O', f'/home/baua/Final_TS_Gene/record_{timestamp}.bag', 'record'])

        for i in range(run_value):

            fault_duration.data = round(random.uniform(dura_min, dura_max), 2)
            fault_amplitude.data = round(random.uniform(amp_min, amp_max), 2)
            self.fault_location = random.choice(joints)     ########changed
            rospy.logerr(f'{self.fault_location}')
            joint_index.data = fault_joints.index(self.fault_location)
            start_time.data = rospy.get_time() + round(random.uniform(10 , 30))
            fault_name = random.choice(fault_modes)

            if fault_name == 'Bias Fault':
                fault_type.data = 1
            elif fault_name == 'Noise Fault':
                fault_type.data = 2

            try:

                # Launch the processes for drilling execution
                self.fault_injector()        
                rospy.logerr('0')

                rospy.logerr('1')

                self.drilling_process = subprocess.Popen(['rosrun', 'pick_and_place', 'welding.py'])
                rospy.logerr('2')

                rospy.logerr('3')

                rospy.logerr('4')

                rospy.logwarn("Welding execution started")
                rospy.logerr(f'execution {i}')
                self.drilling_process.wait()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting execution: {e}")

            finally:
                self.fault_process.terminate()
                self.fault_thread.join(timeout=1)

    
    def go_to_welding_execution_page(self):
        if self.welding_flag:
            self.stacked_widget.setCurrentWidget(self.pages['welding_execution'])

        if self.put_robot_in_gazebo:
            QMessageBox.critical(self, "Robot is already in the scene")
        else:

            try:
                    # subprocess.Popen(['rqt_plot'])
                self.put_robot_in_gazebo = subprocess.Popen(
                    ['roslaunch', 'panda_gazebo', 'put_robot_in_world.launch', 'load_gripper:=false', 'gripper:=welding']
                )
                time.sleep(3)
                self.execution_process = subprocess.Popen(['rosrun', 'panda_gazebo', 'ee_location_welding.py']) ##Yuliang

            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Error adding robot: {e}")

            
        
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

            # Set the flag to indicate Gazebo was explicitly killed
            self.gazebo_killed = True

            current_widget = self.stacked_widget.currentWidget()
            class_name = type(current_widget).__name__
            if class_name in ["SetHolesPage", "DrillingExecutionPage", "SetWeldingLinePage", "WeldingExecutionPage"]:
                if self.task_flag == 1:
                    self.launch_gazebo('roslaunch', 'panda_gazebo', 'start_workscene.launch')
                    if class_name == "DrillingExecutionPage":
                        self.remove_robot()
                    self.stacked_widget.setCurrentWidget(self.pages['drilling'])

                elif self.task_flag == 0:
                    self.launch_gazebo('roslaunch', 'panda_gazebo', 'start_workscene_welding.launch')
                    if class_name == "WeldingExecutionPage":
                        self.remove_robot()
                    self.stacked_widget.setCurrentWidget(self.pages['welding'])

    def randomize_geometry(self):
        self.run_command(['rosrun', 'panda_gazebo', 'modify_geometry.py'])

    def randomize_position(self):
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


    def remove_robot(self):
        try:
            rospy.wait_for_service('/gazebo/delete_model', timeout=5)
            delete_model_service = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
            delete_model_service('panda')  # Replace 'panda' with the actual name of your robot model in Gazebo
            self.put_robot_in_gazebo.terminate()  # Terminates the subprocess
            self.put_robot_in_gazebo = None
            QMessageBox.information(self, "Success", "Robot has been successfully removed from the scene.")
        except (rospy.ServiceException, rospy.ROSException) as e:
            QMessageBox.critical(self, "Error", f"Failed to remove robot: {e}")


    def start_drilling_execution(self, checked):
        if checked:
            self.pages['drilling_execution'].button_start.setText("Stop")
            self.pages['drilling_execution'].button_start.setIcon(QIcon('/home/apurv/Downloads/stop.png'))

            try:
                # Launch the processes for drilling execution
                self.drilling_joint_state_process = subprocess.Popen(['rosrun', 'joint_state_publisher', 'recorder'])  # First process
                time.sleep(3)
                self.drilling_process = subprocess.Popen(['rosrun', 'pick_and_place', 'drilling.py'])
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                self.drilling_rosbag_process = subprocess.Popen(['rosbag', 'record', '-O', f'/home/baua/Final_TS_Gene/record_{timestamp}.bag', 'record'])
               
                rospy.logwarn("Drilling execution started")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting execution: {e}")

        else:
            # Terminate all processes for drilling
            self.terminate_process(self.drilling_joint_state_process)
            self.terminate_process(self.drilling_process)
            self.terminate_process(self.drilling_rosbag_process)
            # bag_file_path = self.find_newest_bag_file()
            # csv_file_path = bag_file_path.replace('rosbag', 'roscsv').replace('.bag', '.csv')
            # self.convert_bag_to_csv(bag_file_path, csv_file_path, '/record')
            # time.sleep(5)
            # self.drilling_plot = subprocess.Popen(['rosrun', 'panda_gazebo', 'plot.py'])
            rospy.logwarn("Drilling execution terminated")

            # Reset button text and icon
            self.pages['drilling_execution'].button_start.setText("Start")
            self.pages['drilling_execution'].button_start.setIcon(QIcon('/home/apurv/Downloads/play.png'))

    def convert_newest_bag_to_csv(self):
        """Converts the newest bag file to CSV."""
        try:
            # Find the newest bag file
            newest_bag_file_path = self.find_newest_bag_file()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            csv_file_path = os.path.join(self.csv_output_directory, f'record_{timestamp}.csv')

            # Convert the bag file to CSV
            self.convert_bag_to_csv(newest_bag_file_path, csv_file_path, '/record')

        except Exception as e:
            rospy.logerr(f"Error converting the newest bag file to CSV: {e}")
    def convert_bag_to_csv(self, bag_file_path, csv_file_path, topic_name):
        
        try:
            # Use subprocess to run rostopic echo command to extract the data from the bag to CSV
            with open(csv_file_path, 'w') as csv_file:
                self.execution_process = subprocess.Popen(
                    ['rostopic', 'echo', '-b', bag_file_path, '-p', topic_name],
                    stdout=csv_file
                )

            rospy.logwarn(f"Converted rosbag {bag_file_path} to CSV {csv_file_path}")

        except Exception as e:
            rospy.logerr(f"Error converting bag to CSV: {e}")

    def find_newest_bag_file(self):
 
        bag_files = [f for f in os.listdir(self.rosbag_directory) if f.endswith('.bag')]
        if not bag_files:
            raise FileNotFoundError("No .bag files found in the directory.")

        # Sort the files by modification time (newest first)
        bag_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.rosbag_directory, f)), reverse=True)
        
        # Return the path to the newest bag file
        newest_bag_file = os.path.join(self.rosbag_directory, bag_files[0])
        # print(f"Newest bag file: {newest_bag_file}")
        return newest_bag_file
    
    def start_welding_execution(self, checked):
        if checked:
            self.pages['welding_execution'].button_welding_start.setText("Stop")
            self.pages['welding_execution'].button_welding_start.setIcon(QIcon('/home/apurv/Downloads/stop.png'))

            try:
                # Launch the processes for welding execution
                self.welding_joint_state_process = subprocess.Popen(['rosrun', 'joint_state_publisher', 'recorder'])  # First process
                # time.sleep(3)
                self.welding_process = subprocess.Popen(['rosrun', 'pick_and_place', 'welding.py'])  # Second process
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                self.welding_rosbag_process = subprocess.Popen(['rosbag', 'record', 'record'])  # Third process

                rospy.logwarn("Welding execution started")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting execution: {e}")

        else:
            # Terminate all processes for welding
            self.terminate_process(self.welding_joint_state_process)
            self.terminate_process(self.welding_process)
            self.terminate_process(self.welding_rosbag_process)
            # bag_file_path = self.find_newest_bag_file()
            # csv_file_path = bag_file_path.replace('rosbag', 'roscsv').replace('.bag', '.csv')
            # self.convert_bag_to_csv(bag_file_path, csv_file_path, '/record')
            # time.sleep(5)
            # self.welding_plot = subprocess.Popen(['rosrun', 'panda_gazebo', 'plot.py'])
            rospy.logwarn("Welding execution terminated")

            # Reset button text and icon
            self.pages['welding_execution'].button_welding_start.setText("Start")
            self.pages['welding_execution'].button_welding_start.setIcon(QIcon('/home/apurv/Downloads/play.png'))


    def terminate_process(self, process):
        """Terminate a subprocess if it is running."""
        if process:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                rospy.logwarn("Process did not terminate gracefully, killing it forcefully")
                process.kill()
            finally:
                process = None

    # def stop_drilling_execution(self):
    #     if self.execution_process:
    #         self.execution_process.terminate()
    #         try:
    #             self.execution_process.wait(timeout=5)
    #         except subprocess.TimeoutExpired:
    #             rospy.logwarn("Execution did not terminate gracefully, killing it forcefully")
    #             self.execution_process.kill()
    #         finally:
    #             self.execution_process = None
    #         rospy.logwarn("Drilling execution terminated")

    #     else:
    #         rospy.logwarn("No execution process running.")
            

    # def stop_welding_execution(self):
    #     # Stop execution logic here
    #     if self.execution_process:
    #         # Attempt to terminate the process gracefully
    #         self.execution_process.terminate()
    #         try:
    #             self.execution_process.wait(timeout=5)  # Wait for up to 10 seconds for the process to terminate
    #         except subprocess.TimeoutExpired:
    #             print("Execution did not terminate gracefully, killing it forcefully.")
    #             self.execution_process.kill()  # Force kill if it doesn't terminate
    #         finally:
    #             # Ensure the process is cleaned up
    #             self.execution_process = None

    #         rospy.logwarn("Execution process terminated.")
    #     else:
    #         rospy.logwarn("No execution process running.")

    def clear_fault(self):
        # Clear fault values
        self.fault_duration = 0
        self.fault_amplitude = 0
        self.joint_index = 0  # Reset joint index
        self.start_time = 0
        current_widget = self.stacked_widget.currentWidget()
        class_name = type(current_widget).__name__

        if class_name == "DrillingExecutionPage":
            # self.pages['drilling_execution'].label_1.setText(f"Fault Information:")
            self.pages['drilling_execution'].label_2.setText(f"\n\nFault Amplitude:")
            self.pages['drilling_execution'].label_3.setText(f"\n\nFault Location:")
            self.pages['drilling_execution'].label_4.setText(f"\n\nFault Duration:")
            self.pages['drilling_execution'].label_T.setText(f"\n\nFault Time:")


        elif class_name == "WeldingExecutionPage":
            # self.pages['welding_execution'].label_1.setText(f"Fault Information:")
            self.pages['welding_execution'].label_2.setText(f"\n\nFault Amplitude:")
            self.pages['welding_execution'].label_3.setText(f"\n\nFault Location:")
            self.pages['welding_execution'].label_4.setText(f"\n\nFault Duration:")
            self.pages['welding_execution'].label_T.setText(f"\n\nFault Time:")
        self.update_image('/home/baua/Final_TS_Gene/src/gui/resource/None.jpg')  # Reset image       

    def fault_generator(self):

        self.image_mapping = {
            0: '/home/baua/Final_TS_Gene/src/gui/resource/joint1.jpg',
            1: '/home/baua/Final_TS_Gene/src/gui/resource/joint2.jpg',
            2: '/home/baua/Final_TS_Gene/src/gui/resource/joint3.jpg',
            3: '/home/baua/Final_TS_Gene/src/gui/resource/joint4.jpg',
            4: '/home/baua/Final_TS_Gene/src/gui/resource/joint5.jpg',
            5: '/home/baua/Final_TS_Gene/src/gui/resource/joint6.jpg',
            6: '/home/baua/Final_TS_Gene/src/gui/resource/joint7.jpg'
                    # Add more mappings as necessary
            # Add more mappings as necessary
        }
        
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
                self.pages['drilling_execution'].label_1.setText(f"Fault Information:")
                self.pages['drilling_execution'].label_2.setText(f"\n\nFault Amplitude: {self.fault_amplitude}")
                self.pages['drilling_execution'].label_3.setText(f"\n\nFault Location: {self.fault_location}")
                self.pages['drilling_execution'].label_4.setText(f"\n\nFault Duration: {self.fault_duration}")
                self.pages['drilling_execution'].label_T.setText(f"\n\nFault Time: {self.start_time}")
            elif class_name == "WeldingExecutionPage":
                self.pages['welding_execution'].label_1.setText(f"Fault Information:")
                self.pages['welding_execution'].label_2.setText(f"\n\nFault Amplitude: {self.fault_amplitude}")
                self.pages['welding_execution'].label_3.setText(f"\n\nFault Location: {self.fault_location}")
                self.pages['welding_execution'].label_4.setText(f"\n\nFault Duration: {self.fault_duration}")
                self.pages['welding_execution'].label_T.setText(f"\n\nFault Time: {self.start_time}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating fault: {e}")

        rospy.logwarn('Fault created successfully')

        return self.joint_index, self.fault_amplitude, self.fault_duration, self.start_time
    
    def bias_fault_generator(self):

        rospy.set_param('/use_sim_time', True) 

        self.image_mapping = {
        0: '/home/baua/Final_TS_Gene/src/gui/resource/joint1.jpg',
        1: '/home/baua/Final_TS_Gene/src/gui/resource/joint2.jpg',
        2: '/home/baua/Final_TS_Gene/src/gui/resource/joint3.jpg',
        3: '/home/baua/Final_TS_Gene/src/gui/resource/joint4.jpg',
        4: '/home/baua/Final_TS_Gene/src/gui/resource/joint5.jpg',
        5: '/home/baua/Final_TS_Gene/src/gui/resource/joint6.jpg',
        6: '/home/baua/Final_TS_Gene/src/gui/resource/joint7.jpg'
                    # Add more mappings as necessary
        }
        global joint_index, fault_amplitude, fault_duration, start_time, fault_type

        # Your existing bias fault generation code...
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
            self.start_time = rospy.get_time() + round(random.uniform(10, 30))

            fault_duration.data = self.fault_duration
            fault_amplitude .data= self.fault_amplitude
            joint_index.data = self.joint_index
            start_time.data = self.start_time
            fault_type.data = 1

            current_widget = self.stacked_widget.currentWidget()
            class_name = type(current_widget).__name__

            if class_name == "DrillingExecutionPage":
                # self.pages['drilling_execution'].label_1.setText(f"Fault Information:")
                self.pages['drilling_execution'].label_2.setText(f"\n\nFault Amplitude: {self.fault_amplitude}")
                self.pages['drilling_execution'].label_3.setText(f"\n\nFault Location: {self.fault_location}")
                self.pages['drilling_execution'].label_4.setText(f"\n\nFault Duration: {self.fault_duration}")
                self.pages['drilling_execution'].label_T.setText(f"\n\nFault Time: {self.start_time}")
            elif class_name == "WeldingExecutionPage":
                # self.pages['welding_execution'].label_1.setText(f"Fault Information:")
                self.pages['welding_execution'].label_2.setText(f"\n\nFault Amplitude: {self.fault_amplitude}")
                self.pages['welding_execution'].label_3.setText(f"\n\nFault Location: {self.fault_location}")
                self.pages['welding_execution'].label_4.setText(f"\n\nFault Duration: {self.fault_duration}")
                self.pages['welding_execution'].label_T.setText(f"\n\nFault Time: {self.start_time}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating fault: {e}")

        rospy.logwarn('Fault created successfully')

        return self.joint_index, self.fault_amplitude, self.fault_duration, self.start_time
    
    def noise_fault_generator(self):

        rospy.set_param('/use_sim_time', True) 

        self.image_mapping = {
        0: '/home/baua/Final_TS_Gene/src/gui/resource/joint1.jpg',
        1: '/home/baua/Final_TS_Gene/src/gui/resource/joint2.jpg',
        2: '/home/baua/Final_TS_Gene/src/gui/resource/joint3.jpg',
        3: '/home/baua/Final_TS_Gene/src/gui/resource/joint4.jpg',
        4: '/home/baua/Final_TS_Gene/src/gui/resource/joint5.jpg',
        5: '/home/baua/Final_TS_Gene/src/gui/resource/joint6.jpg',
        6: '/home/baua/Final_TS_Gene/src/gui/resource/joint7.jpg'
                    # Add more mappings as necessary
        }

        global joint_index, fault_amplitude, fault_duration, start_time, fault_type
        try:
            with open("/home/baua/Final_TS_Gene/noise_config.yaml", 'r') as file:
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
            self.start_time = rospy.get_time() + round(random.uniform(10 , 30))

            fault_duration.data = self.fault_duration
            fault_amplitude .data= self.fault_amplitude
            joint_index.data = self.joint_index
            start_time.data = self.start_time
            fault_type.data = 2


            current_widget = self.stacked_widget.currentWidget()
            class_name = type(current_widget).__name__

            if class_name == "DrillingExecutionPage":
                # self.pages['drilling_execution'].label_1.setText(f"Fault Information:")
                self.pages['drilling_execution'].label_2.setText(f"\n\nFault Amplitude: {self.fault_amplitude}")
                self.pages['drilling_execution'].label_3.setText(f"\n\nFault Location: {self.fault_location}")
                self.pages['drilling_execution'].label_4.setText(f"\n\nFault Duration: {self.fault_duration}")
                self.pages['drilling_execution'].label_T.setText(f"\n\nFault Time: {self.start_time}")
            elif class_name == "WeldingExecutionPage":
                # self.pages['welding_execution'].label_1.setText(f"Fault Information:")
                self.pages['welding_execution'].label_2.setText(f"\n\nFault Amplitude: {self.fault_amplitude}")
                self.pages['welding_execution'].label_3.setText(f"\n\nFault Location: {self.fault_location}")
                self.pages['welding_execution'].label_4.setText(f"\n\nFault Duration: {self.fault_duration}")
                self.pages['welding_execution'].label_T.setText(f"\n\nFault Time: {self.start_time}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating fault: {e}")

        rospy.logwarn('Fault created successfully')

        return self.joint_index, self.fault_amplitude, self.fault_duration, self.start_time
    
    def fault_injector(self):
        global pub_state
        sub.unregister()  # Unregister subscribers/publishers if needed
        pub.unregister()  # Ensure `pub` is defined globally or passed properly
        pub_fault.unregister()
        pub_state = False
        rospy.logwarn('Launching fault injector node')

        # Start the fault injector node directly with subprocess.Popen()
        def run_fault_injector():
            try:
                self.fault_process = subprocess.Popen(['rosrun', 'joint_state_publisher', 'fault_injector'])
                self.fault_process.wait()  # Wait for the process to complete
            except Exception as e:
                rospy.logerr(f"Fault injector failed: {e}")

        # Start the fault injector in a separate thread
        self.fault_thread = threading.Thread(target=run_fault_injector)
        self.fault_thread.start()
        threads.append(self.fault_thread)

        # Wait until all necessary subscribers are connected
        while pub_index.get_num_connections() == 0 or pub_amplitude.get_num_connections() == 0 or pub_duration.get_num_connections() == 0 or pub_time.get_num_connections() == 0:
            rospy.loginfo("Waiting for subscribers...")
            rospy.sleep(0.01)

        # Publish the fault data 20 times with a small delay
        for i in range(20):
            pub_index.publish(joint_index)  # Publish to ROS topics
            pub_amplitude.publish(fault_amplitude)  # Publish to ROS topics
            pub_duration.publish(fault_duration)  # Publish to ROS topics
            pub_time.publish(start_time)  # Publish to ROS topics
            pub_type.publish(fault_type)  # Publish the fault type (Bias or Noise)
            rospy.sleep(0.1)

        rospy.logwarn('Fault inserted successfully')
        return pub_state

    def badger(self):
        rospy.logerr('badger function here')


    def remove_fault():

        pass


    def closeEvent(self, event):
        # Call the cleanup function when the window is closed
        close_event_handler()
        event.accept()



# ROS-related code for publisher and subscriber
def joint_callback(jointstate: JointState):
    
    pub.publish(jointstate)
    fault_flag = Int32()
    fault_flag.data = 0  # Initialize it with a value
    pub_fault.publish()
    # if pub_state:
        # pub.publish(jointstate)

            # pub2.publish(data)  # Publish to ROS topics
    # pub_index.publish(joint_index)  # Publish to ROS topics
    # pub_amplitude.publish(fault_amplitude)  # Publish to ROS topics
    # pub_duration.publish(fault_duration)  # Publish to ROS topics
    # pub_time.publish(start_time)  # Publish to ROS topics


def ros_spin():
    rospy.spin()

def close_event_handler():
    # Shut down ROS gracefully
    rospy.signal_shutdown("Shutting down ROS...")
    print("ROS shutdown initiated...")

    # Join the ROS thread
    for thread in threads:
        if thread is not None and thread.is_alive():            
            thread.join(timeout=1)  # Wait for the ROS thread to finish
            print("ROS thread joined.")

    # Terminate Gazebo, RViz, and other running processes gracefully
    processes = ['gazebo', 'gzserver', 'gzclient', 'rviz']

    for process in processes:
        try:
            subprocess.call(['pkill', '-f', process])
            print(f"{process} terminated.")
        except Exception as e:
            print(f"Error terminating {process}: {e}")

    # Cleanup ROS nodes
    try:
        subprocess.call('echo y | rosnode cleanup', shell=True)
        print("ROS nodes cleaned up.")
    except Exception as e:
        print(f"Error during ROS node cleanup: {e}")

    print("Shutdown complete.")


if __name__ == "__main__":

    threads = []
    subprocess.call('echo y | rosnode cleanup', shell=True)    
    rospy.init_node("Run")
    rospy.set_param('/use_sim_time', True) 
    # Publisher for /faulty_joint_states
    pub = rospy.Publisher('/faulty_joint_states', JointState, queue_size=100)
    pub_state = True
    # pub2 = rospy.Publisher('fault_data', my_message, queue_size=100)
    pub_index = rospy.Publisher('fault_index', Int32, queue_size=50)
    pub_duration = rospy.Publisher('fault_duration', Float32, queue_size=50)
    pub_amplitude = rospy.Publisher('fault_amplitude', Float32, queue_size=50)
    pub_time = rospy.Publisher('fault_time', Float32, queue_size=50)
    pub_fault = rospy.Publisher('fault_flag', Int32, queue_size=100)
    pub_type = rospy.Publisher('fault_type', Int32, queue_size=100)
    # Subscriber for /joint_states
    sub = rospy.Subscriber('/joint_states', JointState, callback=joint_callback)

    # Start ROS spin in a separate thread
    ros_thread = threading.Thread(target=ros_spin)
    ros_thread.start()
    threads.append(ros_thread)
    # GUI-related code
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('/home/apurv/Downloads/icon.png'))
    win = Gui()
    win.closeEvent = lambda event: close_event_handler()  # Override close event
    win.show()
    sys.exit(app.exec_())