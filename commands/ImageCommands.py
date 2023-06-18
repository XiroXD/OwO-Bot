import requests
import discord
import math
import json

from utils import Message, Api, Config
from discord.ext import commands
from io import BytesIO

DELETE_TIMER = Config.get("deletetimer")


class Image(commands.Cog):
    """Utility commands"""

    def __init__(self, bot):
        self.bot = bot

    # /// COMMANDS \\\
    @commands.command(name="fox", usage="fox", description="Sends a random fox image")
    async def fox(self, ctx):
        await ctx.message.delete()
        link = Api.some_random_api("img", "fox", field="link")
        fox = BytesIO(requests.get(link, stream=True).content)
        await ctx.send(file=discord.File(fox, filename="foxie.png"))
    
    # Dogs are better
    @commands.command(name="cat", usage="cat", description="Sends a random cat image")
    async def cat(self, ctx):
        await ctx.message.delete()
        link = Api.some_random_api("img", "cat", field="link")
        cat = BytesIO(requests.get(link, stream=True).content)
        await ctx.send(file=discord.File(cat, filename="gato.png"))
        
    @commands.command(name="redpanda", usage="redpanda", description="Sends a random red panda image")
    async def redpanda(self, ctx):
        await ctx.message.delete()
        link = Api.some_random_api("img", "red_panda", field="link")
        panda = BytesIO(requests.get(link, stream=True).content)
        await ctx.send(file=discord.File(panda, filename="panda.png"))
            
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
        output_text = Message.paginated_codeblock("Image Commands", chr(10).join(cmds[start:end]), page, num_pages)
        await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Image(bot))
