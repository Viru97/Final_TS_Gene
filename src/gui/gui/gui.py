#!/usr/bin/env python3
"""GUI for Time Series Data Generator — migrated from ROS 1 (rospy) to ROS 2 (rclpy)."""

import os
import sys
import csv
import time
import random
import shutil
import datetime
import threading
import subprocess

import yaml

# ---------- ROS 2 ----------
import rclpy
from rclpy.qos import (
    QoSProfile, DurabilityPolicy, ReliabilityPolicy, HistoryPolicy,
)
from rclpy.executors import MultiThreadedExecutor
from rclpy.parameter import Parameter

# ---------- Qt ----------
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QWidget, QStackedWidget, QLineEdit, QMessageBox, QFrame, QComboBox,
    QCheckBox, QSizePolicy, QProgressBar, QGridLayout,
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal

# ---------- Messages / services ----------
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32, Float32, String
from gazebo_msgs.srv import DeleteEntity          # ROS 2 replaces DeleteModel
from rcl_interfaces.msg import Log                # ROS 2 replaces rosgraph_msgs/Log


# ============================================================
# Constants
# ============================================================
BASE  = '/home/baua/Final_TS_Gene'
LOGOS = f'{BASE}/src/gui/logos'
RES   = f'{BASE}/src/gui/resource'
ROSBAG_DIR = f'{BASE}/data/rosbag'
ROSCSV_DIR = f'{BASE}/data/roscsv'

ICON = {
    'left':   f'{LOGOS}/left.png',
    'right':  f'{LOGOS}/right.png',
    'close':  f'{LOGOS}/close.png',
    'play':   f'{LOGOS}/play.png',
    'stop':   f'{LOGOS}/stop.png',
    'badger': f'{LOGOS}/badger.jpg',
    'icon':   f'{LOGOS}/icon.png',
}
NONE_IMG = f'{RES}/None.jpg'
JOINT_IMG_MAP = {i: f'{RES}/joint{i+1}.jpg' for i in range(7)}
FAULT_JOINTS  = [f"Joint {i}" for i in range(1, 9)]

LE_STYLE = """
    QLineEdit { border: 2px solid black; border-radius: 5px;
                font-size: 32px; padding: 5px; }
"""
NEXT_STYLE = """
    QPushButton { padding-left: 20px; padding-right: 10px;
                  padding-top: 5px; padding-bottom: 5px;
                  qproperty-iconSize: 50px; }
"""
LABEL_BOLD = "font-weight: bold; font-size: 14pt;"

# "Latched" behavior in ROS 2 = TRANSIENT_LOCAL durability
LATCHED_QOS = QoSProfile(
    depth=1,
    history=HistoryPolicy.KEEP_LAST,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    reliability=ReliabilityPolicy.RELIABLE,
)

# Shared state
joint_index     = Int32()
fault_amplitude = Float32()
fault_duration  = Float32()
start_time      = Float32()
fault_type      = Int32()
task_type       = None
count           = None
threads         = []

# Populated in __main__
ros_node      = None
executor      = None
pub           = None
pub_index     = None
pub_duration  = None
pub_amplitude = None
pub_time      = None
pub_fault     = None
pub_type      = None
sub_joint     = None
pub_state     = True


# ============================================================
# ROS 2 helpers
# ============================================================
def get_sim_time_sec():
    """ROS 2 equivalent of rospy.get_time()."""
    if ros_node is None:
        return time.time()
    return ros_node.get_clock().now().nanoseconds * 1e-9


def _log(level, msg):
    if ros_node is None:
        print(f"[{level}] {msg}"); return
    lg = ros_node.get_logger()
    {'info': lg.info, 'warn': lg.warning, 'error': lg.error}[level](str(msg))

def loginfo(m): _log('info', m)
def logwarn(m): _log('warn', m)
def logerr(m):  _log('error', m)


def wait_for_message(msg_type, topic, timeout_sec=None, qos=10):
    """Thread-safe replacement for rospy.wait_for_message()."""
    holder = {'msg': None}
    ev = threading.Event()

    def cb(msg):
        if not ev.is_set():
            holder['msg'] = msg
            ev.set()

    s = ros_node.create_subscription(msg_type, topic, cb, qos)
    try:
        ev.wait(timeout=timeout_sec)
        return holder['msg']
    finally:
        ros_node.destroy_subscription(s)


def ros2_launch(pkg, launch_file, *args):
    return ['ros2', 'launch', pkg, launch_file, *args]

def ros2_run(pkg, executable, *args):
    return ['ros2', 'run', pkg, executable, *args]


# ============================================================
# Bag → CSV (rosbag2_py based, emulates `rostopic echo -p`)
# ============================================================
def _flatten(obj, prefix=''):
    """Flatten a message (as dict) into {field.path: value}."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            out.update(_flatten(v, key))
        return out
    if isinstance(obj, (list, tuple)):
        out = {}
        for i, v in enumerate(obj):
            out.update(_flatten(v, f"{prefix}{i}"))
        return out
    return {prefix: obj}


def convert_bag_to_csv(bag_dir, csv_file_path, topic_name):
    """ROS 2 bag (directory) → CSV. Replaces `rostopic echo -b ... -p ...`."""
    try:
        from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
        from rclpy.serialization import deserialize_message
        from rosidl_runtime_py.utilities import get_message
        from rosidl_runtime_py import message_to_ordereddict

        reader = SequentialReader()
        reader.open(
            StorageOptions(uri=bag_dir, storage_id='sqlite3'),
            ConverterOptions(input_serialization_format='cdr',
                             output_serialization_format='cdr'),
        )
        types = {t.name: t.type for t in reader.get_all_topics_and_types()}
        if topic_name not in types:
            raise ValueError(f"Topic {topic_name} not in bag.")
        MsgT = get_message(types[topic_name])

        rows, keys = [], None
        while reader.has_next():
            topic, data, t_ns = reader.read_next()
            if topic != topic_name:
                continue
            msg = deserialize_message(data, MsgT)
            flat = _flatten(message_to_ordereddict(msg))
            flat['%time'] = t_ns
            if keys is None:
                keys = ['%time'] + [k for k in flat if k != '%time']
            rows.append(flat)

        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        with open(csv_file_path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=keys or ['%time'])
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, '') for k in (keys or [])})
        logwarn(f"Converted bag {bag_dir} → {csv_file_path}")
    except Exception as e:
        logerr(f"Error converting bag to CSV: {e}")


# ============================================================
# UI helpers
# ============================================================
def make_button(text, size=(400, 80), icon=None):
    btn = QPushButton(text); btn.setFixedSize(*size)
    if icon:
        btn.setIcon(QIcon(icon)); btn.setIconSize(btn.sizeHint())
    return btn

def back_btn(): return make_button("Back", (150, 80), ICON['left'])
def kill_btn(): return make_button("Reset", (400, 80), ICON['close'])

def next_btn():
    b = make_button("Next", (150, 80), ICON['right'])
    b.setLayoutDirection(Qt.RightToLeft); b.setStyleSheet(NEXT_STYLE)
    return b

def make_line_edit(default="", size=(100, 80), placeholder=""):
    le = QLineEdit(str(default)); le.setFixedSize(*size)
    le.setAlignment(Qt.AlignCenter); le.setStyleSheet(LE_STYLE)
    if placeholder: le.setPlaceholderText(placeholder)
    return le

def make_label(text, bold=False):
    lbl = QLabel(text)
    if bold: lbl.setStyleSheet(LABEL_BOLD)
    return lbl

def bottom_nav(left=None, right=None):
    h = QHBoxLayout()
    if left:  h.addWidget(left);  h.setAlignment(left,  Qt.AlignLeft)
    if right: h.addWidget(right); h.setAlignment(right, Qt.AlignRight if left else Qt.AlignLeft)
    return h


# ============================================================
# Pages
# ============================================================
class Logos(QWidget):
    FILES = ('IAS_LOGO.png', 'Baua_logo.png', 'IESE_logo.png')
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        for fname in self.FILES:
            lbl = QLabel(self)
            pm = QPixmap(f'{LOGOS}/{fname}').scaled(
                450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl.setPixmap(pm); layout.addWidget(lbl)


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.logos = Logos()
        self.label = make_label("Modes:", bold=True)
        self.button_generator    = make_button("Generator")
        self.button_demonstrator = make_button("Demonstrator")
        lay = QVBoxLayout(self); lay.addWidget(self.logos)
        for w in (self.label, self.button_generator, self.button_demonstrator):
            lay.addWidget(w); lay.setAlignment(w, Qt.AlignCenter)


class TasksPage(QWidget):
    def __init__(self):
        super().__init__()
        self.logos = Logos()
        self.label = make_label("Tasks:", bold=True)
        self.button_welding  = make_button("Welding")
        self.button_drilling = make_button("Drilling")
        self.button_back     = back_btn()
        lay = QVBoxLayout(self); lay.addWidget(self.logos)
        lay.addWidget(self.label); lay.setAlignment(self.label, Qt.AlignCenter)
        for b in (self.button_welding, self.button_drilling):
            lay.addWidget(b); lay.setAlignment(b, Qt.AlignCenter)
        lay.addLayout(bottom_nav(left=self.button_back))


class TaskGeneratorPage(QWidget):
    """Unified Drilling/Welding generator setup page."""
    def __init__(self):
        super().__init__()
        self.logos = Logos(); self.run_value = 100
        self.button_go, self.button_back = make_button("Go", (150, 80)), back_btn()

        labels = [make_label(t) for t in (
            "1) Runs:", "2) Fault Duration:", "3) Fault Amplitude:",
            "4) Fault Type:", "5) Fault Location:")]
        self.label, self.label_1, self.label_2, self.label_3, self.label_4 = labels

        self.run_label = make_line_edit(self.run_value, (100, 80))
        self.run_label.editingFinished.connect(self.validate_run_value)
        self.button_up, self.button_down = QPushButton("▲"), QPushButton("▼")
        for b in (self.button_up, self.button_down):
            b.setFixedSize(50, 40); b.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_up.clicked.connect(self.increase_run_value)
        self.button_down.clicked.connect(self.decrease_run_value)

        arrow = QVBoxLayout(); arrow.setSpacing(5)
        arrow.addWidget(self.button_up,   alignment=Qt.AlignLeft)
        arrow.addWidget(self.button_down, alignment=Qt.AlignLeft)

        self.duration_min  = make_line_edit("1",   placeholder="Min")
        self.duration_max  = make_line_edit("2",   placeholder="Max")
        self.amplitude_min = make_line_edit("0.1", placeholder="Min")
        self.amplitude_max = make_line_edit("0.5", placeholder="Max")

        self.checkbox_noise = QCheckBox("Noise"); self.checkbox_noise.setChecked(True)
        self.checkbox_bias  = QCheckBox("Bias");  self.checkbox_bias.setChecked(True)
        for cb in (self.checkbox_noise, self.checkbox_bias):
            cb.stateChanged.connect(self.checkbox_state_changed)

        self.joint_grid = QGridLayout()
        positions = [(0,0),(1,0),(2,0),(3,0),(0,1),(1,1),(2,1)]
        for idx, (r, c) in enumerate(positions, start=1):
            cb = QCheckBox(f"Joint {idx}"); cb.setChecked(True)
            self.joint_grid.addWidget(cb, r, c)

        row_runs = QHBoxLayout()
        row_runs.addWidget(self.label); row_runs.addWidget(self.run_label); row_runs.addLayout(arrow)
        ftype = QVBoxLayout(); ftype.addWidget(self.checkbox_noise); ftype.addWidget(self.checkbox_bias)
        row_ftype = QHBoxLayout(); row_ftype.addWidget(self.label_3); row_ftype.addLayout(ftype)
        row_dur = QHBoxLayout(); row_dur.addWidget(self.label_1)
        row_dur.addLayout(self._min_max(self.duration_min, self.duration_max))
        row_amp = QHBoxLayout(); row_amp.addWidget(self.label_2)
        row_amp.addLayout(self._min_max(self.amplitude_min, self.amplitude_max))

        frame1 = QFrame(self); frame1.setFrameShape(QFrame.StyledPanel); frame1.setFixedWidth(800)
        f1 = QVBoxLayout(frame1)
        for lay in (row_runs, row_dur, row_amp): f1.addLayout(lay)
        f1.addWidget(self.button_back)

        grid_wrap = QGridLayout(); grid_wrap.addLayout(self.joint_grid, 1, 0)
        row_loc = QHBoxLayout(); row_loc.addWidget(self.label_4); row_loc.addLayout(grid_wrap)

        frame2 = QFrame(self); frame2.setFrameShape(QFrame.StyledPanel)
        f2 = QVBoxLayout(frame2); f2.addLayout(row_ftype); f2.addLayout(row_loc)
        f2.addWidget(self.button_go, alignment=Qt.AlignRight)

        h = QHBoxLayout(); h.addWidget(frame1); h.addWidget(frame2)
        outer = QVBoxLayout(self); outer.addWidget(self.logos); outer.addLayout(h)

    @staticmethod
    def _min_max(min_e, max_e):
        lay = QVBoxLayout()
        for t, e in (("Min:", min_e), ("Max:", max_e)):
            row = QHBoxLayout()
            row.addWidget(QLabel(t), alignment=Qt.AlignLeft)
            row.addWidget(e,         alignment=Qt.AlignLeft)
            lay.addLayout(row)
        return lay

    def increase_run_value(self):
        self.run_value = min(1000, self.run_value + 1); self.run_label.setText(str(self.run_value))
    def decrease_run_value(self):
        self.run_value = max(1, self.run_value - 1); self.run_label.setText(str(self.run_value))
    def validate_run_value(self):
        try:    self.run_value = max(1, min(1000, int(self.run_label.text())))
        except: self.run_value = 100
        self.run_label.setText(str(self.run_value))
    def number_of_run(self): return int(self.run_value)

    def checkbox_state_changed(self):
        mode = []
        if self.checkbox_noise.isChecked(): mode.append("Noise")
        if self.checkbox_bias.isChecked():  mode.append("Bias")
        return mode

    def confirm_selection(self):
        selected = []
        for r in range(self.joint_grid.rowCount()):
            for c in range(self.joint_grid.columnCount()):
                it = self.joint_grid.itemAtPosition(r, c)
                if it and isinstance(it.widget(), QCheckBox) and it.widget().isChecked():
                    selected.append(it.widget().text())
        logwarn(f'Selected joints: {selected}')
        return selected

    def duration_amplitude(self):
        try:
            return (float(self.duration_min.text()), float(self.duration_max.text()),
                    float(self.amplitude_min.text()), float(self.amplitude_max.text()))
        except ValueError:
            logwarn("Invalid input for duration or amplitude.")
            return 0, 0, 0, 0


class LogBridge(QObject):
    """Marshals ROS-thread callbacks safely to the Qt GUI thread."""
    progress_signal = pyqtSignal(float)


class ProgressPage(QWidget):
    def __init__(self):
        super().__init__()
        self.logos = Logos(); self.setGeometry(100, 100, 300, 200)
        self.label = QLabel('')
        self.progress_bar = QProgressBar(self); self.progress_bar.setRange(0, 100)
        self.button        = QPushButton('Start Progress')
        self.button_badger = QPushButton('Badger')
        self.button_badger.setIcon(QIcon(ICON['badger']))
        self.button_badger.setIconSize(self.button_badger.sizeHint())
        self.button_plot   = QPushButton('Plot')
        self.button_badger.setEnabled(False); self.button_plot.setEnabled(False)

        self.bridge = LogBridge()
        self.bridge.progress_signal.connect(self._set_progress)
        self.button.clicked.connect(lambda: self.start_progress(1, 1))

        lay = QVBoxLayout(self)
        for w in (self.logos, self.label, self.progress_bar, self.button_plot, self.button_badger):
            lay.addWidget(w)
        self._log_sub = None

    def start_progress(self, current_run, runs):
        self.current_run, self.runs = current_run, runs
        if self._log_sub is None:
            self._log_sub = ros_node.create_subscription(Log, '/rosout', self._log_cb, 10)

    def _log_cb(self, data):
        if task_type == 2 and "round3 end" in data.msg:
            self.bridge.progress_signal.emit(100 * self.current_run / self.runs)
        elif task_type == 1 and "Round end" in data.msg:
            self.bridge.progress_signal.emit(100 * self.current_run / self.runs)

    def _set_progress(self, value):
        self.progress_bar.setValue(int(value))
        if value >= 100:
            self.button_badger.setEnabled(True); self.button_plot.setEnabled(True)


class WorkpiecePage(QWidget):
    def __init__(self):
        super().__init__()
        self.logos = Logos()
        self.label = make_label("Work Piece:", bold=True)
        self.button_geometry = make_button("Geometry")
        self.button_position = make_button("Position")
        self.button_next = next_btn(); self.button_back = back_btn(); self.button_kill = kill_btn()
        lay = QVBoxLayout(self); lay.addWidget(self.logos)
        lay.addWidget(self.label); lay.setAlignment(self.label, Qt.AlignCenter)
        for b in (self.button_geometry, self.button_position):
            lay.addWidget(b); lay.setAlignment(b, Qt.AlignCenter)
        lay.addLayout(bottom_nav(left=self.button_back, right=self.button_next))


class ProcessPage(QWidget):
    def __init__(self, primary_label):
        super().__init__()
        self.logos = Logos()
        self.label = make_label("Process:", bold=True)
        self.button_primary = make_button(primary_label)
        self.button_hands   = make_button("Hands")
        self.button_next, self.button_back = next_btn(), back_btn()
        lay = QVBoxLayout(self); lay.addWidget(self.logos)
        lay.addWidget(self.label); lay.setAlignment(self.label, Qt.AlignCenter)
        for b in (self.button_primary, self.button_hands):
            lay.addWidget(b); lay.setAlignment(b, Qt.AlignCenter)
        lay.addLayout(bottom_nav(left=self.button_back, right=self.button_next))


class TaskExecutionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.logos = Logos()
        self.label    = make_label("Execution:", bold=True)
        self.label_1  = make_label("Fault Information:", bold=True)
        self.label_2  = make_label("\n\nFault Amplitude:")
        self.label_3  = make_label("\n\nFault Location:")
        self.label_4  = make_label("\n\nFault Duration:")
        self.label_T  = make_label("\n\nFault Time:")
        self.label_S  = make_label("\n\nSpeed:")
        self.label_A  = make_label("\n\nAcceleration:")
        self.label_P  = make_label("\n\nPlanning Algorithm:")
        self.label_I  = make_label("\n\nActuation Info:", bold=True)
        for lbl in (self.label, self.label_1): lbl.setFixedHeight(40)

        self.button_start  = make_button("Start",  (200, 100), ICON['play'])
        self.button_start.setCheckable(True)
        self.button_kill   = make_button("Reset",  (150, 80),  ICON['close'])
        self.button_badger = make_button("Badger", (200, 100), ICON['badger'])
        self.button_badger.setEnabled(False)
        self.button_back = back_btn()
        self.button_fault_injector = make_button("Inject Fault", (250, 60))

        lay1 = QVBoxLayout(); lay1.addWidget(self.label)
        for b in (self.button_start, self.button_badger):
            lay1.addWidget(b); lay1.setAlignment(b, Qt.AlignCenter)
        lay1.addLayout(bottom_nav(left=self.button_back, right=self.button_kill))
        self.frame_1 = QFrame(self); self.frame_1.setFrameShape(QFrame.StyledPanel); self.frame_1.setLayout(lay1)

        self.label_5 = QLabel("Faults:"); self.label_5.setStyleSheet(LABEL_BOLD); self.label_5.setFixedHeight(40)
        self.dropdown = QComboBox(self); self.dropdown.setFixedSize(250, 60)
        for item in ('None', 'Bias', 'Noise', 'Failure demo'): self.dropdown.addItem(item)
        self.image_label = QLabel(self); self.image_label.setFixedSize(400, 300)
        self.image_label.setAlignment(Qt.AlignCenter); self.update_image(NONE_IMG)

        lay2 = QVBoxLayout(); lay2.addWidget(self.label_5)
        lay2.addWidget(self.dropdown,    alignment=Qt.AlignCenter)
        lay2.addWidget(self.image_label, alignment=Qt.AlignCenter)
        lay2.addWidget(self.button_fault_injector, alignment=Qt.AlignCenter)
        self.frame_2 = QFrame(self); self.frame_2.setFrameShape(QFrame.StyledPanel); self.frame_2.setLayout(lay2)

        lay3 = QVBoxLayout()
        for lbl in (self.label_1, self.label_2, self.label_3, self.label_4,
                    self.label_T, self.label_I, self.label_S, self.label_A, self.label_P):
            lay3.addWidget(lbl)
        for _ in range(2): lay3.addStretch()
        self.frame_3 = QFrame(self); self.frame_3.setFrameShape(QFrame.StyledPanel); self.frame_3.setLayout(lay3)

        h = QHBoxLayout()
        for f in (self.frame_1, self.frame_2, self.frame_3): h.addWidget(f)
        outer = QVBoxLayout(self); outer.addWidget(self.logos); outer.addLayout(h)

    def update_image(self, path):
        pm = QPixmap(path)
        self.image_label.setPixmap(pm.scaled(self.image_label.size(), Qt.KeepAspectRatio))


class BadgerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.logos = Logos()
        self.label   = QLabel("Fault types:")
        self.label_1 = QLabel("Fault Information:")
        self.label_2 = QLabel("\n\nFault Number:")
        self.label_min = QLabel("\n\nFault Min:")
        self.label_max = QLabel("\n\nFault Max:")
        for lbl in (self.label, self.label_1): lbl.setFixedHeight(40)

        self.button_badger_fault_injector = make_button("Generate", (250, 60))

        self.label_4 = QLabel("Fault types:");     self.label_4.setFixedHeight(40)
        self.label_5 = QLabel("Fault locations:"); self.label_5.setFixedHeight(40)

        self.dropdown = QComboBox(self); self.dropdown.setFixedSize(250, 60)
        for it in ('ZerosPattern', 'RandomPattern', 'Drift', 'MissingPoints'):
            self.dropdown.addItem(it)

        self.dropdown_fault_location = QComboBox(self)
        self.dropdown_fault_location.setFixedSize(250, 60)
        for i in range(7): self.dropdown_fault_location.addItem(f'Joint{i}')

        lay2 = QVBoxLayout(); lay2.addWidget(self.label_4)
        lay2.addWidget(self.dropdown, alignment=Qt.AlignCenter)
        lay2.addWidget(self.label_5)
        lay2.addWidget(self.dropdown_fault_location, alignment=Qt.AlignCenter)
        lay2.addWidget(self.button_badger_fault_injector, alignment=Qt.AlignCenter)
        self.frame_2 = QFrame(self); self.frame_2.setFrameShape(QFrame.StyledPanel); self.frame_2.setLayout(lay2)

        lay3 = QVBoxLayout()
        for lbl in (self.label_1, self.label_2, self.label_min, self.label_max): lay3.addWidget(lbl)
        for _ in range(2): lay3.addStretch()
        self.frame_3 = QFrame(self); self.frame_3.setFrameShape(QFrame.StyledPanel); self.frame_3.setLayout(lay3)

        h = QHBoxLayout(); h.addWidget(self.frame_2); h.addWidget(self.frame_3)
        outer = QVBoxLayout(self); outer.addWidget(self.logos); outer.addLayout(h)


# ============================================================
# Main window
# ============================================================
class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gazebo_process = None
        self.put_robot_in_gazebo = None
        self.execution_process = None
        self.drilling_flag = self.welding_flag = None
        self.fault_location = self.fault_amplitude = self.fault_duration = self.start_time = None
        self.task_flag = None
        self.gazebo_killed = False
        self.fault_type = None
        self.task_completion_flag = None
        self.rosbag_directory = ROSBAG_DIR
        self.csv_output_directory = ROSCSV_DIR
        self._init_ui()

    # ---------- UI setup ----------
    def _init_ui(self):
        self.setWindowTitle("Time Series Data Generator")
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.pages = {
            'main':               MainPage(),
            'generator':          TasksPage(),
            'drill_generator':    TaskGeneratorPage(),
            'welding_generator':  TaskGeneratorPage(),
            'demonstrator':       TasksPage(),
            'drilling':           WorkpiecePage(),
            'drilling_set_holes': ProcessPage("Holes"),
            'drilling_execution': TaskExecutionPage(),
            'welding':            WorkpiecePage(),
            'welding_set_line':   ProcessPage("Line"),
            'welding_execution':  TaskExecutionPage(),
            'badger_page':        BadgerPage(),
            'progress':           ProgressPage(),
        }
        for p in self.pages.values(): self.stacked_widget.addWidget(p)
        self._connect_buttons()
        self.stacked_widget.setCurrentWidget(self.pages['main'])

    def _connect_buttons(self):
        P = self.pages
        P['main'].button_generator.clicked.connect(self.go_to_generator_page)
        P['main'].button_demonstrator.clicked.connect(self.go_to_demonstrator_page)
        P['generator'].button_back.clicked.connect(self.go_to_main_page)
        P['generator'].button_welding.clicked.connect(self.go_to_welding_page_genemode)
        P['generator'].button_drilling.clicked.connect(self.go_to_drilling_page_genemode)
        P['drill_generator'].button_go.clicked.connect(self.go_to_progress_page)
        P['drill_generator'].button_back.clicked.connect(self.go_to_generator_page)
        P['welding_generator'].button_go.clicked.connect(self.go_to_progress_page)
        P['welding_generator'].button_back.clicked.connect(self.go_to_generator_page)
        P['demonstrator'].button_drilling.clicked.connect(self.go_to_drilling_page)
        P['demonstrator'].button_welding.clicked.connect(self.go_to_welding_page)
        P['demonstrator'].button_back.clicked.connect(self.go_to_main_page)

        P['drilling'].button_geometry.clicked.connect(self.randomize_geometry)
        P['drilling'].button_position.clicked.connect(self.randomize_position)
        P['drilling'].button_next.clicked.connect(self.go_to_set_holes_page)
        P['drilling'].button_back.clicked.connect(self.go_to_demonstrator_page)
        P['drilling'].button_kill.clicked.connect(self.kill_gazebo)
        P['drilling_set_holes'].button_primary.clicked.connect(self.randomize_holes)
        P['drilling_set_holes'].button_hands.clicked.connect(self.randomize_hands)
        P['drilling_set_holes'].button_next.clicked.connect(self.go_to_drilling_execution_page)
        P['drilling_set_holes'].button_back.clicked.connect(self.go_to_drilling_page)
        ep = P['drilling_execution']
        ep.button_start.toggled.connect(self.start_drilling_execution)
        ep.button_badger.clicked.connect(self.start_badger)
        ep.button_back.clicked.connect(self.go_to_set_holes_page)
        ep.dropdown.currentIndexChanged.connect(self.fault_options)
        ep.button_fault_injector.clicked.connect(self.fault_injector)

        P['welding'].button_geometry.clicked.connect(self.randomize_geometry)
        P['welding'].button_position.clicked.connect(self.randomize_position)
        P['welding'].button_next.clicked.connect(self.go_to_set_welding_line_page)
        P['welding'].button_back.clicked.connect(self.go_to_demonstrator_page)
        P['welding'].button_kill.clicked.connect(self.kill_gazebo)
        P['welding_set_line'].button_primary.clicked.connect(self.randomize_line)
        P['welding_set_line'].button_hands.clicked.connect(self.randomize_hands)
        P['welding_set_line'].button_next.clicked.connect(self.go_to_welding_execution_page)
        P['welding_set_line'].button_back.clicked.connect(self.go_to_welding_page)
        wp = P['welding_execution']
        wp.button_start.toggled.connect(self.start_welding_execution)
        wp.button_badger.clicked.connect(self.start_badger)
        wp.button_back.clicked.connect(self.go_to_set_welding_line_page)
        wp.dropdown.currentIndexChanged.connect(self.fault_options)
        wp.button_fault_injector.clicked.connect(self.fault_injector)

        P['progress'].button_plot.clicked.connect(self.generator_plot)
        P['progress'].button_badger.clicked.connect(self.start_badger)
        P['badger_page'].dropdown.currentIndexChanged.connect(self.badger_fault_options)
        P['badger_page'].dropdown_fault_location.currentIndexChanged.connect(self.badger_fault_location_options)
        P['badger_page'].button_badger_fault_injector.clicked.connect(self.badger_fault_injector)

    # ---------- Navigation ----------
    def _current_exec(self):
        w = self.stacked_widget.currentWidget()
        return w if isinstance(w, TaskExecutionPage) else None

    def go_to_main_page(self):        self.stacked_widget.setCurrentWidget(self.pages['main'])
    def go_to_generator_page(self):   self.stacked_widget.setCurrentWidget(self.pages['generator'])

    def go_to_demonstrator_page(self):
        if type(self.stacked_widget.currentWidget()).__name__ == "WorkpiecePage":
            self.kill_gazebo()
        self.stacked_widget.setCurrentWidget(self.pages['demonstrator'])
        self.gazebo_killed = False

    def go_to_drilling_page(self):
        self.task_flag = 1
        if isinstance(self.stacked_widget.currentWidget(), TasksPage) or self.gazebo_killed:
            self.launch_gazebo(*ros2_launch('panda_gazebo', 'start_workscene.launch.py'))
            self.gazebo_killed = False
        self.stacked_widget.setCurrentWidget(self.pages['drilling'])

    def go_to_welding_page(self):
        self.task_flag = 0
        if isinstance(self.stacked_widget.currentWidget(), TasksPage) or self.gazebo_killed:
            self.launch_gazebo(*ros2_launch('panda_gazebo', 'start_workscene_welding.launch.py'))
            self.gazebo_killed = False
        self.stacked_widget.setCurrentWidget(self.pages['welding'])

    def go_to_set_holes_page(self):
        if isinstance(self.stacked_widget.currentWidget(), TaskExecutionPage):
            self.remove_robot(); logwarn('removing robot')
        self.stacked_widget.setCurrentWidget(self.pages['drilling_set_holes'])
        self.run_command(ros2_run('panda_gazebo', 'randomize_hole_position.py'))
        self.run_command(ros2_run('panda_gazebo', 'randomize_hand_position.py'))
        self.drilling_flag = True
        return self.drilling_flag

    def go_to_set_welding_line_page(self):
        if isinstance(self.stacked_widget.currentWidget(), TaskExecutionPage):
            self.remove_robot(); logwarn('removing robot')
        self.stacked_widget.setCurrentWidget(self.pages['welding_set_line'])
        self.run_command(ros2_run('panda_gazebo', 'randomize_welding_line.py'))
        self.run_command(ros2_run('panda_gazebo', 'randomize_hand_position.py'))
        self.welding_flag = True
        return self.welding_flag

    def _launch_robot_and_execution(self, robot_launch, ee_script):
        if self.put_robot_in_gazebo:
            QMessageBox.critical(self, "Robot is already in the scene", ""); return
        try:
            gripper = "drill" if "drill" in ee_script else "welding"
            self.put_robot_in_gazebo = subprocess.Popen(
                ros2_launch('panda_gazebo', robot_launch,
                            'load_gripper:=false', f'gripper:={gripper}'))
            time.sleep(5)
            self.execution_process = subprocess.Popen(ros2_run('panda_gazebo', ee_script))
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Error adding robot: {e}")

    def go_to_drilling_execution_page(self):
        if self.drilling_flag:
            self.stacked_widget.setCurrentWidget(self.pages['drilling_execution'])
        self._launch_robot_and_execution('put_robot_in_world.launch.py', 'ee_location_drilling.py')

    def go_to_welding_execution_page(self):
        if self.welding_flag:
            self.stacked_widget.setCurrentWidget(self.pages['welding_execution'])
        self._launch_robot_and_execution('put_robot_in_world_welding.launch.py',
                                         'ee_location_welding.py')

    def go_to_drilling_page_genemode(self):
        global task_type; task_type = 2
        if isinstance(self.stacked_widget.currentWidget(), TasksPage):
            try:
                self.launch_gazebo(*ros2_run('gui', 'generator_mode.py'))
                time.sleep(3)
                self.execution_process = subprocess.Popen(
                    ros2_run('panda_gazebo', 'ee_location_drilling.py'))
                logerr('Setup Launched Successfully')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting Workscene: {e}")
        self.stacked_widget.setCurrentWidget(self.pages['drill_generator'])

    def go_to_welding_page_genemode(self):
        global task_type; task_type = 1
        if isinstance(self.stacked_widget.currentWidget(), TasksPage):
            try:
                self.launch_gazebo(*ros2_run('gui', 'generator_mode_welding.py'))
                time.sleep(3)
                self.execution_process = subprocess.Popen(
                    ros2_run('panda_gazebo', 'ee_location_welding.py'))
                logerr('Setup Launched Successfully')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting Workscene: {e}")
        self.stacked_widget.setCurrentWidget(self.pages['welding_generator'])

    def go_to_progress_page(self):
        cur = self.stacked_widget.currentWidget()
        t = None
        if cur is self.pages['drill_generator']:
            t = threading.Thread(target=self._run_generator, args=('drilling',), daemon=True)
        elif cur is self.pages['welding_generator']:
            t = threading.Thread(target=self._run_generator, args=('welding',), daemon=True)
        if t:
            t.start(); threads.append(t)
        self.stacked_widget.setCurrentWidget(self.pages['progress'])

    # ---------- Generator (unified) ----------
    def _run_generator(self, task):
        global joint_index, fault_amplitude, fault_duration, start_time, fault_type, count
        cfg = {
            'drilling': {'page': self.pages['drill_generator'],   'script': 'drilling.py'},
            'welding':  {'page': self.pages['welding_generator'], 'script': 'welding.py'},
        }[task]
        page = cfg['page']
        run_value = page.number_of_run()
        dmin, dmax, amin, amax = page.duration_amplitude()
        fault_modes = page.checkbox_state_changed()
        joints = page.confirm_selection()
        logwarn(f'{joints}'); logwarn(f'{fault_modes}')

        js_proc = subprocess.Popen(ros2_run('joint_state_publisher', 'recorder'))
        time.sleep(3)
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        bag_dir = os.path.join(ROSBAG_DIR, f'record_{ts}')
        os.makedirs(ROSBAG_DIR, exist_ok=True)
        bag_proc = subprocess.Popen(['ros2', 'bag', 'record', '-o', bag_dir, '/record'])

        try:
            for i in range(run_value):
                count = 0
                self.pages['progress'].start_progress(i + 1, run_value)
                self.pages['progress'].label.setText(f'Runs: {i+1}/{run_value}')

                fault_duration.data  = round(random.uniform(dmin, dmax), 2)
                fault_amplitude.data = round(random.uniform(amin, amax), 2)
                self.fault_location  = random.choice(joints)
                joint_index.data     = FAULT_JOINTS.index(self.fault_location)
                start_time.data      = get_sim_time_sec() + round(random.uniform(10, 30))
                fname = random.choice(fault_modes)
                fault_type.data = 1 if fname == 'Bias' else 2
                logerr(f'Fault name {fname}')

                try:
                    self.fault_injector()
                    proc = subprocess.Popen(ros2_run('pick_and_place', cfg['script']))
                    setattr(self, f'{task}_process', proc)
                    logwarn(f"{task.capitalize()} execution started")
                    logerr(f'execution {i}')
                    proc.wait()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error starting execution: {e}")
                finally:
                    if getattr(self, 'fault_process', None): self.fault_process.terminate()
                    if getattr(self, 'fault_thread', None):  self.fault_thread.join(timeout=1)
        finally:
            js_proc.terminate(); bag_proc.terminate()
            self.pages['progress'].label.setText('Complete!')

    # ---------- Fault selection ----------
    def fault_options(self):
        ep = self._current_exec()
        if ep is None: return None
        sel = ep.dropdown.currentText()
        if sel == 'None':          self.clear_fault()
        elif sel == 'Bias':        self._fault_generator('spike_config.yaml', 1)
        elif sel == 'Noise':       self._fault_generator('noise_config.yaml', 2)
        elif sel == 'Failure demo':self._fault_generator('fault_demo.yaml',  1, single_joint=True)
        if sel != 'None': self._update_image_based_on_joint()
        return sel

    def _fault_generator(self, cfg_name, ftype, single_joint=False):
        # ROS 2: declare or set use_sim_time on our own node
        try:
            ros_node.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        except Exception:
            pass

        self.image_mapping = ({0: f'{RES}/joint1.jpg'} if single_joint else JOINT_IMG_MAP)

        global joint_index, fault_amplitude, fault_duration, start_time, fault_type
        try:
            with open(f"{BASE}/{cfg_name}", 'r') as f:
                d = yaml.safe_load(f)
            dmin, dmax = d['fault_duration_min'], d['fault_duration_max']
            amin, amax = d['fault_amplitude_min'], d['fault_amplitude_max']
            fjoints    = d['joint_names']

            self.fault_duration  = round(random.uniform(dmin, dmax), 2)
            self.fault_amplitude = round(random.uniform(amin, amax), 2)
            self.fault_location  = random.choice(fjoints)
            self.joint_index     = fjoints.index(self.fault_location)
            self.start_time      = get_sim_time_sec() + round(random.uniform(10, 30))

            fault_duration.data  = self.fault_duration
            fault_amplitude.data = self.fault_amplitude
            joint_index.data     = self.joint_index
            start_time.data      = self.start_time
            fault_type.data      = ftype

            ep = self._current_exec()
            if ep is not None:
                ep.label_2.setText(f"\n\nFault Amplitude: {self.fault_amplitude}")
                ep.label_3.setText(f"\n\nFault Location: {self.fault_location}")
                ep.label_4.setText(f"\n\nFault Duration: {self.fault_duration}")
                ep.label_T.setText(f"\n\nFault Time: {self.start_time}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating fault: {e}")

        logwarn('Fault created successfully')
        return self.joint_index, self.fault_amplitude, self.fault_duration, self.start_time

    def clear_fault(self):
        self.fault_duration = self.fault_amplitude = self.joint_index = self.start_time = 0
        ep = self._current_exec()
        if ep is not None:
            ep.label_2.setText("\n\nFault Amplitude:")
            ep.label_3.setText("\n\nFault Location:")
            ep.label_4.setText("\n\nFault Duration:")
            ep.label_T.setText("\n\nFault Time:")
        self.update_image(NONE_IMG)

    def _update_image_based_on_joint(self):
        idx = getattr(self, 'joint_index', None)
        path = self.image_mapping.get(idx, NONE_IMG) if idx is not None else NONE_IMG
        self.update_image(path)

    def update_image(self, path):
        pm = QPixmap(path)
        for key in ('drilling_execution', 'welding_execution'):
            lbl = self.pages[key].image_label
            lbl.setPixmap(pm.scaled(lbl.size(), aspectRatioMode=1))

    # ---------- Badger ----------
    def start_badger(self): self.stacked_widget.setCurrentWidget(self.pages['badger_page'])

    def badger_fault_options(self):
        self.badger_selected_option = self.pages['badger_page'].dropdown.currentText()
        opt = self.badger_selected_option
        if opt in ('ZerosPattern', 'RandomPattern'):
            self.badger_numbers = random.randint(1, 5)
            self.badger_min = random.randint(10, 50); self.badger_max = random.randint(100, 200)
            self._set_badger_labels("Fault Number", "Fault Min", "Fault Max")
        elif opt == 'Drift':
            self.badger_numbers = random.uniform(-0.001, 0.001)
            self.badger_min = random.randint(100, 1000); self.badger_max = None
            self._set_badger_labels("Fault Slope", "Fault Start", "Fault End")
        elif opt == 'MissingPoints':
            self.badger_numbers = random.randint(100, 500)
            self.badger_min = self.badger_max = None
            self._set_badger_labels("Fault Number", "Fault Min", "Fault Max")
        return opt

    def _set_badger_labels(self, l_num, l_min, l_max):
        p = self.pages['badger_page']
        p.label_2.setText(f"\n\n{l_num}: {self.badger_numbers}")
        p.label_min.setText(f"\n\n{l_min}: {self.badger_min}")
        p.label_max.setText(f"\n\n{l_max}: {self.badger_max}")

    def badger_fault_location_options(self):
        self.badger_selected_joint = self.pages['badger_page'].dropdown_fault_location.currentText()
        self.badger_joint_number = self.badger_selected_joint[5:]
        return self.badger_joint_number

    def badger_fault_injector(self):
        if not all([getattr(self, 'badger_selected_option', None),
                    getattr(self, 'badger_numbers', None),
                    getattr(self, 'badger_joint_number', None)]):
            QMessageBox.information(self, "Failed", "Need information about fault."); return
        col = f'field.real_joint_states.position{self.badger_joint_number}'
        opt = self.badger_selected_option
        scripts = {
            'ZerosPattern':   'test_zerosger.py',
            'RandomPattern':  'test_patternsger.py',
            'Drift':          'test_trends.py',
            'MissingPoints':  'test_missingness.py',
        }
        script = f'src/badgers-main/tests/generators/time_series/{scripts[opt]}'
        if opt in ('ZerosPattern', 'RandomPattern'):
            prefix = 'n_zerospatterns' if opt == 'ZerosPattern' else 'n_patterns'
            cmd = ['python3', script, '--column', col,
                   f'--{prefix}', str(self.badger_numbers),
                   '--min_width_patterns', str(self.badger_min),
                   '--max_width_patterns', str(self.badger_max)]
        elif opt == 'Drift':
            cmd = ['python3', script, '--column', col,
                   '--slope', str(self.badger_numbers),
                   '--start_point', str(self.badger_min)]
        else:
            cmd = ['python3', script, '--column', col,
                   '--n_missing', str(self.badger_numbers)]
        self.badger_process = subprocess.Popen(cmd)

    # ---------- Gazebo / commands ----------
    def launch_gazebo(self, *args):
        try: self.gazebo_process = subprocess.Popen(args)
        except Exception as e: QMessageBox.critical(self, "Error", f"Error launching Gazebo: {e}")

    def kill_gazebo(self):
        if not self.gazebo_process: return
        self.gazebo_process.terminate()
        try:    self.gazebo_process.wait(timeout=10)
        except subprocess.TimeoutExpired: self.gazebo_process.kill()
        finally:
            self.gazebo_process = None
            for proc in ('gzserver', 'gzclient', 'gz'):
                subprocess.run(['pkill', '-f', proc], check=False)
        logwarn('Gazebo Terminated'); self.gazebo_killed = True

        cls = type(self.stacked_widget.currentWidget()).__name__
        if cls in ("ProcessPage", "TaskExecutionPage"):
            if self.task_flag == 1:
                self.launch_gazebo(*ros2_launch('panda_gazebo', 'start_workscene.launch.py'))
                if cls == "TaskExecutionPage": self.remove_robot()
                self.stacked_widget.setCurrentWidget(self.pages['drilling'])
            elif self.task_flag == 0:
                self.launch_gazebo(*ros2_launch('panda_gazebo', 'start_workscene_welding.launch.py'))
                if cls == "TaskExecutionPage": self.remove_robot()
                self.stacked_widget.setCurrentWidget(self.pages['welding'])

    def randomize_geometry(self): self.run_command(ros2_run('panda_gazebo', 'modify_geometry.py'))
    def randomize_position(self): self.run_command(ros2_run('panda_gazebo', 'randomize_workpiece_position.py'))
    def randomize_holes(self):
        self.run_command(ros2_run('panda_gazebo', 'randomize_hole_position.py'))
        self.drilling_flag = True; return self.drilling_flag
    def randomize_line(self):
        self.run_command(ros2_run('panda_gazebo', 'randomize_welding_line.py'))
        self.welding_flag = True; return self.welding_flag
    def randomize_hands(self):    self.run_command(ros2_run('panda_gazebo', 'randomize_hand_position.py'))

    def run_command(self, command):
        try: subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def remove_robot(self):
        """Calls ROS 2 /delete_entity service (replaces ROS 1 /gazebo/delete_model)."""
        try:
            client = ros_node.create_client(DeleteEntity, '/delete_entity')
            if not client.wait_for_service(timeout_sec=5.0):
                raise RuntimeError("Service /delete_entity not available")
            req = DeleteEntity.Request(); req.name = 'panda'
            future = client.call_async(req)
            # Executor is spinning in background; just wait on the future.
            deadline = time.time() + 5.0
            while not future.done() and time.time() < deadline: time.sleep(0.05)
            if not future.done():
                raise RuntimeError("Timeout waiting for /delete_entity response")

            if self.put_robot_in_gazebo:
                self.put_robot_in_gazebo.terminate()
            self.put_robot_in_gazebo = None
            time.sleep(1)
            self.run_command(ros2_run('panda_gazebo', 'initialize_hand_position.py'))
            w = self.stacked_widget.currentWidget()
            if w is self.pages['drilling_execution']:
                self.run_command(ros2_run('panda_gazebo', 'initialize_hole_position.py'))
            elif w is self.pages['welding_execution']:
                self.run_command(ros2_run('panda_gazebo', 'initialize_welding_line.py'))
            QMessageBox.information(self, "Success", "Robot has been removed from the scene.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove robot: {e}")

    # ---------- Execution start/stop (unified) ----------
    def _start_execution(self, task, checked):
        page_key = f'{task}_execution'
        ep = self.pages[page_key]
        script = f'{task}.py'
        if checked:
            ep.button_start.setText("Stop")
            ep.button_start.setIcon(QIcon(ICON['stop']))
            try:
                self.task_completion_flag = False
                setattr(self, f'{task}_joint_state_process',
                        subprocess.Popen(ros2_run('joint_state_publisher', 'recorder')))
                time.sleep(3)
                proc = subprocess.Popen(ros2_run('pick_and_place', script))
                setattr(self, f'{task}_process', proc)
                threading.Thread(target=self._process_monitor,
                                 args=(proc, task), daemon=True).start()

                speed      = wait_for_message(Float32, 'speed',              timeout_sec=10)
                accel      = wait_for_message(Float32, 'acceleration',       timeout_sec=10)
                plan_algo  = wait_for_message(String,  'planning_algorithm', timeout_sec=10)
                if speed:     ep.label_S.setText(f"\n\nSpeed: {speed.data}")
                if accel:     ep.label_A.setText(f"\n\nAcceleration: {accel.data}")
                if plan_algo: ep.label_P.setText(f"\n\nPlanning Algorithm: {plan_algo.data}")

                ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                bag_dir = os.path.join(ROSBAG_DIR, f'record_{ts}')
                os.makedirs(ROSBAG_DIR, exist_ok=True)
                setattr(self, f'{task}_rosbag_process',
                        subprocess.Popen(['ros2', 'bag', 'record', '-o', bag_dir, '/record']))
                logwarn(f"{task.capitalize()} execution started")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error starting execution: {e}")
        else:
            self._stop_execution(task)

    def _stop_execution(self, task):
        if self.task_completion_flag: return
        for suffix in ('joint_state_process', 'process', 'rosbag_process'):
            self.terminate_process(getattr(self, f'{task}_{suffix}', None))

        bag_dir = self.find_newest_bag_dir()
        csv_path = os.path.join(ROSCSV_DIR, os.path.basename(bag_dir) + '.csv')
        convert_bag_to_csv(bag_dir, csv_path, '/record')
        time.sleep(2)
        subprocess.Popen(ros2_run('panda_gazebo', 'plot.py',
                                  '--joint_state_column', str(joint_index.data)))
        logwarn(f"{task.capitalize()} execution terminated")
        ep = self.pages[f'{task}_execution']
        ep.button_start.setText("Start"); ep.button_start.setIcon(QIcon(ICON['play']))
        ep.button_start.setChecked(False); ep.button_badger.setEnabled(True)
        self.task_completion_flag = True

    def start_drilling_execution(self, checked): self._start_execution('drilling', checked)
    def start_welding_execution(self,  checked): self._start_execution('welding',  checked)

    def _process_monitor(self, process, task):
        while process.poll() is None: time.sleep(1)
        logwarn(f"Process {process.args} finished with exit code {process.returncode}")
        if process.returncode == 0: self._stop_execution(task)

    def terminate_process(self, process):
        if not process: return
        try:
            process.terminate(); process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logwarn("Process did not terminate gracefully, killing it forcefully")
            process.kill()

    # ---------- Plot / bag discovery ----------
    def generator_plot(self):
        bag_dir  = self.find_newest_bag_dir()
        csv_path = os.path.join(ROSCSV_DIR, os.path.basename(bag_dir) + '.csv')
        convert_bag_to_csv(bag_dir, csv_path, '/record')
        time.sleep(2)
        self.gene_plot = subprocess.Popen(ros2_run('panda_gazebo', 'plot_generator.py'))

    def find_newest_bag_dir(self):
        """ROS 2 bags are directories, not files."""
        if not os.path.isdir(self.rosbag_directory):
            raise FileNotFoundError(f"{self.rosbag_directory} does not exist.")
        dirs = [d for d in os.listdir(self.rosbag_directory)
                if os.path.isdir(os.path.join(self.rosbag_directory, d))]
        if not dirs:
            raise FileNotFoundError("No bag directories found.")
        dirs.sort(key=lambda d: os.path.getmtime(os.path.join(self.rosbag_directory, d)),
                  reverse=True)
        return os.path.join(self.rosbag_directory, dirs[0])

    # ---------- Fault injection ----------
    def fault_injector(self):
        global pub_state, sub_joint
        if sub_joint is not None:
            ros_node.destroy_subscription(sub_joint); sub_joint = None
        pub_state = False
        logwarn('Launching fault injector node')

        def run():
            try:
                self.fault_process = subprocess.Popen(
                    ros2_run('joint_state_publisher', 'fault_injector'))
                self.fault_process.wait()
            except Exception as e:
                logerr(f"Fault injector failed: {e}")

        self.fault_thread = threading.Thread(target=run, daemon=True)
        self.fault_thread.start(); threads.append(self.fault_thread)

        # Wait for at least one subscriber on each latched topic
        t0 = time.time()
        while (pub_index.get_subscription_count() == 0 or
               pub_amplitude.get_subscription_count() == 0 or
               pub_duration.get_subscription_count() == 0 or
               pub_time.get_subscription_count() == 0):
            if time.time() - t0 > 15: break
            loginfo("Waiting for subscribers...")
            time.sleep(0.01)

        for _ in range(20):
            pub_index.publish(joint_index)
            pub_amplitude.publish(fault_amplitude)
            pub_duration.publish(fault_duration)
            pub_time.publish(start_time)
            pub_type.publish(fault_type)
            time.sleep(0.1)

        logwarn('Fault inserted successfully')
        return pub_state

    def closeEvent(self, event):
        close_event_handler(); event.accept()


# ============================================================
# ROS callbacks / shutdown
# ============================================================
def joint_callback(js: JointState):
    pub.publish(js)
    flag = Int32(); flag.data = 0
    pub_fault.publish(flag)   # ROS 2: publish() requires a message


def close_event_handler():
    print("Shutting down ROS 2...")
    try:
        if executor is not None: executor.shutdown()
    except Exception: pass
    try:
        if ros_node is not None: ros_node.destroy_node()
    except Exception: pass
    try:
        if rclpy.ok(): rclpy.shutdown()
    except Exception: pass

    for t in threads:
        if t is not None and t.is_alive():
            t.join(timeout=1)

    for proc in ('gazebo', 'gzserver', 'gzclient', 'gz', 'rviz', 'rviz2'):
        try:
            subprocess.call(['pkill', '-f', proc])
        except Exception as e:
            print(f"Error terminating {proc}: {e}")
    print("Shutdown complete.")


# ============================================================
# Main entrypoint
# ============================================================
def main():
    global ros_node, executor
    global pub, pub_index, pub_duration, pub_amplitude, pub_time, pub_fault, pub_type, sub_joint

    rclpy.init()
    ros_node = rclpy.create_node(
        'run',
        parameter_overrides=[Parameter('use_sim_time', Parameter.Type.BOOL, True)],
    )

    # Publishers (latched ones use TRANSIENT_LOCAL QoS)
    pub           = ros_node.create_publisher(JointState, '/faulty_joint_states', 100)
    pub_index     = ros_node.create_publisher(Int32,   'fault_index',     LATCHED_QOS)
    pub_duration  = ros_node.create_publisher(Float32, 'fault_duration',  LATCHED_QOS)
    pub_amplitude = ros_node.create_publisher(Float32, 'fault_amplitude', LATCHED_QOS)
    pub_time      = ros_node.create_publisher(Float32, 'fault_time',      LATCHED_QOS)
    pub_fault     = ros_node.create_publisher(Int32,   'fault_flag',      LATCHED_QOS)
    pub_type      = ros_node.create_publisher(Int32,   'fault_type',      LATCHED_QOS)

    sub_joint = ros_node.create_subscription(JointState, '/joint_states', joint_callback, 10)

    executor = MultiThreadedExecutor()
    executor.add_node(ros_node)
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start(); threads.append(ros_thread)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON['icon']))
    win = Gui()
    win.closeEvent = lambda event: close_event_handler()
    win.show()
    try:
        sys.exit(app.exec_())
    finally:
        close_event_handler()


if __name__ == "__main__":
    main()