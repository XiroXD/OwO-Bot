import json
import math

from utils import Message, Config
from discord.ext import commands
from utils import Api

DELETE_TIMER = Config.get("deletetimer")


class Nsfw(commands.Cog):
    """Not safe for work commands"""

    def __init__(self, bot):
        self.bot = bot

    # // COMMANDS \\\
    @commands.command(name="hentai", usage="hentai", description="Returns a random hentai image")
    async def hentai(self, ctx):
        await ctx.message.delete()
        image = Api.nekobot_image_api("hentai")
        await ctx.send(image)

    @commands.command("sex", usage="sex <@user/id>", description="Have a sex with anyone")
    async def sex(self, ctx):
        await ctx.message.delete()
        await ctx.send(Message.codeblock("Bruh", "stop being horny u dum fuk"))

    # /// HELP \\\
    @commands.command(name="nsfw", usage="nsfw", description="Shows all the nsfw commands")
    async def nsfw(self, ctx, page: int = 1):
        await ctx.message.delete()
        cmds = []
        for command in self.bot.commands:
            if command.cog_name == "Nsfw" and command.name != "nsfw":
                PREFIX = Config.get("prefix")
                cmds.append(f"[{PREFIX}{command.name}] - {command.description}")
        if not cmds:
            await ctx.send("No nsfw commands available.", delete_after=DELETE_TIMER)
            return
        num_pages = math.ceil(len(cmds) / 10)
        if page > num_pages:
            page = num_pages
        elif page < 1:
            page = 1
        start = (page - 1) * 10
        end = start + 10
        output_text = Message.paginated_codeblock("Nsfw Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Nsfw(bot))
