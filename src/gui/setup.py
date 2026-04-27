from setuptools import setup
import os
from glob import glob

package_name = 'gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # This ensures your GUI can still find your logo/image assets after building!
        (os.path.join('share', package_name, 'logos'), glob('logos/*')),
        (os.path.join('share', package_name, 'resource'), glob('resource/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='The gui package for TS Gene',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # This maps the terminal command 'ros2 run gui gui_node' to the 'main' function in gui.py
            'gui_node = gui.gui:main',
            'generator_mode = gui.generator_mode:main',
            'generator_mode_welding = gui.generator_mode_welding:main',
            'fault_injector = gui.fault_injector:main',
        ],
    },
)