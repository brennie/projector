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

"""The projector command-line interface."""

from pathlib import Path

import click

from projector import get_version_string


@click.group('projector')
@click.version_option(version=get_version_string())
@click.option('config_path', '-c', '--config', metavar='FILE', type=Path,
              default='~/.projector.yaml',
              help='The path to the configuration file.')
def cli(config_path):
    """Projector.

    A tool for managing multiple repositories and setting up development
    environments.
    """
    raise NotImplementedError


@cli.command()
def sync():
    """Synchronize project state.

    This command will fetch any unfetched repositories and create any uncreated
    projects or branches.
    """
    raise NotImplementedError


@cli.command('import')
@click.argument('file_name', metavar='FILENAME', type=Path)
@click.argument('project_name', metavar='[PROJECT]')
def import_project():
    """Import project(s) from a configuration file.

    Unless a project name is specified, all projects from the configuration
    file will be imported.
    """
    raise NotImplementedError


@cli.command()
@click.argument('project_name', metavar='PROJECT')
@click.option('output_file_name', '-o', metavar='FILE', type=Path,
              help='Output to specified file instead of standard output.')
def export():
    """Export project(s) to a configuration file.

    By default this will write to standard output.
    """
    raise NotImplementedError


if __name__ == '__main__':
    cli()
