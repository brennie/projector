# projector - a tool for managing multiple repositories and setting up
#             development environments.
# Copyright (C) 2018 Barret Rennie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Setup configuration for projector."""

from pathlib import Path
from setuptools import find_packages, setup

import projector

readme_path = Path(__file__).parent / "README.rst"
with readme_path.open() as f:
    long_description = f.read()

setup(
    name="projector",
    description=(
        "Projector takes the overhead out of managing your repositories and development "
        "environments."
    ),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    version=projector.__version__,
    license="GPLv3+",
    keywords="development project repository setuptools",
    packages=find_packages(exclude=("contrib", "docs", "tests")),
    author="Barret Rennie",
    author_email="barret@brennie.ca",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Software Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["marshmallow == 3.0.0b16"],
    entry_points={
        "projector.scm_tools": [
            "Git = projector.scm_tools.git.Git",
        ],
    },
    project_urls={
        "Source": "https://github.com/brennie/projector",
        "Issues": "https://github.com/brennie/projector/issues",
    },
)
