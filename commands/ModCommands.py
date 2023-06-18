import json
import math

from utils import Message, Config
from discord.ext import commands

DELETE_TIMER = Config.get("deletetimer")


class Moderation(commands.Cog):
    """Moderation commands"""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ban", usage="ban <user> [reason]", description="Ban a member from the server")
    async def ban(self, ctx, member: commands.MemberConverter, reason: str = "No reason provided"):
        await ctx.message.delete()
        try:
            await member.ban(reason=reason)
            await ctx.send(Message.codeblock("User banned!", f"Banned {member.mention} for {reason}"))
        except Exception as e:
            await ctx.send(Message.codeblock("Error", e))


    # /// HELP \\\
    @commands.command(name="moderation", usage="moderation", description="Shows all the moderation commands")
    async def moderation(self, ctx, page: int = 1):
        await ctx.message.delete()
        cmds = []
        for command in self.bot.commands:
            if command.cog_name == "Moderation" and command.name != "moderation":
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
        output_text = Message.paginated_codeblock("Moderation Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))
