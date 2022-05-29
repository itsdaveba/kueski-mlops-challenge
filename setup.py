from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).parent.resolve()

# Required packages
with open(Path(here, 'requirements.txt')) as file:
    required_packages = [line.strip() for line in file.readlines()]

test_packages = [
    'pytest==7.1.2',
    'great-expectations==0.15.7'
]

docs_packages = [
    'mkdocs==1.3.0',
    'mkdocstrings==0.18.0'
]

setup(
    name='mlops',
    version='0.1',
    description='Kueski MLOps Challenge',
    url='https://github.com/itsdaveba/kueski-mlops-challenge',
    author='David Barragan',
    author_email='dbarragan.a@outlook.com',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=required_packages,
    extras_require={
        'test': test_packages,
        'docs': docs_packages,
        'dev': test_packages + docs_packages
    },
    entry_points={
        'console_scripts': [
            'mlops = mlops.main:app'
        ]
    }
)