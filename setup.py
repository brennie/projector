"""Package setup for projector."""

import os
from codecs import open
from setuptools import setup, find_packages

from projector import get_version_string


pkg_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(pkg_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='projector',
    version=get_version_string(),
    description='A tool for managing multiple repositories and setting up development environments.',
    long_description=long_description,
    author='Barret Rennie',
    author_email='barret@brennie.ca',
    license='GPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Langauge :: Python :: 3',
    ],
    keywords='development project repository setuptools',
    packages=find_packages(exclude=['contrib', 'docs', 'test']),
    install_requires=[
        'click>=6,<7',
        'ruamel.yaml',
        'voluptuous',
    ],
    extras_require={
        'dev': [
            'flake8',
            'flake8-bugbear',
            'flake8-commas',
            'flake8-docstrings',
            'pytest',
            'wheel',
        ],
    },
    entry_points={
        'console_scripts': [
            'projector = projector.cli:cli',
        ],
        'projector.build_tools': [
            'python = projector.build_tools.python:PythonBuildTool',
        ],
        'projector.scm_tools': [
            'git = projector.scm_tools.git:GitSCMTool',
        ],
    },
)
