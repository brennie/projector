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

"""Base SCM tool definition."""

from typing import Any, Dict, Union

from voluptuous import Schema


class SCMTool:
    """The abstract base class for SCMTools.

    Subclasses of this represent a specific SCM tool such as :py:class:`git
    <projector.scm_tools.git:GitSCMTool>`.
    """

    #: The name of the tool.
    name: str = None

    #: The schema for repository entries.
    repository_schema: Union[Dict[Any, Any], Schema] = None
