import discord
import requests
import json
import sqlite3
import datetime 

from discord.ext import commands
from iniconfig import IniConfig
from io import BytesIO
from psutil import cpu_percent, getloadavg, virtual_memory, cpu_count, cpu_freq, sensors_battery, disk_partitions
from petpetgif import petpet as petpetgif
from GPUtil import getGPUs
from regex import regex as re

# Konfigurationsdatei laden
conn = sqlite3.connect("user_data.db")
c = conn.cursor()

config = IniConfig("config.ini")
prefix = config.get("config", "prefix")
TOKEN = config.get("config", "token")
SUGG_WEBHOOK_URL = config.get("config", "sugg_webhook_url")
ABUSEIPDB = config.get("config","abuseipdb_key")

# Database-Initialisierung
c.execute('''
CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    suggestion TEXT NOT NULL,
    date TEXT NOT NULL
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT NOT NULL,
    username TEXT NOT NULL,
    admin_privileges INTEGER NOT NULL
)
''')

# Function to add a suggestion
def add_suggestion(user, suggestion):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''
    INSERT INTO suggestions (user, suggestion, date)
    VALUES (?, ?, ?)
    ''', (user, suggestion, date))
    conn.commit()

# Function to add a permission
def add_permission(userid, username, admin_privileges):
    c.execute('''
    INSERT INTO permissions (userid, username, admin_privileges)
    VALUES (?, ?, ?)
    ''', (userid, username, admin_privileges))
    conn.commit()

def get_admin_privileges(userid):
    c.execute('''
    SELECT admin_privileges FROM permissions WHERE userid = ?
    ''', (userid,))
    return c.fetchone()
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


# Command zum Erfassen von Vorschlägen
@bot.command()
async def suggest(ctx, *, suggestion):
    save_suggestion_to_file(suggestion)

    embed = {
        "title": "Vorschlag wurde übermittelt:",
        "description": suggestion,
        "color": 5814783,  # Farbe des Embeds
        "author": {
            "name": ctx.author.name,
            "icon_url": ctx.author.avatar.url
        }
    }
    data = {
        "embeds": [embed]
    }
    headers = {
        "Content-Type": "application/json"
    }
    add_suggestion(ctx.author.name, suggestion)
    r = requests.post(
        SUGG_WEBHOOK_URL, data=json.dumps(data), headers=headers)

    if re.match(r"2\d\d", str(r.status_code)):
        await ctx.author.send("```Danke für deinen Vorschlag!```")
        await ctx.author.send(f"Dein Vorschlag \" *{suggestion}* \" wurde erfolgreich übermittelt. Bei genaueren Nachfragen etc wende dich bitte an **<@871497360658800640>** oder **<@1227610698373140553>**")
    elif re.match(r"4\d\d", str(r.status_code)):
        print(
            f"Error sending suggestion. Client error: {r.status_code} - {r.text}")
    elif re.match(r"5\d\d", str(r.status_code)):
        print(
            f"Error sending suggestion. Server error: {r.status_code} - {r.text}")
    else:
        print(
            f"Error sending suggestion: {r.status_code} - {r.text}")

# Event for finding all nitro gift links
@bot.event
async def on_message(message):
    if re.match(r"(https://)?(discord\.(gift|com/gifts)/)[a-zA-Z0-9]+", message.content):
        with open("nitro.txt", "a") as f:
            f.write(message.content)
            f.truncate()
            f.close()
    else:
        await bot.process_commands(message)

# Command (ping)
@bot.command()
async def ping(ctx):
    calc = round(bot.latency * 1000,1)
    await ctx.send(f"Pong! {calc}ms")

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

# Command (load)
@bot.command()
async def load(ctx):
    if 1 == get_admin_privileges(ctx.author.id)[0]:
        disk_part = disk_partitions()
        gpu = getGPUs()
        disks = []
        for disk in disk_part:
            disk_letter = disk.device.split(":")[0]
            disks.append(f"{disk_letter}")
        if gpu:
            gpu_ram = round(gpu[0].memoryTotal / 1024)
            gpu_ram_used = round(gpu[0].memoryUsed / 1024)
            temp = gpu[0].temperature
            gpu = gpu[0]
            await ctx.send(f"CPU: {cpu_percent(interval=1)}%\nLoad: {getloadavg()}\nRAM: {round(virtual_memory().total / (1024 ** 3),2)}GB\nRAM Load: {int(virtual_memory().percent)}%\nCPU Cores: {cpu_count()}\nCPU Frequency: {round(cpu_freq().current / 1000,2)}GHz\nBattery: {sensors_battery()}%\nDisks: {disks}\nGPU: {gpu.name}\nGPU RAM: {gpu_ram}GB\nGPU RAM Used: {gpu_ram_used}GB\nGPU Temp: {temp}°C")
        else:
            await ctx.send(f"CPU: {cpu_percent(interval=1)}%\nLoad: {getloadavg()}\nRAM: {round(virtual_memory().total / (1024 ** 3),2)}GB\nRAM Load: {int(virtual_memory().percent)}%\nCPU Cores: {cpu_count()}\nCPU Frequency: {round(cpu_freq().current / 1000,2)}GHz\nBattery: {sensors_battery()}%\nDisks: {disks}")

# Command (dick)
@bot.command()
async def dick(ctx, arg: int):
    shaft = "=" * arg
    await ctx.send("8" + shaft + "B")

# Command (Cat)
@bot.command()
async def cat(ctx):
    url = "https://cataas.com/cat?type=medium"
    await ctx.send(url)

# Command (Cif)
@bot.command()
async def cif(ctx):
    url = "https://cataas.com/cat/gif?type=medium"
    await ctx.send(url)

# Command (meow)
@bot.command()
async def meow(ctx,*,text=None):
    if text is None:
        url = "https://cataas.com/cat/says/hehe?fontSize=50&fontColor=violet"
    else:
        url = f"https://cataas.com/cat/says/{text}?fontSize=50&fontColor=violet"
    await ctx.send(url)

# Command (safeIP)
# just a idea not realy taht important its just looks in abuseipdb for the confidentscore and if its a tor ip would be better with virustotal api but i didnt had a api key for it
@bot.command()
async def safeip(ctx,ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    ABUSEIPDB = "1e6cf48ee828259d88c533d1576303e454cb00319033f4bd32237a66124477b60bfb989c93aa8a27" # temporary aslong as Gabriel didnt added it to config.ini
    querystring = {
    'ipAddress': ip,
    'maxAgeInDays': '365'
    }
    headers = {
    'Accept': 'application/json',
    'Key': ABUSEIPDB
    }
    r = requests.request(method='GET', url=url, headers=headers, params=querystring)
    decodedResponse = json.loads(r.text)
    confidentscore = decodedResponse["data"]["abuseConfidenceScore"]
    isTor = decodedResponse["data"]["isTor"]
    await ctx.send(f"TorIP:  {isTor}\nConfidentscore:  {confidentscore}/100")

# Command (AddAdmin)
@bot.command()
async def addadmin(ctx,user: discord.User):
    if 1 == get_admin_privileges(ctx.author.id)[0]:
        add_permission(user.id, user.name, 1)
        await ctx.send("added succesfully")
    else:
        await ctx.send("du hast keine berechtigungen dafür")

#command (RemoveAdmin)
@bot.command()
async def removeadmin(ctx,user: discord.User):
    if 1 == get_admin_privileges(ctx.author.id)[0]:
        add_permission(user.id,user.name,0)
        await ctx.send("removed succesfully")
    else:
        await ctx.send("du hast keine berechtigungen dafür")

@bot.command()
@commands.has_guild_permissions(moderate_members=True)
async def timeout(ctx,time,*,user: discord.User,reason):
    ...
    #https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=timeout#discord.Member.timeout
    

# Bot starten
bot.run(TOKEN)
