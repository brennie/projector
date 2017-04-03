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

from functools import partial
from operator import add
from typing import Optional, Set

from ruamel.yaml.comments import CommentedMap

from projector.build_tools import get_build_tools


_TOP_LEVEL_KEYS = {'options', 'repositories', 'projects'}
_OPTIONS_KEYS = {'source_dir', 'project_dir', 'tools'}


class ValidationError(Exception):
    """An error that occurs with configuration validation."""

    def __init__(self, msg: str, code: Optional[str]):
        """Initialize the error.

        Args:
            msg: The exception message.
            code: A unique exception code.
        """
        super().__init__(msg)
        self.code = code


def validate_config(config: CommentedMap):
    """Validate the configuration.

    Args:
        config: The configuration to validate.

    Raises:
        ValidationError:
            Raised when the configuration is invalid.
    """
    _validate_keys(config, _TOP_LEVEL_KEYS)

    options = config['options']
    _validate_keys(options, _OPTIONS_KEYS, prefix='options.')

    tools = options.get('tools')
    if tools:
        configured_tools = set(tools)
        build_tools = get_build_tools()

        unknown_keys = configured_tools - {build_tool.name for build_tool in build_tools}

        if unknown_keys:
            key = unknown_keys.pop()
            raise ValidationError(f'Unknown build tool: "{key}"',
                                  code='unknown-tool')

        for tool in get_build_tools():
            if tool.name in tools:
                tool.validate_options(tools[tool.name])


def _validate_keys(mapping: CommentedMap, expected_keys: Set[str], *,
                   prefix: Optional[str]=None):
    """Validate that the keys present in the mapping are all expected and that none are missing.

    Args:
        mapping: The mapping to validate.
        expected_keys: The set of expected keys. All must be present in the mapping.

    """
    keys = set(mapping)
    missing_keys = expected_keys - keys
    unknown_keys = keys - expected_keys

    if unknown_keys:
        key = unknown_keys.pop()
        if prefix:
            key = f'{prefix}{key}'

        raise ValidationError(f'Unknown key "{key}"', code='unknown-key')

    if missing_keys:
        if not prefix:
            prefix = ''
        missing_keys = ', '.join(map(partial(add, prefix), missing_keys))
        raise ValidationError(f'Expected keys {missing_keys} were missing.',
                              code='missing-key')
