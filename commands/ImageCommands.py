import discord
import math
import json

from discord.ext import commands
from utils import Message, Api
from io import BytesIO

with open('config/config.json') as f:
    config = json.load(f)
    PREFIX = config['prefix']
    DELETE_TIMER = config['deletetimer']


class Image(commands.Cog):
    """Utility commands"""

    def __init__(self, bot):
        self.bot = bot

    # /// COMMANDS \\\
    @commands.command(name="horny", usage="horny <@user/id>", description="Give someone a license to be horny")
    async def horny(self, ctx, user: discord.Member):
        await ctx.message.delete()
        pfp = user.display_avatar
        image = BytesIO(Api.some_random_api("canvas/misc", "horny", f"avatar={pfp}", True))
        await ctx.send(file=discord.File(image, filename=f"{user.name}.png"))

    @commands.command(name="deepfry", usage="deepfry <@user/id>", description="Deepfry someone's pfp")
    async def deepfry(self, ctx, user: discord.Member):
        await ctx.message.delete()
        pfp = user.display_avatar
        url = Api.nekobot_imagegen_api("deepfry", f"image={pfp}&raw=1")
        image = BytesIO(url)
        await ctx.send(file=discord.File(image, filename=f"{user.name}.png"))

    @commands.command(name="changemymind", usage="changemymind <text>", description="Create a change my mind meme")
    async def changemymind(self, ctx, text):
        image = BytesIO(Api.nekobot_imagegen_api("changemymind", f"text={text}&raw=1"))
        await ctx.send(file=discord.File(image, filename=f"{text}.png"))

    # /// HELP \\\
    @commands.command(name="image", usage="image", description="Shows all image commands")
    async def image(self, ctx, page: int = 1):
        await ctx.message.delete()
        cmds = []
        for command in self.bot.commands:
            if command.cog_name == "Image" and command.name != "image":
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
        output_text = Message.paginated_codeblock("Image Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Image(bot))