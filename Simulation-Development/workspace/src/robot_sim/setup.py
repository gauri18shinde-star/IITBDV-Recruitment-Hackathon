from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'robot_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', 'robot.gazebo'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', 'robot.urdf'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', 'colour.xacro'))),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', 'spawn_robot.launch.py'))),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', 'world.launch.py'))),
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', 'world.sdf'))),


    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gauri',
    maintainer_email='gauri@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'roam = robot_sim.roam:main',
    ],
    },
)
