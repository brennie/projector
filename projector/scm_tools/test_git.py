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

"""Tests for projector.scm_tools.git."""

import pytest
from marshmallow import ValidationError

from projector.scm_tools.git import GitRepositorySchema


def test_git_repository_schema():
    schema = GitRepositorySchema()

    assert schema.load({"remotes": {"origin": {"url": "https://example.com/foo.git"}}}) == {
        "ref": "master",
        "detach": False,
        "remotes": {"origin": {"url": "https://example.com/foo.git", "default": True}},
    }

    assert schema.load(
        {
            "remotes": {
                "origin": {"url": "https://example.com/foo.git"},
                "fork": {"url": "http://example.com/bar.git"},
            }
        }
    ) == {
        "ref": "master",
        "detach": False,
        "remotes": {
            "origin": {"url": "https://example.com/foo.git", "default": True},
            "fork": {"url": "http://example.com/bar.git", "default": False},
        },
    }

    assert schema.load({"remotes": {"my-remote": {"url": "https://example.com/bar.git"}}}) == {
        "ref": "master",
        "detach": False,
        "remotes": {"my-remote": {"url": "https://example.com/bar.git", "default": True}},
    }

    assert schema.load(
        {
            "remotes": {
                "origin": {"url": "https://example.com/foo.git"},
                "fork": {"url": "http://example.com/bar.git", "default": True},
            }
        }
    ) == {
        "ref": "master",
        "detach": False,
        "remotes": {
            "origin": {"url": "https://example.com/foo.git", "default": False},
            "fork": {"url": "http://example.com/bar.git", "default": True},
        },
    }

    assert schema.load(
        {
            "ref": "release-1.x",
            "detach": True,
            "remotes": {"origin": {"url": "git@example.com:foo.git", "default": True}},
        }
    ) == {
        "ref": "release-1.x",
        "detach": True,
        "remotes": {"origin": {"url": "git@example.com:foo.git", "default": True}},
    }

    with pytest.raises(ValidationError) as excinfo:
        schema.load({})
    assert excinfo.value.messages == {"remotes": ["Missing data for required field."]}

    with pytest.raises(ValidationError) as excinfo:
        schema.load({"remotes": {}})
    assert excinfo.value.messages == {"_schema": ["Repository has no remotes."]}

    with pytest.raises(ValidationError) as excinfo:
        schema.load(
            {
                "remotes": {
                    "upstream": {"url": "https://example.com/upstream.git"},
                    "fork": {"url": "https://example.com/downstream.git"},
                }
            }
        )
    assert excinfo.value.messages == {"_schema": ["Repository has no default remote."]}

    with pytest.raises(ValidationError) as excinfo:
        schema.load(
            {
                "remotes": {
                    "upstream": {"url": "https://example.com/upstream.git", "default": True},
                    "fork": {"url": "https://example.com/downstream.git", "default": True},
                }
            }
        )
    assert excinfo.value.messages == {
        "_schema": ["A repository cannot have multiple default remotes."]
    }

    with pytest.raises(ValidationError) as excinfo:
        schema.load({"remotes": {"origin": {}}})
    assert excinfo.value.messages == {
        "remotes": {"origin": {"value": {"url": ["Missing data for required field."]}}}
    }
