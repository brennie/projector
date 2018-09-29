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
from pprint import pprint
from types import SimpleNamespace

import click
import ruamel.yaml as yaml
import voluptuous.error
from ruamel.yaml.error import YAMLError

from projector import get_version_string
from projector.scm_tools import get_scm_tools
from projector.scm_tools.base import RepositoryError
from projector.config import validate_config


@click.group('projector')
@click.version_option(version=get_version_string())
@click.option('config_path', '-c', '--config', metavar='FILE', type=Path,
              default='~/.projector.yaml',
              help='The path to the configuration file.')
@click.pass_context
def cli(ctx, config_path):
    """Projector.

    A tool for managing multiple repositories and setting up development
    environments.
    """
    config_path = config_path.expanduser().resolve()

    ctx.obj = SimpleNamespace()
    ctx.obj.config_path = config_path

    try:
        with config_path.open() as f:
            config = yaml.load(f, yaml.RoundTripLoader)
    except IOError as e:
        click.echo(f'projector: could not open "{config_path}": {e}', err=True)
        raise SystemExit(1)
    except YAMLError as e:
        click.echo(f'projector: could not parse "{config_path}": {e}', err=True)
        raise SystemExit(1)

    try:
        validate_config(config)
    except voluptuous.error.Invalid as e:
        click.echo(f'projector: could not parse "{config_path}": {e}', err=True)
        raise SystemExit(1)

    ctx.obj.config = config


@cli.command('dump-config')
@click.pass_context
def dump_config(ctx):
    """Dump configuration to standard output."""
    pprint(ctx.obj.config)


@cli.command()
@click.option('all_repos', '-a', '--all', is_flag=True,
              help='Clone all repositories.')
@click.argument('repo_name', metavar='REPOSITORY', required=False, default=None)
@click.pass_context
def clone(ctx, all_repos, repo_name):
    """Clone a configured repository."""
    if all_repos and repo_name:
        click.echo('projector: can only specify one of --all and REPOSITORY', err=True)
        raise SystemExit(1)
    elif not all_repos and not repo_name:
        click.echo(ctx.get_help())
        raise SystemExit(0)

    config = ctx.obj.config
    config_repos = config['repositories']
    source_dir = Path(config['source_dir']).expanduser().resolve()

    if all_repos:
        to_clone = config_repos
    elif repo_name in config_repos:
        to_clone = [repo_name]
    else:
        click.echo(f'projector: unknown repository "{repo_name}"', err=True)
        raise SystemExit(1)

    for repo_name in to_clone:
        repo = config_repos[repo_name]
        scm = repo['scm']

        tool = get_scm_tools()[scm]
        checkout_path = source_dir.joinpath(*repo_name.split('/'))

        if not checkout_path.exists():
            checkout_path.mkdir(0o755, parents=True, exist_ok=True)
        elif not checkout_path.is_dir():
            click.echo(f'projector: cannot checkout {repo_name}: "{checkout_path}" exists but is not directory',
                       err=True)
            continue

        try:
            tool.checkout(checkout_path, repo)
        except RepositoryError as e:
            click.echo(f'projector: {e}', err=True)
            continue


@cli.command()
@click.pass_context
def sync(ctx):
    """Synchronize project state.

    This command will fetch any unfetched repositories and create any uncreated
    projects or branches.
    """
    raise NotImplementedError


@cli.command('import')
@click.argument('file_name', metavar='FILENAME', type=Path)
@click.argument('project_name', metavar='[PROJECT]')
@click.pass_context
def import_project(ctx):
    """Import project(s) from a configuration file.

    Unless a project name is specified, all projects from the configuration
    file will be imported.
    """
    raise NotImplementedError


@cli.command()
@click.argument('project_name', metavar='PROJECT')
@click.option('output_file_name', '-o', metavar='FILE', type=Path,
              help='Output to specified file instead of standard output.')
@click.pass_context
def export(ctx):
    """Export project(s) to a configuration file.

    By default this will write to standard output.
    """
    raise NotImplementedError


if __name__ == '__main__':
    cli()
