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

"""Tests for projector.fields."""

from pathlib import Path

import pytest
from marshmallow import Schema, ValidationError, fields
from kgb import spy_on

from projector.fields import EitherField, PathField


def test_either_field():
    """Testing projector.fields.EitherField"""

    class ComplexSchema(Schema):
        foo = fields.String(required=True)
        bar = fields.String(required=True)

    class TestSchema(Schema):
        field = EitherField(
            required=True,
            fields={dict: fields.Nested(ComplexSchema), str: fields.String(required=True)},
        )

    schema = TestSchema()

    assert schema.load({"field": {"foo": "foo", "bar": "bar"}}) == {
        "field": {"foo": "foo", "bar": "bar"}
    }
    assert schema.load({"field": "some-value"}) == {"field": "some-value"}

    with pytest.raises(ValidationError) as excinfo:
        schema.load({"field": 123})

    assert excinfo.value.messages == {
        "field": ["Expected type of value to be one of dict, str; got int instead."]
    }

    with pytest.raises(ValidationError) as excinfo:
        schema.load({"field": {"foo": "foo"}})

    assert excinfo.value.messages == {"field": {"bar": ["Missing data for required field."]}}

    assert schema.dump({"field": {"foo": "foo", "bar": "bar"}}) == {
        "field": {"foo": "foo", "bar": "bar"}
    }

    assert schema.dump({"field": "foo"}) == {"field": "foo"}

    with pytest.raises(ValidationError) as excinfo:
        schema.dump({"field": 123})

    assert excinfo.value.messages == {
        "field": ["Expected type of value to be one of dict, str; got int instead."]
    }


def test_either_field_subclass():
    """Testing projector.fields.EitherField when one field type is a subclass of another"""

    class Special(int):
        pass

    class SuperSpecial(Special):
        pass

    class NotSoSpecial(int):
        pass

    int_field = fields.Raw()
    special_field = fields.Raw()

    class TestSchema(Schema):
        field = EitherField(required=True, fields={Special: special_field, int: int_field})

    schema = TestSchema()

    with spy_on(int_field._deserialize) as int_spy, spy_on(
        special_field._deserialize
    ) as special_spy:
        assert schema.load({"field": 3}) == {"field": 3}
        assert int_spy.called
        assert not special_spy.called

        int_spy.reset_calls()

        assert schema.load({"field": Special(3)}) == {"field": Special(3)}
        assert not int_spy.called
        assert special_spy.called

        special_spy.reset_calls()

        assert schema.load({"field": SuperSpecial(3)}) == {"field": SuperSpecial(3)}
        assert not int_spy.called
        assert special_spy.called

        special_spy.reset_calls()

        assert schema.load({"field": NotSoSpecial(3)}) == {"field": NotSoSpecial(3)}
        assert int_spy.called
        assert not special_spy.called

    with spy_on(int_field._serialize) as int_spy, spy_on(special_field._serialize) as special_spy:
        assert schema.dump({"field": 3}) == {"field": 3}
        assert int_spy.called
        assert not special_spy.called

        int_spy.reset_calls()

        assert schema.dump({"field": Special(3)}) == {"field": Special(3)}
        assert not int_spy.called
        assert special_spy.called

        special_spy.reset_calls()

        assert schema.dump({"field": SuperSpecial(3)}) == {"field": SuperSpecial(3)}
        assert not int_spy.called
        assert special_spy.called

        special_spy.reset_calls()

        assert schema.dump({"field": NotSoSpecial(3)}) == {"field": NotSoSpecial(3)}
        assert int_spy.called
        assert not special_spy.called


def test_path_field():
    """Testing projector.fields.PathField"""

    class TestSchema(Schema):
        field = PathField(required=True)

    schema = TestSchema()

    assert schema.load({"field": "/"}) == {"field": Path("/")}
    assert schema.load({"field": "/tmp/foo"}) == {"field": Path("/tmp/foo")}

    assert schema.dump({"field": Path("/")}) == {"field": "/"}
    assert schema.dump({"field": Path("/tmp/foo")}) == {"field": "/tmp/foo"}
