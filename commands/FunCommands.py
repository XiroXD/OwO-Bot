import discord
import random
import json
import math

from utils import Message, Config
from discord.ext import commands
from utils import Api

DELETE_TIMER = Config.get("deletetimer")


class Fun(commands.Cog):
    """Funny commands"""

    def __init__(self, bot):
        self.bot = bot

    # // COMMANDS \\\
    @commands.command(name="dick", usage="dick (@user/id) (size)", description="Check how big someone pp is")
    async def dick(self, ctx, user: discord.Member = None, size=None):
        await ctx.message.delete()
        if user is None:
            user = ctx.message.author

        if size == 'microscopic':
            size = 0
        elif size == 'small':
            size = 1
        elif size == 'medium':
            size = 5
        elif size == 'big':
            size = 30
        else:
            size = random.randint(0, 20)

        if size == 0:
            pp = "Couldn't measure dick size.. maybe it's too small or doesn't exist?"
        else:
            pp = "8"+"="*size+"D"
        await ctx.send(Message.codeblock(f"{user}'s dick size", pp), delete_after=DELETE_TIMER)

    @commands.command(name="gay", usage="gay (@user/id) (number)", description="Check how gay someone is")
    async def gay(self, ctx, user: discord.Member = None, number: int = None):
        await ctx.message.delete()

        if user is None:
            user = ctx.message.author

        if number is None:
            number = random.randint(0, 100)

        await ctx.send(Message.codeblock("Gay Meter", f"[{user}] is {number}% gay!"), delete_after=DELETE_TIMER)

    @commands.command(name="joke", usage="joke", description="Gives a random joke")
    async def joke(self, ctx):
        await ctx.message.delete()
        joke = Api.some_random_api("others", "joke", "joke")
        await ctx.send(Message.codeblock("Joke", joke), delete_after=DELETE_TIMER)

    # /// HELP \\\
    @commands.command(name="fun", usage="fun", description="Shows all the fun commands")
    async def fun(self, ctx, page: int = 1):
        await ctx.message.delete()
        cmds = []
        for command in self.bot.commands:
            if command.cog_name == "Fun" and command.name != "fun":
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
        output_text = Message.paginated_codeblock("Fun Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Fun(bot))
