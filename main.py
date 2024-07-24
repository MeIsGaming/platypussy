from discord.ext import commands
from iniconfig import IniConfig

config = IniConfig("config.ini")
prefix = config.get("config", "prefix")
TOKEN = config.get("config", "token")

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print(f"Successfully logged in as {bot.user.name}.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    author = message.author
    content = message.content
    print(f"{author}: {content}")

@bot.event
async def on_member_update(before, after):
    print(f"{before.nick} -> {after.nick}")

bot.run(TOKEN)