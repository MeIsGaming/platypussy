from discord.ext import commands
from iniconfig import IniConfig

config = IniConfig("config.ini")
prefix = config.get("config", "prefix")
TOKEN = config.get("config", "token")

bot = commands.Bot(command_prefix=prefix.lower())

@bot.event
async def on_ready():
    print(f"Successfully logged in as {bot.user.name}.")


@bot.command()
async def foo(ctx, arg, arg2):
    await ctx.send(arg + arg2)

bot.run(TOKEN)