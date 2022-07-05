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
        if len(delteded_rgs) > 0:
            embed.add_embed_field(
                name="Deleted Resource Groups",
                value=", ".join(delteded_rgs),
                inline=False,
            )
        if len(un_delteded_rgs) > 0:
            embed.add_embed_field(
                name="Failed to Delete Resource Groups",
                value=", ".join(un_delteded_rgs),
                inline=False,
            )

        webhook.add_embed(embed)
        response = webhook.execute()

    except Exception as e:
        logging.error("Failed to get Resoruce Groups")
        logging.exception(e)