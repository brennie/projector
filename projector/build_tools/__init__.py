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

"""Projector build tools."""

from functools import lru_cache
from pkg_resources import iter_entry_points
from typing import List

from projector.build_tools.base import BuildTool


@lru_cache(None)
def get_build_tools() -> List[BuildTool]:
    """Return the registered build tools.

    Build tools are registered with the ``projector.build_tools`` entry point.

    Returns:
        The registered build tools.
    """
    tools = []
    for entry_point in iter_entry_points(group='projector.build_tools'):
        tools.append(entry_point.load())

    return tools
