from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    Returns list of requirements from requirements.txt
    """
    requirement_list: List[str] = []
    
    try:
        with open("requirements.txt", "r", encoding="utf-8") as file:
            for line in file:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        raise FileNotFoundError("requirements.txt not found. Please add it before installing.")
    
    return requirement_list

setup(
    name="AI-TRAVEL-PLANNER",
    version="0.0.1",
    author="SAMEER MISHRA",
    author_email="sameermishra280202@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
