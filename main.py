import colorama
import requests
import asyncio
import json
import os

from utils import Message, Log, Api
from discord.ext import commands
from colorama import Fore, Back
from win11toast import notify


colorama.init(autoreset=True)
os.system('cls')

try:
    with open('config/config.json') as f:
        config = json.load(f)
        TOKEN = config['token']
        PREFIX = config['prefix']
        DELETE_TIMER = config['deletetimer']
except:
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
    notify('Selfbot', 'Successfully connected to Discord gateway', app_id="OwO Bot")
    
    count = 0
    for command in OwO.commands:
        count += 1
    Log.info(f'Loaded {count} commands')
    
    Log.custom_info('[Selfbot]', 'Successfully connected to Discord gateway')
    Log.custom_info('[Selfbot]', f'Logged in as {OwO.user}')
    
    url = "https://raw.githubusercontent.com/XiroXD/OwO-Bot/master/version.json"
    r = requests.get(url).content
    parsed = json.loads(r)
    if not os.path.exists("./data/version.json"):
        Api.get_version()
    else:
        with open("./data/version.json") as f:
            version = json.load(f)
            if version['version'] != parsed['version']:
                notify('Selfbot', f'New version available: {parsed["version"]}',  app_id="OwO Bot")
                Log.warn(f'New version available: {parsed["version"]}')


@OwO.event
async def on_disconnect():
    global lost_connection
    if not lost_connection:
        lost_connection = True
        notify('Selfbot', 'Lost connection to Discord gateway', app_id="OwO Bot")
        Log.warn('Lost connection to Discord gateway')


@OwO.event
async def on_resumed():
    global lost_connection
    lost_connection = False
    notify('Selfbot', 'Reconnected to Discord gateway', app_id="OwO Bot")
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
        await ctx.send(Message.error(error), delete_after=DELETE_TIMER)


async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await OwO.load_extension(f'commands.{filename[:-3]}')
            print(f'{Back.BLUE}{Fore.BLACK}[Commands]{Back.RESET} {Fore.WHITE}Loaded {filename}')
    for filename in os.listdir('./events'):
        if filename.endswith('.py'):
            await OwO.load_extension(f'events.{filename[:-3]}')
            print(f'{Back.YELLOW}{Fore.BLACK}[Events]{Back.RESET} {Fore.WHITE}Loaded {filename}')


async def main():
    async with OwO:
        await load()
        await OwO.start(TOKEN)


asyncio.run(main())
