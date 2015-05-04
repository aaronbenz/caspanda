from setuptools import find_packages
from setuptools import setup
setup(
    name='caspanda',
    version='0.0.0.2',
    packages=find_packages(),
    install_requires=['cassandra-driver',
              'numpy',
              'pandas'],
    url='',
    license='MIT',
    author='Aaron Benz',
    author_email='aaron.benz@accenture.com',
    description='Cassandra Wrapper for Easy Panda DataFrame Access',
    include_package_data=True
)
