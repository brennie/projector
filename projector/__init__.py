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

"""Projector versioning data types.

See Also:
    https://www.python.org/dev/peps/pep-0440/:
        The PEP outlining Python package versions.

"""

from enum import Enum
from typing import Optional, NamedTuple


class ReleaseKind(Enum):
    """The kind of release this is."""

    #: An alpha release.
    ALPHA = "a"

    #: A beta release.
    BETA = "b"

    #: A release candidate.
    RELEASE_CANDIDATE = "rc"

    #: A development release.
    DEV = "dev"


class Release(NamedTuple):
    """Release information."""

    #: The kind of release this is.
    kind: ReleaseKind

    #: The release number.
    n: int

    def __str__(self) -> str:
        return f"{self.kind.value}{self.n}"


class Version(NamedTuple):
    """Version information."""

    #: The major version.
    #:
    #: This is ``X`` in ``X.Y.Z``.
    major: int

    #: The minor version.
    #:
    #: This is ``Y`` in ``X.Y.Z``.
    minor: int

    #: The patch numner.
    #:
    #: This is ``Z`` in ``X.Y.Z``.
    patch: int

    #: The release information.
    #:
    #: This will be ``None`` if and only if it is a released version.
    release: Optional[Release]

    def __str__(self) -> str:
        s = f"{self.major}.{self.minor}.{self.patch}"

        if self.release is not None:
            s = f"{s}.{self.release}"

        return s

    def to_short(self) -> str:
        """Return a short (``X.Y``) version string."""
        return f"{self.major}.{self.minor}"


#: The current version of this package.
VERSION = Version(major=0, minor=1, patch=0, release=Release(kind=ReleaseKind.DEV, n=0))

#: The PEP 484 version string of this package.
__version__ = str(VERSION)
