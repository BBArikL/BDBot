from tortoise import Model, fields

from bdbot.db.subscription import Subscription
from bdbot.mention import MentionPolicy


class DiscordSubscription(Subscription, Model):
    channel: "ChannelSubscription" = fields.ForeignKeyField(
        "bdbot.ChannelSubscription", related_name="subscriptions"
    )


class ChannelSubscription(Model):
    id: int = fields.IntField(primary_key=True)
    server: "ServerSubscription" = fields.ForeignKeyField(
        "bdbot.ServerSubscription", related_name="channels"
    )
    subscriptions: fields.ReverseRelation[DiscordSubscription]


class ServerSubscription(Model):
    id: int = fields.IntField(primary_key=True)
    mention_policy: MentionPolicy = fields.CharEnumField(
        MentionPolicy, default=MentionPolicy.Deactivated
    )
    role_id: int | None = fields.IntField(null=True, default=None)
    channels: fields.ReverseRelation[ChannelSubscription]
