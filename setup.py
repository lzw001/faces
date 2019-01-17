from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='faces',
    version='0.1',
    author='Lukasz Ambroziak',
    description='Detect and recognize faces.',
    url='https://github.com/stasulam/faces',
    license='MIT',
    packages=['faces'],
    install_requires=requirements,
    zip_safe=True
)