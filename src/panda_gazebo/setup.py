from setuptools import setup

setup(
    name='panda_gazebo',
    version='2.7.8',
    packages=['panda_gazebo', 'panda_gazebo.common', 'panda_gazebo.core'],
    package_dir={'': 'src'},
)
