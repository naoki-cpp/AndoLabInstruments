from setuptools import setup, find_packages

setup(
    name='AndoLabInstruments',
    version='0.1.0',
    packages=find_packages(), 
    install_requires=[
        'parse',
        'numpy',
        'pandas',
        'pyvisa',
        'pymeasure'
    ],
)
