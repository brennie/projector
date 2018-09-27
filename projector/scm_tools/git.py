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

"""Support for the Git SCM tool."""

from marshmallow import Schema, ValidationError, fields, validates_schema

from projector.scm_tools.base import ScmTool


class GitRemoteSchema(Schema):
    """The schema for a Git remote."""

    url = fields.String(required=True)
    default = fields.Boolean(missing=False)


class GitRepositorySchema(Schema):
    """The schema for a Git repository."""

    ref = fields.String(missing="master")
    detach = fields.Boolean(missing=False)
    remotes = fields.Dict(
        required=True, keys=fields.String(), values=fields.Nested(GitRemoteSchema)
    )

    @validates_schema
    def validate_remotes(self, data):
        """Validate the ``remotes`` field.

        Raises:
            marshmallow.exceptions.ValidationError:
                The remotes do not pass validation.
        """
        remotes = data.get("remotes")

        if remotes is None or len(remotes) == 0:
            raise ValidationError("Repository has no remotes.")

        has_default = False
        for remote in remotes.values():
            if remote.get("default", False):
                if has_default:
                    raise ValidationError("A repository cannot have multiple default remotes.")

                has_default = True

        if not has_default:
            if "origin" in remotes:
                remotes["origin"]["default"] = True

            elif len(remotes) == 1:
                remote = next(iter(remotes))
                remotes[remote]["default"] = True

            else:
                raise ValidationError("Repository has no default remote.")


class Git(ScmTool):
    """The Git SCM."""

    name = "Git"
    schema = GitRepositorySchema
