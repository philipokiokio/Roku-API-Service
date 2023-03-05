from campaign.campaign_repo import (
    Campaign,
    Coupon,
    EventRefferal,
    campaign_repo,
    coupon_repo,
    event_ref_repo,
)


class CampaignService:
    def __init__(self) -> None:
        self.repo = campaign_repo
        self.event_ref_repo = event_ref_repo
        self.coupon_repo = coupon_repo
