import glob, os
from setuptools import find_packages, setup

package_name = 'report_one_pkg'
share_dir = 'share/' + package_name

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (share_dir, ['package.xml']),
        (share_dir + '/launch', glob.glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bird99',
    maintainer_email='bird99@todo.todo',
    keywords=['ROS'],
    description='ROS 2 rclpy example package for the topic, service, action',
    license='Apache License, Version 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'mygui = report_one_pkg.mygui:main',
            'mymode = report_one_pkg.mymode:main',
            'mymoving = report_one_pkg.mymoving:main',
        ],
    },
)
