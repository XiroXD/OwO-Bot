import colorama
import requests
import asyncio
import semver
import json
import os

from utils import Message, Log, Api, Toast, Config, Console
from discord.ext import commands
from colorama import Fore, Back


colorama.init(autoreset=True)
Console.clear()

try:
    TOKEN = Config.get("token")
    PREFIX = Config.get("prefix")
    DELETE_TIMER = Config.get("deletetimer")
except Exception:
    Log.error("Couldn't read config file")
    exit(1)

if not TOKEN:
    Log.error("Please put your token in config/config.json")
    exit(1)

OwO = commands.Bot(command_prefix=PREFIX, self_bot=True, reconnect=True)

OwO.remove_command('help')

lost_connection = False


@OwO.event
async def on_ready():
    global lost_connection
    lost_connection = False
    Toast.send('Selfbot', 'Successfully connected to Discord gateway')
    
    Log.print_banner()
    width = Console.get_width()

    print(Fore.WHITE + f"Prefix: {OwO.command_prefix} | User: {OwO.user} | Servers: {len(OwO.guilds)}".center(width))

    Log.custom_info('[Selfbot]', 'Successfully connected to Discord gateway')
    Log.custom_info('[Selfbot]', f'Logged in as {OwO.user}')


@OwO.event
async def on_disconnect():
    global lost_connection
    if not lost_connection:
        lost_connection = True
        Toast.send('Selfbot', 'Lost connection to Discord gateway')
        Log.warn('Lost connection to Discord gateway')


@OwO.event
async def on_resumed():
    global lost_connection
    lost_connection = False
    Toast.send('Selfbot', 'Reconnected to Discord gateway')
    Log.warn('Reconnected to Discord gateway')


@OwO.event
async def on_command(ctx):
    Log.info(f'Command used: {ctx.command}')


@OwO.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(Message.error("Command not found"), delete_after=DELETE_TIMER)
    else:
        await ctx.message.delete()
       

async def update_check():
    Log.info("Checking for updates")
    url = "https://raw.githubusercontent.com/XiroXD/OwO-Bot/master/version.json"
    r = requests.get(url).content
    parsed = json.loads(r)
    if not os.path.exists("./data/version.json"):
        Api.get_version()
        
    else:
        with open("./data/version.json") as f:
            version = json.load(f)
            compare = semver.compare(version['version'], parsed['version'])
            if compare == -1:
                Api.get_version()
                Toast.send('Selfbot', f'New version available: {parsed["version"]}')
                Log.warn(f'New version available: {parsed["version"]}')
                exit(0)
            else: 
                Log.info("You're using the latest version!")

async def load():
    await update_check()
    debug = Config.get("development")['debug']
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await OwO.load_extension(f'commands.{filename[:-3]}')
            if debug:
                print(f'{Back.BLUE}{Fore.BLACK}[Commands]{Back.RESET} {Fore.WHITE}Loaded {filename}')
    for filename in os.listdir('./events'):
        if filename.endswith('.py'):
            await OwO.load_extension(f'events.{filename[:-3]}')
            if debug:
                print(f'{Back.YELLOW}{Fore.BLACK}[Events]{Back.RESET} {Fore.WHITE}Loaded {filename}')


async def main():
    async with OwO:
        await load()
        await OwO.start(TOKEN)


asyncio.run(main())
