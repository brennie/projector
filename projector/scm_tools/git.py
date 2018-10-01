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

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Union

from marshmallow import Schema, ValidationError, fields, post_load, pre_dump, validate
from more_itertools import ilen

from projector.fields import EitherField
from projector.scm_tools.base import ScmTool


class RemoteKind(Enum):
    """The kind of remote, either implicit or explicit.

    Implicit remotes contain just the URL, while explicit remotes contain key-value pairs.
    """

    IMPLICIT = "implicit"
    EXPLICIT = "explicit"


@dataclass
class Remote:
    """A Git remote.

    See Also:
        :py:class:`RemoteKind`:
            A description of the kinds of remotes.
    """

    #: The kind of remote this is.
    kind: RemoteKind

    #: The contents of this remote.
    inner: Union[str, Dict[str, Any]]

    #: Whether or not the remote is the default.
    #:
    #: This is only used by :py:attr:`implicit <RemoteKind.IMPLICIT>` remotes, since they
    #: otherwise would not have a location to store their status as a default.
    #:
    #: This value is not serialized.
    _default: bool = False

    @classmethod
    def from_raw(cls, value: Union[str, Dict[str, Any]]) -> "Remote":
        """Create a remote from a raw value.

        Returns:
            Remote:
            The created remote.
        """
        kind = RemoteKind.IMPLICIT if isinstance(value, str) else RemoteKind.EXPLICIT

        return cls(kind=kind, inner=value)

    @property
    def url(self):
        if self.kind == RemoteKind.IMPLICIT:
            return self.inner
        elif self.kind == RemoteKind.EXPLICIT:
            return self.inner["url"]

    @url.setter
    def url(self, value: str):
        if self.kind == RemoteKind.IMPLICIT:
            self.inner = value
        elif self.kind == RemoteKind.EXPLICIT:
            self.inner["url"] = value

    @property
    def default(self) -> bool:
        if self.kind == RemoteKind.IMPLICIT:
            return self._default
        elif self.kind == RemoteKind.EXPLICIT:
            return self.inner["default"]

    @default.setter
    def default(self, value: bool):
        if self.kind == RemoteKind.IMPLICIT:
            self._default = value
        elif self.kind == RemoteKind.EXPLICIT:
            self.inner["default"] = value


class GitRemoteSchema(Schema):
    """The schema for a Git remote."""

    url = fields.String(required=True)
    default = fields.Boolean(missing=False)


class GitRepositorySchema(Schema):
    """The schema for a Git repository."""

    ref = fields.String(missing="master")
    detach = fields.Boolean(missing=False)
    remotes = fields.Dict(
        required=True,
        keys=fields.String(),
        values=EitherField({dict: fields.Nested(GitRemoteSchema), str: fields.String()}),
        validate=validate.Length(min=1, error="Repository has no remotes."),
    )

    @post_load
    def _post_load(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Pre-process remotes into Remote objects."""
        remotes = {
            remote_name: Remote.from_raw(remote) for remote_name, remote in data["remotes"].items()
        }

        default_count = ilen(1 for remote in remotes.values() if remote.default)

        if default_count == 0:
            if len(remotes) == 1:
                default_remote = next(iter(remotes))
            elif "origin" in remotes:
                default_remote = "origin"
            else:
                default_remote = None

            if default_remote:
                remotes[default_remote].default = True
            else:
                raise ValidationError("Repository has no default remote.", field_names="remotes")
        elif default_count > 1:
            raise ValidationError(
                "A repository cannot have multiple default remotes.", field_names="remotes"
            )

        return {"remotes": remotes, "ref": data["ref"], "detach": data["detach"]}

    @pre_dump
    def _pre_dump(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Unwrap remotes into their raw representation prior to serialization."""
        return {
            "ref": data["ref"],
            "detach": data["detach"],
            "remotes": {
                remote_name: remote.inner for remote_name, remote in data["remotes"].items()
            },
        }


class Git(ScmTool):
    """The Git SCM."""

    name = "Git"
    schema = GitRepositorySchema
