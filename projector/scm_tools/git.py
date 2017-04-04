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

"""Git SCM tool defintion."""

from voluptuous import All, Length, Required, Url

from projector.scm_tools.base import SCMTool


class GitSCMTool(SCMTool):
    """The Git SCM tool."""

    name = 'git'

    repository_schema = {
        Required('url'): Url(),
        'ref': str,
        'detach': bool,
        'remotes': All(Length(min=1), {
            str: Url(),
        }),
    }
