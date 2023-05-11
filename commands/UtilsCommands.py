import discord
import math
import json

from discord.ext import commands
from utils import Message

with open('config/config.json') as f:
    config = json.load(f)
    PREFIX = config['prefix']
    DELETE_TIMER = config['deletetimer']


class Utils(commands.Cog):
    """Utility commands"""

    def __init__(self, bot):
        self.bot = bot

    # /// COMMANDS \\\
    @commands.command(name="pfp", usage="pfp (@user/id)", description="Shows the bot's ping")
    async def pfp(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.message.author

        await ctx.send(user.display_avatar)

    # /// HELP \\\
    @commands.command(name="utils", usage="utils", description="Shows all utility commands")
    async def utils(self, ctx, page: int = 1):
        await ctx.message.delete()
        cmds = []
        for command in self.bot.commands:
            if command.cog_name == "Utils" and command.name != "utils":
                cmds.append(f"[{PREFIX}{command.name}] - {command.description}")
        if not cmds:
            await ctx.send("No fun commands available.", delete_after=DELETE_TIMER)
            return
        num_pages = math.ceil(len(cmds) / 10)
        if page > num_pages:
            page = num_pages
        elif page < 1:
            page = 1
        start = (page - 1) * 10
        end = start + 10
        output_text = Message.paginated_codeblock("Utility Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Utils(bot))
