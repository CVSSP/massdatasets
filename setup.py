from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='massdatasets',
    version='0.1',
    description='Datasets for musical audio source separation work.',
    author='Dominic Ward',
    author_email='dw0031@surrey.ac.uk',
    url='',
    py_modules=['massdatasets'],
    long_description=long_description,
    keywords='audio music bss',
    license='MIT',
    install_requires=[
        'numpy',
        'pandas',
        'xlrd',
        'pyaml',
    ]
)
