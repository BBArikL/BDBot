from discord.ext.commands.bot import Bot

from bdbot.comics import BaseComic


class BDBotClient(Bot):
    link_cache: dict = {}
    comic_details: dict[str, BaseComic] = {}
    random_footers: list[str] = []
