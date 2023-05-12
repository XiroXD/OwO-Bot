import json

from discord_webhook import DiscordWebhook, DiscordEmbed
from utils import Log

def embed(type: str, title: str, description: str, color: int, author: str = None, footer: str = None, fields: list = {}):
    try:
        with open('config/notifications/webhooks.json') as f:
            config = json.load(f)
            url = config[type]
    except FileNotFoundError:
        Log.error("Webhook config file not found")
        return
    except Exception:
        return

    webhook = DiscordWebhook(url=url)

    embed = DiscordEmbed(title=title, description=description, color=color)
    embed.set_author(name=author)
    embed.set_footer(text=footer)

    if fields:
        for field in fields:
            embed.add_embed_field(name=field[0], value=field[1], inline=field[2])
    
    embed.set_timestamp()

    webhook.add_embed(embed)
    webhook.execute()
