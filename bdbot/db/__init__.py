import logging
import os
import shutil
import sqlite3
import time

from tortoise import Tortoise, connections

from bdbot.db.discord_subscription import (
    ChannelSubscription,
    DiscordSubscription,
    ServerSubscription,
)
from bdbot.db.subscription import Subscription
from bdbot.files import BACKUP_FILE_PATH, BACKUPS_PATH, DATABASE_FILE_PATH
from bdbot.time import get_now

TORTOISE_ORM = {
    "connections": {
        "default": f"sqlite://{DATABASE_FILE_PATH}",
    },
    "apps": {
        "bdbot": {"models": ["bdbot.db"], "default_connection": "default"},
    },
}


async def dbinit():
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas()


def save_backup(logger: logging.Logger):
    """

    :param logger:
    :return:
    """
    logger.info("Running backup...")
    # Copies the database
    backup_file_path = BACKUP_FILE_PATH + get_now().strftime("%Y_%m_%d_%H") + ".db"

    source = None
    backup = None
    try:
        source = sqlite3.connect(DATABASE_FILE_PATH)
        backup = sqlite3.connect(backup_file_path)
        with backup:
            source.backup(backup)
    except sqlite3.Error as e:
        print(f"Backup failed: {e}")
    finally:
        if source:
            source.close()
        if backup:
            backup.close()

    for f in os.listdir(BACKUPS_PATH):
        fp = os.path.join(BACKUPS_PATH, f)
        if os.stat(fp).st_mtime < int(time.time()) - 14 * 86400:
            os.remove(fp)
    logger.info("Backup successfully done")


async def restore_backup():
    """Restore a last used backup"""
    await connections.close_all()
    files = list(filter(os.path.isfile, os.listdir(BACKUPS_PATH)))
    files.sort(key=lambda x: os.path.getmtime(x))
    if len(files) == 0:
        raise Exception("No backup was found!")
    last_backup = os.path.join(BACKUPS_PATH, files[-1])
    os.remove(DATABASE_FILE_PATH)
    shutil.copyfile(last_backup, DATABASE_FILE_PATH)
    await dbinit()


__all__ = [
    dbinit,
    save_backup,
    restore_backup,
    Subscription,
    DiscordSubscription,
    ServerSubscription,
    ChannelSubscription,
]
