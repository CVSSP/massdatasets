from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='massdatasets',
    version='0.1',
    description='Datasets for musical audio source separation.',
    author='Dominic Ward',
    author_email='dw0031@surrey.ac.uk',
    url='',
    py_modules=['massdatasets'],
    long_description=long_description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords='audio music bss',
    license='MIT',
    install_requires=[
        'pandas'
    ]
)
