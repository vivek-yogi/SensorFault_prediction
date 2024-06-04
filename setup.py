from setuptools import find_packages,setup
from typing import List

def get_requirements()->list[str]:

    requirements_list : List[str] = []
    return requirements_list

setup (
    name         = 'SensorFault_prediction',
    version      = '0.0.1',
    author       = 'Vivek_yogi',
    author_email = 'vivek87yogi@gmail.com',
    packages     = find_packages(),
    install_requires = get_requirements() ,#['pymongo']
)