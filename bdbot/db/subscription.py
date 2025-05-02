from tortoise import fields

from bdbot.subscription_type import SubscriptionType
from bdbot.time import Weekday


class Subscription:
    id: int = fields.IntField(primary_key=True, generated=True)
    comic_id: int = fields.IntField()
    subscription_type: SubscriptionType = fields.CharEnumField(SubscriptionType)
    weekday: Weekday = fields.CharEnumField(Weekday)
    hour: int = fields.IntField()
