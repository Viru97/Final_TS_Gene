#!/usr/bin/env python3
"""Compatibility launcher for the ROS 2 GUI module."""

import os
import runpy


if __name__ == '__main__':
    target = os.path.join(os.path.dirname(__file__), 'gui', 'gui.py')
    runpy.run_path(target, run_name='__main__')
