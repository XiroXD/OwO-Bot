import discord
import json

from discord.ext import commands
from utils import Log, Toast

with open('config/config.json') as f:
    config = json.load(f)
    PREFIX = config['prefix']
    DELETE_TIMER = config['deletetimer']


class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, discord.DMChannel):
            msg = f"""
Author: {message.author}
Content: {message.content}  
            """

            Log.custom_info("[Message Removed]", msg)
            Toast.send("Message Removed", msg)
        else:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return
        if isinstance(before.channel, discord.DMChannel):
            msg = f"""
Author: {before.author}
Before: {before.content}
After: {after.content}
            """
            Log.custom_info("[Message Edited]", msg)
            Toast.send("Message Edited", msg)
        else:
            return

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if isinstance(channel, discord.DMChannel):
            msg = f"""
{user} is typing...
            """
            Log.custom_info("[Typing]", msg)
            Toast.send("Typing", msg)


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))
