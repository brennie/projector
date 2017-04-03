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

"""Projector configuration validation."""

from ruamel.yaml.comments import CommentedMap
from voluptuous import All, Length, Required, Schema

from projector.build_tools import get_build_tools


def validate_config(config: CommentedMap):
    """Validate the configuration.

    Args:
        config: The configuration to validate.

    Raises:
        voluptuous.error.Invalid:
            Raised when the configuration is invalid.
    """
    schema = Schema({
        Required('options'): {
            Required('project_dir'): All(str, Length(min=1)),
            Required('source_dir'): All(str, Length(min=1)),
            'tools': {
                tool.name: tool.options_schema
                for tool in get_build_tools()
                if tool.options_schema is not None
            },
        },
        Required('repositories'): {},
        Required('projects'): {},
    })

    schema(config)
