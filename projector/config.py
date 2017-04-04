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

from copy import copy

import voluptuous
import voluptuous.error
from ruamel.yaml.comments import CommentedMap
from voluptuous import All, Length, Required, Schema

from projector.build_tools import get_build_tools
from projector.scm_tools import get_scm_tools


def _validate_scm(scm_name: str) -> str:
    """Validate an SCM name.

    The SCM must be a registered under the ``projector.scm_tools`` entry point.

    Returns:
        The SCM name.

    Raises:
        voluptuous.error.Invalid:
            Raised when an unknown SCM tool is encountered.
    """
    try:
        get_scm_tools()[scm_name]
    except KeyError:
        raise voluptuous.error.Invalid(f'unknown SCM tool: "{scm_name}"', ['scm'])

    return scm_name


def _validate_repository(repo: CommentedMap) -> CommentedMap:
    """Validate a repository entry.

    Args:
        repo:
            The repository configuration.

    Returns:
        The configuration.

    Raises:
        voluptuous.error.Invalid:
            Raised when the repository configuration is invalid.
    """
    tool = get_scm_tools()[repo['scm']]
    schema = copy(tool.repository_schema)
    schema[Required('scm')] = tool.name

    Schema(schema)(repo)

    return repo


_schema = Schema({
    Required('options'): {
        Required('project_dir'): All(str, Length(min=1)),
        Required('source_dir'): All(str, Length(min=1)),
        'tools': {
            tool.name: tool.options_schema
            for tool in get_build_tools()
            if tool.options_schema is not None
        },
    },
    Required('repositories'): {
        str: All(
            Schema({Required('scm'): All(str, _validate_scm)},
                   extra=voluptuous.ALLOW_EXTRA),
            _validate_repository,
        ),
    },
    Required('projects'): {},
})


def validate_config(config: CommentedMap):
    """Validate the configuration.

    Args:
        config: The configuration to validate.

    Raises:
        voluptuous.error.Invalid:
            Raised when the configuration is invalid.
    """
    _schema(config)
