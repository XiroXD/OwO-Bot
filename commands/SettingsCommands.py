import discord
import math

from utils import Message, Config
from discord.ext import commands

DELETE_TIMER = Config.get("deletetimer")


class Settings(commands.Cog):
    """Settings commands"""

    def __init__(self, bot):
        self.bot = bot

    # // COMMANDS \\\
    @commands.command(name="prefix", usage="prefix <prefix>", description="Changes the prefix")
    async def prefix(self, ctx, prefix: str):
        await ctx.message.delete()
        Config.set("prefix", prefix)
        self.bot.command_prefix = prefix
        await ctx.send(Message.codeblock("Prefix Changed", f"Prefix changed to [{prefix}]"), delete_after=DELETE_TIMER)

    # /// HELP \\\
    @commands.command(name="settings", usage="settings", description="Shows all the settings commands")
    async def fun(self, ctx, page: int = 1):
        await ctx.message.delete()
        cmds = []
        for command in self.bot.commands:
            if command.cog_name == "Settings" and command.name != "settings":
                PREFIX = Config.get("prefix")
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
        output_text = Message.paginated_codeblock("Settings Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Settings(bot))
