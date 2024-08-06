import discord
from io import BytesIO
from petpetgif import petpet


# Define a new function to clone a guild
async def makepet(ctx, user):
    
    try:
        await ctx.message.delete()
    except discord.ext.commands.errors.CommandInvokeError:
        print("Error deleting message containing command")
    except discord.errors.Forbidden:
        print("Error deleting message (2FA)")

    avatar = await (ctx.author.avatar if user is None else user.avatar).read()
    source = BytesIO(avatar)
    dest = BytesIO()
    petpet.make(source, dest)
    dest.seek(0)
    await ctx.send(file=discord.File(dest, filename=f"{avatar[0]}-petpet_uwu.gif"))
