from src.app.utils.base_repo_utils import BaseRepo
from src.workspace.models import Workspace, WorkspaceMember


class WorkspaceRepo(BaseRepo):
    def base_query(self):
        return self.db.query(Workspace)

    def check_workspace(self, name: str):
        return self.base_query().filter(Workspace.name.ilike(name)).first()

    def get_workspace(self, slug: str):
        return self.base_query().filter(Workspace.slug == slug).first()

    def get_user_workspaces(self, user_id: int):
        return (
            self.base_query()
            .filter(Workspace.workspace_member.user_id.has(id=user_id))
            .all()
        )

    def user_workspace_count_data(self, user_id: int):

        user_workspace = (
            self.base_query()
            .filter(Workspace.workspace_member.any(member_id=user_id))
            .all()
        )
        workspace_count = (
            self.base_query()
            .filter(Workspace.workspace_member.any(member_id=user_id))
            .count()
        )
        return user_workspace, workspace_count

    def create_workspace(self, workspace_create: dict):
        new_workspace = Workspace(**workspace_create)
        self.db.add(new_workspace)
        self.db.commit()
        self.db.refresh(new_workspace)
        return new_workspace

    def update_workspace(self, workspace_update: Workspace):
        self.db.commit()
        self.db.refresh(workspace_update)
        return workspace_update

    def delete_workspace(self, workspace: Workspace):
        self.db.delete(workspace)
        self.db.commit()


class WorkspaceMemberRepo(BaseRepo):
    def base_query(self):
        return self.db.query(WorkspaceMember)

    def get_workspace_member(self, workspace_id: int, id: int):
        return (
            self.base_query()
            .filter(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.id == id,
            )
            .first()
        )

    def get_workspace_member_by_user_id(self, workspace_id: int, user_id: int):
        return (
            self.base_query()
            .filter(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.member_id == user_id,
            )
            .first()
        )

    def get_workspace_members(self, workspace_id: int):
        return (
            self.base_query()
            .filter(
                WorkspaceMember.workspace_id == workspace_id,
            )
            .all()
        )

    def create_workspace_member(self, workspace_member: dict):
        new_workspace_member = WorkspaceMember(**workspace_member)
        self.db.add(new_workspace_member)
        self.db.commit()
        self.db.refresh(new_workspace_member)
        return new_workspace_member

    def update_workspace_member(self, workspace_update):
        self.db.commit()
        self.db.refresh(workspace_update)
        return workspace_update

    def delete_workspace_member(self, workspace):
        self.db.delete(workspace)
        self.db.commit()


workspace_repo = WorkspaceRepo()
workspace_member_repo = WorkspaceMemberRepo()
