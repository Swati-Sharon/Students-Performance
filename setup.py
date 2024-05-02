from setuptools import find_packages,setup
from typing import List


#to avoid -e in requirement
HYPHEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    """This function will return the list of requirements of the library that is needed in the project"""
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[i.replace("\n","")for i in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
name='mlproject',
version='0.0.1',
author='Sharon',
author_email='swatihansda05@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
     
)