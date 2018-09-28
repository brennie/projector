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

"""SCM tool utilities."""

from functools import lru_cache
from pkg_resources import iter_entry_points
from typing import Dict

from projector.scm_tools.base import ScmTool


# This really only exists so we can spy on it with kgb.
#
# We cannot spy on `get_scm_tools` becuase some Python dsitributions have a native module for the
# wrapper that lru_cache uses to wrap functions. This wrapper is not a proper function, but a C
# object.
def _get_scm_tools_uncached() -> Dict[str, ScmTool]:
    return {
        tool.name: tool
        for tool in (
            entry_point.load() for entry_point in iter_entry_points("projector.scm_tools")
        )
    }


@lru_cache(None)
def get_scm_tools() -> Dict[str, ScmTool]:
    """Return registered SCM Tools.

    Supported SCM tools are registered with the ``projector.scm_tools`` entry point. The results
    will be cached for future use.

    Returns:
        The registered SCM tools.
    """
    return _get_scm_tools_uncached()
