from src.app.utils.base_repo_utils import BaseRepo
from src.campaign.models import Campaign


class CampaignRepo(BaseRepo):
    def base_query(self):
        self.db.query(Campaign)

    def get_campaign(self, slug: str):
        return self.base_query().filter(Campaign.slug == slug).first()

    # def get_campaign(self, user_id: int):
    #     return self.base_query().filter(Campaign.slug == slug)

    def create_campaign(self, create_campaign) -> Campaign:
        new_campaign = Campaign(**create_campaign.dict())
        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def delete_campaign(self, campaign: Campaign):
        self.db.delete(campaign)
        self.db.commit()

    def update_campaign(self, campaign: Campaign):
        self.db.commit()
        self.db.refresh(campaign)
        return campaign
