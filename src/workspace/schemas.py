from src.app.utils.base_schemas import AbstractModel, ResponseModel, RoleOptions, User
from pydantic import EmailStr
from typing import List, Optional


class WorkspaceCreate(AbstractModel):
    name: str


class WorkspaceResponse(WorkspaceCreate):
    id: int
    slug: str
    creator: User
    members: List[User] | None


class MessageWorkspaceResp(ResponseModel):
    data: WorkspaceResponse


class MessageListWorkspaceResp(ResponseModel):
    data: List[WorkspaceResponse]


class workspaceUpdate(AbstractModel):
    name: Optional[str]


class UpdateRole(AbstractModel):
    role: RoleOptions


class Workspace(AbstractModel):
    name: str
    slug: str


class WorkspaceMemberResponse(AbstractModel):
    workspace: Workspace
    user: User
    role: str


class MessageWorkspaceMembResp(ResponseModel):
    data: WorkspaceMemberResponse


class MessageListWorkspaceMemResp(ResponseModel):
    data: List[WorkspaceMemberResponse]


class JoinWorkspace(AbstractModel):
    email: EmailStr


class UpdateWorkspaceMember(AbstractModel):
    role: RoleOptions
