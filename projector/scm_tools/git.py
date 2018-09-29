# projector - a tool for managing multiple repositories and setting up
#             development environments.
# Copyri    ght (C) 2017 Barret Rennie
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

"""Git SCM tool defintion."""

import subprocess
from pathlib import Path
from typing import Any, Dict, Tuple

import click
from voluptuous import All, Length, Required, Url

from projector.scm_tools.base import RepositoryError, SCMTool


class GitSCMTool(SCMTool):
    """The Git SCM tool."""

    name = 'git'

    repository_schema = {
        Required('url'): str,
        'ref': str,
        'detach': bool,
        'remotes': All(Length(min=1), {
            str: str,
        }),
    }

    @classmethod
    def _run_git(cls, *args: Tuple[Any], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                 encoding='utf-8',
                 **kwargs: Dict[str, Any]) -> subprocess.CompletedProcess:
        cmd = ['git']
        cmd.extend(map(str, args))

        return subprocess.run(cmd, stdin=stdin, stdout=stdout, stderr=stderr, encoding=encoding, **kwargs)

    @classmethod
    def checkout(cls, checkout_path: Path, config: Dict[str, Any]):
        url = config['url']
        try:
            cls._run_git('clone', url, checkout_path, check=True)
        except subprocess.CalledProcessError as e:
            raise RepositoryError(f'could not clone {url}:\n{e.stdout}') from e

        git_dir = checkout_path / '.git'
        ref = config.get('ref', 'master')
        checkout_cmd = ['--git-dir', git_dir, 'checkout', ref]
        if config.get('detach'):
            checkout_cmd.append('--detach')

        try:
            cls._run_git(*checkout_cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RepositoryError(f'could not clone checkout branch "{ref}":\n{e.stdout}') from e

        for remote_name, remote_url in config.get('remotes', {}):
            try:
                cls._run_git('--git-dir', git_dir, 'remote', 'add', remote_name, remote_url)
            except subprocess.CalledPorcessError as e:
                raise RepositoryError(f'could not add remote "{remote_name}":\n{e.stdout}') from e
