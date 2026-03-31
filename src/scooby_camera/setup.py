from setuptools import setup, find_packages

package_name = 'scooby_camera'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Giulio Vestri',
    maintainer_email='g.vestri2904@gmail.com',
    description='ROS2 package to publish Raspberry Pi camera images for Scooby Bot.',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'camera_publisher = scooby_camera.camera_publisher:main',
        ],
    },
)
