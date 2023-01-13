from src.workspace import schemas
from src.workspace.models import WorkspaceMember, Workspace
from fastapi import HTTPException, status
from src.workspace.workspace_repository import workspace_member_repo, workspace_repo
from fastapi.encoders import jsonable_encoder
from src.app.utils.base_schemas import RoleOptions
from src.app.utils.token import gen_token, retrieve_token
from starlette.requests import Request
from src.auth.auth_repository import user_repo


class WorkspaceService:
    def __init__(self):
        self.workspace_repo = workspace_repo
        self.workspace_member_repo = workspace_member_repo

    def orm_call(self, workspace: Workspace):

        workspace_ = jsonable_encoder(workspace)
        workspace_["creator"] = workspace.creator
        workspace_["members"] = workspace.workspace_member
        return workspace_

    def member_orm_call(self, workspace_member: WorkspaceMember):
        workspace_member_ = jsonable_encoder(workspace_member)
        workspace_member_["workspace"] = workspace_member.workspace
        workspace_member_["user"] = workspace_member.member
        return workspace_member_

    def create_workspace(
        self, user_id: int, workspace_create: schemas.WorkspaceCreate
    ) -> schemas.MessageWorkspaceResp:

        workspace_check = self.workspace_repo.check_workspace(workspace_create.name)
        if workspace_check:
            raise HTTPException(
                detail="Workspace exist", status_code=status.HTTP_409_CONFLICT
            )

        workspace_dict = workspace_create.dict()
        workspace_dict["slug"] = self.workspace_repo.slugger(workspace_create.name)
        workspace_dict["created_by"] = user_id
        workspace_dict["is_premium"] = False

        workspace = self.workspace_repo.create_workspace(workspace_dict)

        workspace_member_dict = {
            "workspace_id": workspace.id,
            "member_id": user_id,
            "role": RoleOptions.admin.value,
        }
        self.workspace_member_repo.create_workspace_member(workspace_member_dict)
        workspace = self.orm_call(workspace)
        resp = {
            "message": "Workspace Created Successfully",
            "data": workspace,
            "status": status.HTTP_201_CREATED,
        }

        return resp

    def get_workspace(self, slug: str) -> schemas.MessageWorkspaceResp:

        workspace = self.workspace_repo.get_workspace(slug)
        if not workspace:
            raise HTTPException(
                detail="Workspace does not exists",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        workspace_ = self.orm_call(workspace)
        resp = {
            "message": "Workspace Returned",
            "data": workspace_,
            "status": status.HTTP_200_OK,
        }
        return resp

    def get_user_workspace(self, user_id: int) -> schemas.MessageListWorkspaceResp:

        user_workspaces, _ = self.workspace_repo.user_workspace_count_data(user_id)
        if not user_workspaces:
            raise HTTPException(
                detail="User Does not have Workspaces",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        workspaces = []
        for user_workspace in user_workspaces:
            workspaces.append(self.orm_call(user_workspace))

        resp = {
            "message": "User Workspaces retrieved successfully",
            "data": workspaces,
            "status": status.HTTP_200_OK,
        }
        return resp

    def update_workspace(
        self, slug: str, update_workspace: schemas.workspaceUpdate
    ) -> schemas.MessageWorkspaceResp:

        workspace = self.workspace_repo.get_workspace(slug)
        if not workspace:
            raise HTTPException(
                detail="Workspace does not exists",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        workspace_update_ = update_workspace.dict()

        for key, value in workspace_update_.items():
            setattr(workspace, key, value)

        workspace = self.workspace_repo.update_workspace(workspace)

        workspace_ = self.orm_call(workspace)
        resp = {
            "message": "Workspace Updated Successfully",
            "data": workspace_,
            "status": status.HTTP_200_OK,
        }
        return resp

    def delete_workspace(self, slug: str):

        workspace = self.workspace_repo.get_workspace(slug)

        if not workspace:
            raise HTTPException(
                detail="Workspace does not exists",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        self.workspace_repo.delete_workspace(workspace)

    def workspace_check(self, workspace):
        if not workspace:
            raise HTTPException(
                detail="workspace does not exist", status_code=status.HTTP_404_NOT_FOUND
            )

    def workspace_link_invite(self, slug: str, role: RoleOptions, request: Request):

        workspace = self.workspace_repo.get_workspace(slug)
        self.workspace_check(workspace)

        token = gen_token(workspace.slug)
        role_tok = gen_token(role)
        if workspace.revoke_link:
            workspace.revoke_link = True
            self.workspace_repo.update_workspace(workspace)

        invite_link = f"{request.base_url}/{workspace.name}/invite/{token}/{role_tok}/roku=invite/"
        resp = {
            "message": "Invite Link Created successfully",
            "data": invite_link,
            "status": status.HTTP_200_OK,
        }
        return resp

    def revoke_workspace_link(self, workspace_slug: str):
        workspace = self.workspace_repo.get_workspace(workspace_slug)
        self.workspace_check(workspace)
        workspace.revoke_link = False
        self.update_workspace(workspace)

        resp = {
            "message": "Workspace revoked successfully",
            "data": workspace,
            "status": status.HTTP_200_OK,
        }
        return resp

    def get_workspace_member_check(self, id: int, workspace_id: int):

        return self.workspace_member_repo.get_workspace_member(workspace_id, id)

    def workspace_member_check(self, workspace_member):
        if not workspace_member:
            raise HTTPException(
                detail="User is not a member of the workspace",
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def workspace_member_check_(self, workspace_member):
        if workspace_member:
            raise HTTPException(
                detail="User is a member of the workspace",
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def join_workspace(
        self, token: str, role_token: str, join_workspace: schemas.JoinWorkspace
    ) -> schemas.MessageWorkspaceMembResp:

        token_data = retrieve_token(token)
        role_tok_data = retrieve_token(role_token)

        if not token_data:
            raise HTTPException(
                detail="Token invalid", status_code=status.HTTP_409_CONFLICT
            )
        if not role_tok_data:
            role_tok_data = RoleOptions.member

        workspace_check = self.workspace_repo.get_workspace(token_data)

        if not workspace_check:
            raise HTTPException(
                detail="Workspace does not exist", status_code=status.HTTP_404_NOT_FOUND
            )

        user_check = user_repo.get_user(join_workspace.email)
        if not user_check:
            raise HTTPException(
                detail="No account for this detail",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        workspace_mem_check = (
            self.workspace_member_repo.get_workspace_member_by_user_id(
                workspace_check.id, user_check.id
            )
        )
        self.workspace_member_check_(workspace_mem_check)

        workspace_member_data = {
            "member_id": user_check.id,
            "role": role_tok_data,
            "workspace_id": workspace_check.id,
        }

        workspace_member = self.workspace_member_repo.create_workspace_member(
            workspace_member_data
        )
        workspace_member_ = self.member_orm_call(workspace_member)

        resp = {
            "message": "User Joined Workspace",
            "data": workspace_member_,
            "status": status.HTTP_201_CREATED,
        }
        return resp

    def get_workspace_member(
        self, id: int, workspace_slug: str
    ) -> schemas.MessageWorkspaceMembResp:

        workspace = self.workspace_repo.get_workspace(workspace_slug)
        self.workspace_check(workspace)
        workspace_member_check = self.get_workspace_member_check(id, workspace.id)
        self.workspace_member_check(workspace_member_check)
        workspace_member = self.member_orm_call(workspace_member_check)
        resp = {
            "message": "Workspace Member Retrieved Successfully",
            "data": workspace_member,
            "status": status.HTTP_200_OK,
        }

        return resp

    def get_all_workspace_member(
        self, workspace_slug: str
    ) -> schemas.MessageListWorkspaceResp:

        workspace = self.workspace_repo.get_workspace(workspace_slug)
        self.workspace_check(workspace)

        workspace_member_check = self.workspace_member_repo.get_workspace_members(
            workspace.id
        )
        self.workspace_member_check(workspace_member_check)

        workspace_member_ = []
        for workspace_member in workspace_member_check:
            workspace_member_.append(self.member_orm_call(workspace_member))

        resp = {
            "message": "Workspace Members retrieved successfully",
            "data": workspace_member_,
            "status": status.HTTP_200_OK,
        }
        return resp

    def update_workspace_member(
        self,
        workspace_slug: str,
        id: int,
        role_update: schemas.UpdateWorkspaceMember,
    ):
        workspace = self.workspace_repo.get_workspace(workspace_slug)
        self.workspace_check(workspace)
        workspace_member = self.workspace_member_repo.get_workspace_member(
            workspace.id, id
        )
        self.workspace_member_check(workspace_member)
        workspace_member.role = role_update.role
        workspace_member = self.workspace_member_repo.update_workspace_member(
            workspace_member
        )
        resp = {
            "message": "Workspace Member Updated Successfully",
            "data": workspace_member,
            "status": status.HTTP_200_OK,
        }

        return resp

    def delete_workspace_member(self, workspace_slug: str, user_id: int):

        workspace = self.workspace_repo.get_workspace(workspace_slug)
        self.workspace_check(workspace)
        workspace_member = self.workspace_member_repo.get_workspace_member(
            workspace.id, user_id
        )
        self.workspace_member_check(workspace_member)
        self.workspace_member_repo.delete_workspace_member(workspace_member)


workspace_service = WorkspaceService()
