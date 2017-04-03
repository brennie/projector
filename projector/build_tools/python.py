# projector - a tool for managing multiple repositories and setting up
#             development environments.
# Copyright (C) 2017 Barret Rennie
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

"""Python build tool."""

from voluptuous import Required

from projector.build_tools.base import BuildTool


class PythonBuildTool(BuildTool):
    """The Python build tool.

    The Python build tool uses ``pew`` to create virtual environemnts.
    """

    name = 'python'

    options_schema = {
        'virtualenvs': {
            str: {Required('python'): str},
        },
    }
