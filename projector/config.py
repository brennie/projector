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

"""Projector configuration."""

from pathlib import Path

from marshmallow import Schema, ValidationError, fields, validates_schema

from projector.scm_tools import get_scm_tools


class PathField(fields.String):
    """A field that deserializes into a :py:class:`~pathlib.path`."""

    def _deserialize(self, value, attr, obj) -> Path:
        return Path(super()._deserialize(value, attr, obj))

    def _serialize(self, value, attr, obj) -> str:
        return super()._serialize(str(value), attr, obj)


class DirectoriesSchema(Schema):
    """The schema for the directories section."""

    source = PathField(required=True)


class RepositorySchema(Schema):
    """A schema representing a single repository."""

    scm = fields.String(required=True)
    config = fields.Dict(required=True)

    @validates_schema
    def _validate_scm(self, data):
        """Validate the given SCM is known and its config is valid.

        Raises:
            marshmallow.exceptions.ValidationError:
                Either the SCM is not registered or the configuration section is invalid.
        """
        scm_name = data["scm"]

        try:
            scm = get_scm_tools()[scm_name]
        except KeyError:
            raise ValidationError(f"Unknown SCM: `{scm_name}'", field_names=("scm",))

        if scm_name != "Git":
            assert False

        data["config"] = scm.schema().load(data["config"])


class ConfigSchema(Schema):
    """A schema representing the entirety of the configuration."""

    directories = fields.Nested(DirectoriesSchema, required=True)
    repositories = fields.Dict(
        required=True, keys=fields.String(), values=fields.Nested(RepositorySchema)
    )
