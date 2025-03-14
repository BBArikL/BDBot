from bdbot import utils
from bdbot.comics.comicskingdom import ComicsKingdom
from bdbot.comics.gocomics import Gocomics
from bdbot.comics.webtoons import Webtoons
from bdbot.embed import Embed
from bdbot.field import Field

HELP_SCHEDULE_NAME = "schedule"
HELP_GENERAL_NAME = "general"
HELP_NEW_NAME = "new"
HELP_FAQ_NAME = "faq"
HELP_FIELDS_NAME = "fields"


def get_general_help(general_help: dict[str, str | dict[str, str]]) -> Embed:
    strips = utils.strip_details
    help_embed: Embed = Embed.from_dict(general_help)
    help_embed.fields.clear()
    for website in [Gocomics, ComicsKingdom, Webtoons]:
        help_embed.add_field(
            Field(name=website.WEBSITE_NAME, value=website.WEBSITE_HELP)
        )
    for strip in strips.values():
        if strip.__class__ not in [
            Gocomics,
            ComicsKingdom,
            Webtoons,
        ]:
            help_embed.add_field(Field(name=strip.name, value=strip.help))
    for field in general_help[HELP_FIELDS_NAME]:
        field: dict[str, str]
        help_embed.add_field(Field(**field))
    return help_embed
