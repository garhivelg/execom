from setuptools import setup, find_packages
# from distutils.core import setup, find_packages
import py2exe
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, '..', 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    console=["manage.py"],
    # package_dir={'': 'src'},
    packages=find_packages('.', exclude=['tests']),        
    options={"py2exe": {
        "packages": [
            'sqlalchemy.sql',
            'jinja2',
            'faker',
        ],
        "includes": [
            "config",
        ],           
        # "path": [
        #     path.dirname(__file__),
        # ],                                     
    }},
    install_requires=requirements,
    # zipfile=None
)