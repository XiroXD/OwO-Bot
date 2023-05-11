import math
import json

from discord.ext import commands
from utils import Message

with open('config/config.json') as f:
    config = json.load(f)
    PREFIX = config['prefix']
    DELETE_TIMER = config['deletetimer']


class Network(commands.Cog):
    """Network related commands"""

    def __init__(self, bot):
        self.bot = bot

    # /// COMMANDS \\\
    @commands.command(name="ping", usage="ping", description="Shows the bot's ping")
    async def ping(self, ctx):
        await ctx.message.delete()
        msg = f"[Discord Ping] - {round(self.bot.latency * 1000)}ms"
        await ctx.send(Message.codeblock("Pong!", msg), delete_after=DELETE_TIMER)

    # /// HELP \\\
    @commands.command(name="network", usage="network", description="Shows all the network commands")
    async def network(self, ctx, page: int = 1):
        await ctx.message.delete()
        cmds = []
        for command in self.bot.commands:
            if command.cog_name == "Network" and command.name != "network":
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
        output_text = Message.paginated_codeblock("Nsfw Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Network(bot))
