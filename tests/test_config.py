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

"""Tests for projector.config."""

import pytest
from kgb import spy_on
from marshmallow import ValidationError

from projector.config import ConfigSchema
from projector.scm_tools.git import Git
from projector.scm_tools import _get_scm_tools_uncached, get_scm_tools


def test_config_schema():
    scm_tools = {"Git": Git}

    schema = ConfigSchema()

    try:
        with spy_on(_get_scm_tools_uncached, call_fake=lambda: scm_tools):
            with pytest.raises(ValidationError) as excinfo:
                schema.load({})

            assert excinfo.value.messages == {"repositories": ["Missing data for required field."]}

            with pytest.raises(ValidationError) as excinfo:
                schema.load({"repositories": {"my-repo": {"scm": "unknown-scm"}}})

            assert excinfo.value.messages == {
                "repositories": {
                    "my-repo": {"value": {"config": ["Missing data for required field."]}}
                }
            }

            with pytest.raises(ValidationError) as excinfo:
                schema.load({"repositories": {"my-repo": {"scm": "unknown-scm", "config": {}}}})
            assert excinfo.value.messages == {
                "repositories": {"my-repo": {"value": {"scm": ["Unknown SCM: `unknown-scm'"]}}}
            }

            assert schema.load({"repositories": {}}) == {"repositories": {}}

            assert schema.load(
                {
                    "repositories": {
                        "projector": {
                            "scm": "Git",
                            "config": {
                                "remotes": {
                                    "origin": {"url": "git@github.com:brennie/projector.git"}
                                }
                            },
                        }
                    }
                }
            ) == {
                "repositories": {
                    "projector": {
                        "scm": "Git",
                        "config": {
                            "ref": "master",
                            "detach": False,
                            "remotes": {
                                "origin": {
                                    "url": "git@github.com:brennie/projector.git",
                                    "default": True,
                                }
                            },
                        },
                    }
                }
            }
    finally:
        get_scm_tools.cache_clear()
