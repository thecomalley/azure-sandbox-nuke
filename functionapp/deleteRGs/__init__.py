import datetime
import logging
import os

import azure.functions as func
from discord_webhook import DiscordWebhook, DiscordEmbed

from deleteRGs.deleteRGs import delete_rgs


def main(mytimer: func.TimerRequest) -> None:
    try:
        delteded_rgs, un_delteded_rgs = delete_rgs()

        webhook = DiscordWebhook(url=os.environ.get("DISCORD_WEBHOOK_URL"))
        embed = DiscordEmbed(
            title="AzCleaner", color='03b2f8', timestamp=datetime.datetime.utcnow()
        )
        embed.set_timestamp()

    
    except Exception as e:
        logging.exception(e)
        embed.add_embed_field(
            name="error running function",
            value=str(e),
            inline=False,
        )
        webhook.add_embed(embed)
        webhook.execute()

    else:
        if len(delteded_rgs) == 0 and len(un_delteded_rgs) == 0:
            logging.info("Nothing to delete...")
        else:
            embed.add_embed_field(
                name="deleted rgs",
                value=str(delteded_rgs),
                inline=False,
            )
            webhook.add_embed(embed)
            webhook.execute()