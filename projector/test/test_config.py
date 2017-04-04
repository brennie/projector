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

"""Projector configuration validation tests."""

from functools import partial
from itertools import takewhile
from operator import eq

import pytest
import ruamel.yaml as yaml
import voluptuous.error

from projector.config import validate_config


def _dedent(s: str) -> str:
    """Dedent the string by the number of leading spaces on the first line.

    This is a convenience function so that configurations can be included in
    tests in a cleaner fashion.
    """
    lines = s.splitlines(keepends=True)
    leading_spaces = takewhile(partial(eq, ' '), lines[0])

    # We can't directly take the length of the generator and converting to a
    # list will waste memory unnecessarily.
    dedent = sum(1 for _ in leading_spaces)
    return ''.join(line[dedent:] for line in lines)


def test_validate_config_valid():
    """Testing validate_config with a valid configuration."""
    config = yaml.load(_dedent('''\
        ---
        options:
          source_dir: ~/src
          project_dir: ~/projects
          tools: {}
        repositories: {}
        projects: {}'''), yaml.RoundTripLoader)

    validate_config(config)


def test_validate_config_missing_key():
    """Testing validate_config with missing required keys."""
    configs = map(_dedent, (
        '''\
        ---
        options: {}
        repositories: {}
        ''',
        '''\
        ---
        options: {}
        projects: {}
        ''',
        '''\
        ---
        repositories: {}
        projects: {}
        ''',
        '''\
        ---
        options: {}
        repositories: {}
        projects: {}
        ''',
    ))

    for config in configs:
        config = yaml.load(config, yaml.RoundTripLoader)

        with pytest.raises(voluptuous.error.MultipleInvalid) as excinfo:
            validate_config(config)

        for e in excinfo.value.errors:
            assert isinstance(e, voluptuous.error.RequiredFieldInvalid)


def test_validate_config_unknown_key():
    """Testing validate_config with unknown keys."""
    configs = map(_dedent, (
        '''\
        ---
        options:
          source_dir: ~/src
          project_dir: ~/projects
          tools: {}
        repositories: {}
        projects: {}
        unknown: foo
        ''',
        '''\
        options:
          source_dir: ~/src
          project_dir: ~/projects
          tools: {}
          unknown: foo
        repositories: {}
        projects: {}
        ''',
    ))

    for config in configs:
        config = yaml.load(config, yaml.RoundTripLoader)

        with pytest.raises(voluptuous.error.MultipleInvalid):
            validate_config(config)


def test_validate_config_unknown_tool():
    """Testing validate_config with unknown build tool."""
    config = yaml.load(_dedent('''\
        ---
        options:
          source_dir: ~/src
          project_dir: ~/projects
          tools:
            unknown_tool: {}
        repositories: {}
        projects: {}
        '''), yaml.RoundTripLoader)

    with pytest.raises(voluptuous.error.MultipleInvalid):
        validate_config(config)


def test_validate_config_python_tool_valid():
    """Testing validate_config with a valid PythonTool configuration."""
    config = yaml.load(_dedent('''\
        ---
        options:
          source_dir: ~/src
          project_dir: ~/projects
          tools:
            python:
              virtualenvs:
                venv2: {python: '2'}
                venv3: {python: '3'}
        repositories: {}
        projects: {}
        '''), yaml.RoundTripLoader)

    validate_config(config)


def test_validate_config_python_tool_invalid_numeric_version():
    """Testing validate_config with an invalid PythonTool configuration with numeric point Python versions."""
    config = yaml.load(_dedent('''\
        ---
        options:
          source_dir: ~/src
          project_dir: ~/projects
          tools:
            python:
              virtualenvs:
                venv2: {python: 2}
                venv3: {python: 3.4}
        repositories: {}
        projects: {}
        '''), yaml.RoundTripLoader)

    with pytest.raises(voluptuous.error.MultipleInvalid) as excinfo:
        validate_config(config)

    for error in excinfo.value.errors:
        assert isinstance(error, voluptuous.error.TypeInvalid)


def test_validate_config_invalid_repo_scm():
    """Testing validate_config with an invalid repository SCM tool."""
    config = yaml.load(_dedent('''\
        ---
        options:
          source_dir: ~/src
          project_dir: ~/projects
        repositories:
          repo1:
            scm: invalid
        '''), yaml.RoundTripLoader)

    with pytest.raises(voluptuous.error.MultipleInvalid):
        validate_config(config)


def test_validate_config_repo_git_scm():
    """Testing validate_config with a valid git repository configuration."""
    config = yaml.load(_dedent('''\
        ---
        options:
          source_dir: ~/src
          project_dir: ~/projects
        repositories:
          repo1:
            scm: git
            url: ssh://git@example.com:foo/bar.git
            ref: development
            detach: true
            remotes:
              clone: ssh://git@example.com:foo-clone/bar.git
        projects: {}
        '''), yaml.RoundTripLoader)

    validate_config(config)
