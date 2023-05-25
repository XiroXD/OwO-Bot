import json

from utils import Message, Config
from discord.ext import commands

DELETE_TIMER = Config.get("deletetimer")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, command=None):
        await ctx.message.delete()
        if command is None:
            categories = []
            for cog in self.bot.cogs:
                if "Help" not in cog and "events" not in cog.lower():
                    category_docstring = self.bot.get_cog(cog).__doc__
                    PREFIX = Config.get("prefix")
                    categories.append(f'[{PREFIX}{cog.lower()}] - {category_docstring}')
            categories_text = "\n".join(categories)
            output_text = Message.codeblock("Categories", categories_text)
            await ctx.send(output_text, delete_after=DELETE_TIMER)
        else:
            cmd = self.bot.get_command(command)
            if cmd is None:
                await ctx.send(Message.error("Command not found"), delete_after=DELETE_TIMER)
                return
            output_text = f"""
```ini
[OwO Bot]
```
```ini
[OwO Bot]
<> = Required
() = Optional

[{PREFIX}{cmd.usage}] - {cmd.description}
```
```
OwO Bot - Made by Xiro#0001 | Prefix: {PREFIX}
```
"""
            await ctx.send(output_text, delete_after=DELETE_TIMER)


async def setup(bot):
    await bot.add_cog(Help(bot))
