from setuptools import setup

package_name = 'scooby_camera'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]),
                ('share/' + package_name, ['package.xml'])],
    install_requires=['setuptools', 'rclpy', 'opencv-python', 'cv_bridge'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='ROS2 package to publish Raspberry Pi camera images for Scooby Bot.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_publisher = scooby_camera.camera_publisher:main',
        ],
    },
)
