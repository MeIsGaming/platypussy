import discord
import requests

from discord.ext import commands
from iniconfig import IniConfig
from io import BytesIO
from petpetgif import petpet as petpetgif

# Konfigurationsdatei laden
config = IniConfig("config.ini")
prefix = config.get("config", "prefix")
TOKEN = config.get("config", "token")
SUGG_WEBHOOK_URL = config.get("config", "sugg_webhook_url")

# Bot-Initialisierung
bot = commands.Bot(command_prefix=prefix.lower())

# Ereignis, wenn der Bot bereit ist


@bot.event
async def on_ready():
    print(f"Successfully logged in as {bot.user.name}.")

# Funktion, um Vorschläge in eine Textdatei zu speichern


def save_suggestion_to_file(suggestion):
    with open("suggestions.txt", "a") as file:
        file.write(suggestion + "\n")


# Neuer Command zum Erfassen von Vorschlägen


@bot.command()
async def suggest(ctx, *, suggestion):
    webhook = SUGG_WEBHOOK_URL
    data = {
        "content": suggestion,
        "username": ctx.author.name,
        "avatar_url": ctx.author.avatar.url
    }
    response = requests.request("POST", webhook, data=data)
    if response.status_code != 204:
        print(
            f"Failed to send suggestion to webhook: {response.status_code} - {response.text}")


# Beispiel-Command (test)


@bot.command()
async def test(ctx, arg, arg2):
    await ctx.send("Test: " + arg + arg2)

# Command (pet)


@bot.command()
async def pet(ctx, user: discord.User = None):
    try:
        await ctx.message.delete()
    except discord.ext.commands.errors.CommandInvokeError:
        print("Error deleting message containing command")
    except discord.errors.Forbidden:
        print("Error deleting message (2FA)")

    if user is None:
        avatar = await ctx.author.avatar.read()
    else:
        avatar = await user.avatar.read()
    source = BytesIO(avatar)
    dest = BytesIO()
    petpetgif.make(source, dest)
    dest.seek(0)
    await ctx.send(file=discord.File(dest, filename=f"{avatar[0]}-petpet.gif"))

# Command (dick)


@bot.command()
async def dick(ctx, arg: int):
    shaft = "=" * arg
    await ctx.send("8" + shaft + "B")

# Bot starten
bot.run(TOKEN)
