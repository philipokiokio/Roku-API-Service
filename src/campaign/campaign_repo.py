from typing import Union

from src.app.utils.base_repo_utils import BaseActionMixinRepo, BaseRepo
from src.campaign.models import Campaign, Coupon, Event, EventRefferal


class CampaignRepo(BaseRepo):
    @property
    def base_query(self):
        return self.db.query(Campaign)

    def campaign_check(self, workspace_id: int, campaign_name: str):
        return self.base_query.filter(
            Campaign.workspace_id == workspace_id, Campaign.name.ilike(campaign_name)
        ).first()

    def get_campaign(self, slug: str):
        return self.base_query.filter(Campaign.slug == slug).first()

    def get_by_workspace(self, workspace_id: int) -> Union[Campaign, None]:
        return self.base_query.filter(Campaign.workspace_id == workspace_id).all()

    def by_workspace__slug(
        self, workspaace_id: int, slug: str
    ) -> Union[Campaign, None]:
        return self.base_query.filter(
            Campaign.workspace_id == workspaace_id, Campaign.slug == slug
        ).first()

    # def get_campaign(self, user_id: int):
    #     return self.base_query.filter(Campaign.slug == slug)

    def create(self, create_campaign) -> Campaign:
        new_campaign = Campaign(**create_campaign.dict())
        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def delete(self, campaign: Campaign):
        self.db.delete(campaign)
        self.db.commit()

    def update(self, campaign: Campaign):
        self.db.commit()
        self.db.refresh(campaign)
        return campaign


class EventRepo(BaseActionMixinRepo):
    def __init__(self, model):
        super().__init__(model)

    pass


class EventRefferalRepo(BaseRepo):
    @property
    def base_query(self):
        return self.db.query(EventRefferal)

    def create(self, campaign_refferal: dict) -> EventRefferal:
        campaign_reff = EventRefferal(**campaign_refferal)
        self.db.add(campaign_reff)
        self.db.commit()
        self.db.refresh(campaign_reff)
        return campaign_reff

    def update(self, campaign_reff: EventRefferal) -> EventRefferal:
        self.db.commit()
        self.db.refresh(campaign_reff)
        return campaign_reff

    def delete(self, campaign_reff: EventRefferal):
        self.db.delete(campaign_reff)
        self.db.commit()


class CouponRepo(BaseRepo):
    @property
    def base_query(self):
        return self.db.query(Coupon)

    def create(self, coupon_dict: dict) -> Coupon:
        coupon = Coupon(**coupon_dict)
        self.db.add(coupon)
        self.db.commit()
        self.db.refresh(coupon)
        return coupon

    def update(self, coupon: Coupon) -> Coupon:
        self.db.commit()
        self.db.refresh(coupon)
        return coupon

    def delete(self, coupon: Coupon):
        self.db.delete(coupon)
        self.db.refresh()


campaign_repo = CampaignRepo()
event_repo = EventRepo(Event)
event_ref_repo = EventRefferalRepo()
coupon_repo = CouponRepo()
