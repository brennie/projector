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
from typing import Dict, Type

from marshmallow import ValidationError, fields


class EitherField(fields.Field):
    """A polymorphic field whose contents can be one of any number of fields."""

    def __init__(self, fields: Dict[Type, fields.Field], **kwargs):
        """Initialize the field.

        Args:
            fields:
                A mapping of result types to field types.

                The ordering of this dictionary is **important**, as (de)serialization will be
                attempted in the order the fields are provided.

                During (de)serialization, if an exact match for a type is found in ``fields``,
                that match will be used. Otherwise, each entry will be checked *in order* for
                whether it is a :py:func:`isinstance` match. That means that if a value is a
                subclass of multiple types in ``fields``, the first one that it matches will be
                used.
        """
        super().__init__(**kwargs)

        self._fields = fields

    def _deserialize(self, value, attr, obj):
        return self._serde("_deserialize", value, attr, obj)

    def _serialize(self, value, attr, obj):
        return self._serde("_serialize", value, attr, obj)

    def _serde(self, serde_method_name: str, value, attr, obj):
        """Do the actual (de)serialization.

        The implementation of serialization and deserialization is identical up to the method
        called on the matching field.
        """
        field = self._fields.get(type(value))
        if field is not None:
            return getattr(field, serde_method_name)(value, attr, obj)

        for field_type, field in self._fields.items():
            if isinstance(value, field_type):
                return getattr(field, serde_method_name)(value, attr, obj)

        types = ", ".join(t.__name__ for t in self._fields.keys())
        raise ValidationError(
            f"Expected type of value to be one of {types}; got {type(value).__name__} instead."
        )


class PathField(fields.String):
    """A field that deserializes into a :py:class:`~pathlib.path`."""

    def _deserialize(self, value, attr, obj) -> Path:
        return Path(super()._deserialize(value, attr, obj))

    def _serialize(self, value, attr, obj) -> str:
        return super()._serialize(str(value), attr, obj)
