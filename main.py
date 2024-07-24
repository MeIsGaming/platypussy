from discord.ext import commands
from iniconfig import IniConfig

config = IniConfig("config.ini")
prefix = config.get("config", "prefix")
TOKEN = config.get("config", "token")

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print(f"AI Selfbot successfully logged in as {bot.user.name}.")

bot.run(TOKEN)