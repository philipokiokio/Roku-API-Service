from typing import List, Union

from fastapi import status
from fastapi.exceptions import HTTPException

from auth.models import User
from campaign import schemas
from campaign.campaign_repo import (
    Campaign,
    Coupon,
    EventRefferal,
    campaign_repo,
    coupon_repo,
    event_ref_repo,
    event_repo,
)
from workspace.models import Workspace


class CampaignService:
    def __init__(self) -> None:
        self.repo = campaign_repo
        self.event_repo = event_repo
        self.event_ref_repo = event_ref_repo
        self.coupon_repo = coupon_repo

    def camp_orm_call(self, campaign: Campaign):
        campaign_dict = campaign.__dict__
        campaign_dict["workspace"] = campaign.workspace_id
        campaign_dict["event"] = campaign.event
        campaign_dict["coupon"] = campaign.coupon
        campaign_dict["creator"] = campaign.creator

        return campaign_dict

    def create_campaign(
        self,
        workspace: Workspace,
        campaign_create: schemas.CampaignCreate,
        current_user: User,
    ):

        campaign_check = self.repo.campaign_check(workspace.id, campaign_create.name)
        if campaign_check:
            raise HTTPException(
                detail="Campaign with this title for this workspace Exists",
                status_code=status.HTTP_409_CONFLICT,
            )
        campaign_dict = campaign_create.dict(exclude_unset=True)
        # deleting data that is not a part of the campaign table.
        del campaign_dict["event"]
        del campaign_dict["coupon"]

        # filling campaign data
        campaign_dict["slug"] = self.repo.time_slugger
        campaign_dict["workspace_id"] = workspace.id
        campaign_dict["api_key"] = "keysys" + "-" + self.repo.time_slugger
        campaign_dict["created_by"] = current_user.id

        # creating campaign
        campaign = self.repo.create(campaign_dict)

        # creating campaign based on Campaign Type
        if campaign.campaign_type == schemas.CampaignType.event.value:
            if campaign_create.event:
                event_dict = {
                    "name": campaign_create.event,
                    "campaign_id": campaign.id,
                    "slug": self.repo.time_slugger,
                    "created_by": current_user.id,
                    "has_rewards": False,
                }
                self.event_repo.create(event_dict)

        elif campaign.campaign_type == schemas.CampaignType.coupon.value:

            if campaign_create.coupon:
                coupon_dict = {
                    "coupon": campaign_create.coupon.coupon,
                    "value_off": campaign_create.coupon.value_off,
                    "campaign_id": campaign.id,
                    "slug": self.repo.time_slugger,
                    "created_by": current_user.id,
                }
                self.coupon_repo.create(coupon_dict)

        # campaign = self.camp_orm_call(campaign)

        resp = {
            "message": "Campaign created successfully",
            "data": campaign,
            "status": status.HTTP_201_CREATED,
        }

        return resp

    def campaign_check(self, campaign: Union[Campaign, List[Campaign]]):
        if not campaign:
            raise HTTPException(
                detail="Campaign does not exist for this workspace",
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def get_campaigns(self, workspace: Workspace):

        campaigns = self.repo.get_by_workspace(workspace.id)
        self.campaign_check(campaigns)

        campaigns_ = []

        for campaign in campaigns:
            campaigns_.append(campaign)

        resp = {
            "message": "Campaign retrieved successfully",
            "data": campaigns_,
            "status": status.HTTP_200_OK,
        }
        return resp

    def get_campaign(self, workspace: Workspace, slug: str):

        campaign = self.repo.by_workspace__slug(workspace.id, slug)
        self.campaign_check(campaign)

        # campaign = self.camp_orm_call(campaign)

        resp = {
            "message": "Campaign retrieved successfully",
            "data": campaign,
            "status": status.HTTP_200_OK,
        }
        return resp

    def update_campaign(
        self, workspace: Workspace, slug: str, update_campaign: schemas.CampaignUpdate
    ):

        campaign = self.repo.by_workspace__slug(workspace.id, slug)
        self.campaign_check(campaign)

        for key, value in update_campaign.dict(exclude_unset=True).items():

            setattr(campaign, key, value)

        campaign = self.repo.update(campaign)

        # campaign = self.camp_orm_call(campaign)

        resp = {
            "message": "Campaign is updated successfully",
            "data": campaign,
            "status": status.HTTP_200_OK,
        }
        return resp

    def delete_campaign(self, workspace: Workspace, slug: str):
        campaign = self.repo.by_workspace__slug(workspace.id, slug)
        self.campaign_check(campaign)

        self.repo.delete(campaign)

        return {"status": status.HTTP_204_NO_CONTENT}
