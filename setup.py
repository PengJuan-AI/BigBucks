from setuptools import find_packages, setup

setup(
    name='BigBucks',
    version='2.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)