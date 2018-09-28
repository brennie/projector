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

"""Custom marshmallow fields for Projector."""

from pathlib import Path
from typing import Any, Dict, Type

from marshmallow import ValidationError, fields


class EitherField(fields.Field):
    """A polymorphic field whose contents can be one of any number of fields."""

    def __init__(self, fields: Dict[Type, fields.Field], **kwargs):
        """Initialize the field.

        Args:
            fields:
                A mapping of result types to field types.

                The ordering of this dictionary is **important**, as deserialization will be
                attempted in the order the fields are provided.

                If a value would parse as valid for multiple fields, only the first field that
                matches will be used.
        """
        super().__init__(**kwargs)

        self._fields = fields

    def _deserialize(self, value, attr, obj) -> Any:
        field = self._fields.get(type(value))
        if field is not None:
            return field._deserialize(value, attr, obj)
        else:
            for field_type, field in self._fields.items():
                if isinstance(value, field_type):
                    return field._deserialize(value, attr, obj)

        self.fail("validator_failed")

    def _serialize(self, value, attr, obj) -> Any:
        field = self._fields.get(type(value))
        if field is not None:
            return field._serialize(value, attr, obj)
        else:
            for field_type, field in self._fields.items():
                if isinstance(value, field_type):
                    return field._serialize(value, attr, obj)

        types = ", ".join(self._fields.keys())
        raise ValidationError(f"Expected type to be one of {types} but got {type(value)} instead.")


class PathField(fields.String):
    """A field that deserializes into a :py:class:`~pathlib.path`."""

    def _deserialize(self, value, attr, obj) -> Path:
        return Path(super()._deserialize(value, attr, obj))

    def _serialize(self, value, attr, obj) -> str:
        return super()._serialize(str(value), attr, obj)
