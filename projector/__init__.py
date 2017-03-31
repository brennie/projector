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

"""Projector package information."""

from collections import namedtuple


Version = namedtuple('Version', ('major', 'minor', 'patch', 'release'))


VERSION = Version(0, 0, 1, release=False)


def get_version_string() -> str:
    """Return the version of Projector.

    Unreleased versions will be suffixed by ``'.dev0'``.

    Returns:
        The version of projector.
    """
    version = '.'.join(map(str, VERSION[:3]))

    if not VERSION.release:
        version = f'{version}.dev0'

    return version
