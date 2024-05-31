from bdbot.subscription_type import SubscriptionType
from bdbot.time import Weekday


class Subscription:
    id: int
    comic_id: int
    subscription_type: SubscriptionType
    weekday: Weekday
    hour: int
