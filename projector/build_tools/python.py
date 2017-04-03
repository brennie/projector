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

from ruamel.yaml.comments import CommentedMap

from projector.build_tools.base import BuildTool
from projector.config import ValidationError


class PythonBuildTool(BuildTool):
    """The Python build tool.

    The Python build tool uses ``pew`` to create virtual environemnts.
    """

    name = 'python'

    @classmethod
    def validate_options(cls, options: CommentedMap):
        """Validate the Python build tool options."""
        unknown_keys = set(options) - {'virtualenvs'}

        if unknown_keys:
            key = unknown_keys.pop()
            raise ValidationError(f'Unknown key "options.tools.python.{key}".',
                                  code='unknown-key')

        virtualenvs = options.get('virtualenvs')

        if virtualenvs:
            if not isinstance(virtualenvs, CommentedMap):
                raise ValidationError('Key "options.tools.python.virtualenvs" should be a map.',
                                      code='invalid-key')

            for venv_name, venv_options in virtualenvs.items():
                if not isinstance(venv_options, CommentedMap):
                    raise ValidationError(f'Key "options.tools.python.virtualenvs.{venv_name}" should be a map.',
                                          code='invalid-key')

                unknown_keys = set(venv_options) - {'python'}

                if unknown_keys:
                    key = unknown_keys.pop()
                    raise ValidationError(f'Unknown key "options.tools.python.{venv_name}.{key}".',
                                          code='unknown-key')

                python_version = venv_options.get('python')

                if not python_version:
                    raise ValidationError(f'Expected key "options.tools.python.{venv_name}.python was missing.',
                                          code='missing-key')
