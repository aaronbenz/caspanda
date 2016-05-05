from setuptools import setup
from setuptools import find_packages


setup(
    name='caspanda',
    version='0.0.0.4',
    packages=find_packages(),
    install_requires=[
        'cassandra-driver',
        'numpy',
        'pandas',
        'nose',
        'blist',
    ],
    url='',
    license='MIT',
    author='Aaron Benz',
    author_email='aaron.benz@accenture.com',
    description='Cassandra Wrapper for Easy Panda DataFrame Access',
    include_package_data=True,
)
