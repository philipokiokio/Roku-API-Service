from fastapi import APIRouter, status, Depends
from src.workspace.workspace_service import workspace_service
from src.workspace import schemas
from src.auth.oauth import get_current_user
from src.auth.models import User


workspace_router = APIRouter(prefix="/api/v1/workspace", tags={"workspace"})


@workspace_router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MessageWorkspaceResp,
)
def create_workspace(
    create_workspace: schemas.WorkspaceCreate,
    current_user: User = Depends(get_current_user),
):

    resp = workspace_service.create_workspace(current_user.id, create_workspace)

    return resp


@workspace_router.get(
    "s/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageListWorkspaceResp,
)
def get_workspaces(current_user: User = Depends(get_current_user)):

    resp = workspace_service.get_user_workspace(current_user.id)

    return resp


@workspace_router.get(
    "/{workspace_slug}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageWorkspaceResp,
)
def get_workspace(workspace_slug: str, current_user: User = Depends(get_current_user)):

    resp = workspace_service.get_workspace(workspace_slug)

    return resp


@workspace_router.patch(
    "/{workspace_slug}/update/",
    response_model=schemas.MessageWorkspaceResp,
    status_code=status.HTTP_200_OK,
)
def workspace_update(
    workspace_slug: str,
    update_workspace: schemas.workspaceUpdate,
    current_user: User = Depends(get_current_user),
):

    resp = workspace_service.update_workspace(workspace_slug, update_workspace)

    return resp


@workspace_router.delete(
    "/{workspace_slug}/delete/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def workspace_delete(
    workspace_slug: str, current_user: User = Depends(get_current_user)
):

    workspace_service.delete_workspace(workspace_slug)

    return {"status": status.HTTP_204_NO_CONTENT}


@workspace_router.post(
    "/{workspace_slug}/invite-link/gen/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageWorkspaceResp,
)
def generate_workspace_invite_link(
    workspace_slug: str,
    role_data: schemas.UpdateWorkspaceMember,
    current_user: User = Depends(get_current_user),
):

    resp = workspace_service.workspace_link_invite(workspace_slug, role_data.role)

    return resp


@workspace_router.post(
    "/{workspace_slug}/revoke-link/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageWorkspaceResp,
)
def revoke_workspace(
    workspace_slug: str, current_user: User = Depends(get_current_user)
):

    resp = workspace_service.revoke_workspace_link(workspace_slug)
    return resp


@workspace_router.post(
    "/join/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageWorkspaceMembResp,
)
def workspace_member_join(
    token: str, role_token: str, new_workspace_member: schemas.JoinWorkspace
):

    resp = workspace_service.join_workspace(token, role_token, new_workspace_member)

    return resp


@workspace_router.get(
    "/{workspace_slug}/member/{member_id}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageWorkspaceMembResp,
)
def get_workspace_member(
    workspace_slug: str, member_id: int, current_user: User = Depends(get_current_user)
):

    resp = workspace_service.get_workspace_member(member_id, workspace_slug)

    return resp


@workspace_router.get(
    "/{workspace_slug}/members/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageListWorkspaceMemResp,
)
def get_workspace_members(
    workspace_slug: str, current_user: User = Depends(get_current_user)
):

    resp = workspace_service.get_all_workspace_member(workspace_slug)

    return resp


@workspace_router.patch(
    "/{workspace_slug}/member/{member_id}/update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageWorkspaceMembResp,
)
def update_workspace_member(
    workspace_slug: str,
    member_id: int,
    update_workspace_member: schemas.JoinWorkspace,
    current_user: User = Depends(get_current_user),
):
    resp = workspace_service.update_workspace_member(
        workspace_slug, member_id, update_workspace_member
    )

    return resp


@workspace_router.delete(
    "/{workspace_slug}/member/{member_id}/delete/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workspace_member(
    workspace_slug: str, member_id: int, current_user: User = Depends(get_current_user)
):

    workspace_service.delete_workspace_member(workspace_slug, member_id)

    return {"status": status.HTTP_204_NO_CONTENT}
