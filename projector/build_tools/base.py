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

"""Projector build tool base class."""

from ruamel.yaml.comments import CommentedMap


class BuildTool:
    """The base build tool class."""

    #: The build tool name.
    #:
    #: This must be unique.
    tool_name = None

    @classmethod
    def validate_options(cls, options: CommentedMap):
        """Validate the options.

        Args:
            options: The build tool-specific options.

        Raises:
            projector.config.ValidationError:
                Raised when the configuration is invalid.
        """
        pass