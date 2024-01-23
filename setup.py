# setup.py is responsible for creating machine learning applications as a package and even deploy Pypi
from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]: # here my function will return a list because requirements.txt will basically have a list of libraries
    # here in ('''...''') basically we are writing a definition
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines() # It will read the lines in the requirements.txt
        requirements=[req.replace("\n","") for req in requirements] # Replacing \n with blank

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements


setup(
    name='Student-Performance-Indicator-Project',
    version='0.0.1',
    author='Kunal Mishra',
    author_email='mishrakunal065@gmail.com',
    packages=find_packages(), # find_packages will see in how many folder we have __init__.py. Then after finding __init__.py it will consider as a package.
    install_requires=get_requirements('requirements.txt')
)
