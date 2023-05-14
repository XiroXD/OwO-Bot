import json

from discord_webhook import DiscordWebhook, DiscordEmbed
from utils import Log


def embed(
    type: str,
    description: str,
    author: str = None,
    footer: str = None,
    fields: list = None,
):
    if fields is None:
        fields = {}
    try:
        with open("config/notifications/webhooks.json") as f:
            config = json.load(f)
            url = config[type]
            title = config["title"]
            color = config["color"]
    except FileNotFoundError:
        Log.error("Webhook config file not found")
        return
    except Exception as e:
        Log.error(e)
        return
    print(url)
    if url is None:
        return
    webhook = DiscordWebhook(url=url)
    embed = DiscordEmbed(
        title=f"{title} | {type}", description=description, color=color
    )
    embed.set_author(name=author)
    embed.set_footer(text=footer)
    embed.set_timestamp()
    if fields:
        for field in fields:
            embed.add_embed_field(name=field[0], value=field[1], inline=field[2])
    webhook.add_embed(embed)
    webhook.execute()
