from setuptools import setup, find_packages

setup(
    name='RASErrorDetection',
    version='0.1',
    description='Detect error in Activity Daily Living',
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ],
    url='https://github.com/WSU-RAS/ras-error-detection',
    author='Gabriel V. de la Cruz Jr.',
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'pyqt5',
        'pytest',
        'coloredlogs'
    ],
    include_package_data=True
)
