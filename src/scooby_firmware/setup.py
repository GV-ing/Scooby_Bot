from setuptools import setup, find_packages

package_name = 'scooby_firmware'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Giulio Vestri',
    maintainer_email='g.vestri2904@gmail.com',
    description='Bridge seriale per il controllo motori di Scooby-Bot via Arduino',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'serial_bridge = scooby_firmware.serial_bridge:main'
        ],
    },
)
