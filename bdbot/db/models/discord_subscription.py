from bdbot.db.models.subscription import Subscription
from bdbot.mention import MentionChoice, MentionPolicy


class DiscordSubscription(Subscription):
    guild_id: int
    channel_id: int
    mentions: MentionChoice
    mentions_policy: MentionPolicy | None
    role_id: int | None
