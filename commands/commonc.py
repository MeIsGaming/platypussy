import discord
from io import BytesIO
from petpetgif import petpet
from functions.commonf import (decrement_dick_counter,)
import platy_sec.sec_main as sec
from asyncio import create_task


"""
Handles the 'makepet' command by creating a 'petpet' animation of the user's avatar and sending it as a GIF in the chat.

Args:
    ctx: The context of the command.
    user: The user whose avatar will be animated (default is None).

Returns:
    None
"""


async def makepet(ctx, user):

    try:
        await ctx.message.delete()
    except (discord.ext.commands.errors.CommandInvokeError, discord.errors.Forbidden) as e:
        print(f"Error deleting message: {e}")

    avatar = await (user.avatar if user else ctx.author.avatar).read()
    source = BytesIO(avatar)
    dest = BytesIO()
    petpet.make(source, dest)
    dest.seek(0)
    await ctx.send(file=discord.File(dest, filename=f"{avatar[0]}-petpet_uwu.gif"))

"""
Handles the 'dick' command by processing the user input and sending a response message based on the input parameters and the current dick count.

Args:
    ctx: The context of the command.
    arg: The length of the 'dick' represented by the number of '=' characters.
    dick_counter: A dictionary storing the count of 'dick' requests per user.

Returns:
    None
"""


async def handle_dick(ctx, arg, dick_counter):
    user_id = ctx.author.id
    dick_counter[user_id] = dick_counter.setdefault(user_id, 0) + 1

    if dick_counter[user_id] >= 3:
        msg = "Interessant,dass du so viele Cöcks sehen willst 👀...\n[Why are you gay?](https://media1.tenor.com/m/RMP0AGC2sLIAAAAC/why-are-you-gay.gif) \nHier deiner, damit du nd traurig bist:\n```8=3```\n-# Vergiss nd durchzuatmen und trink genug! (Bitte warte kurz, bin überfordert  nya~)"
    elif arg > 500:
        msg = "Übertreib nd, solange is nd mal der von deiner mum UwU\nDein Cöck, du kek:[||uwu||](https://cdn.discordapp.com/emojis/1272257395451756645.webp?size=96&quality=lossless)\n-# 8==B"
        arg = 20
    elif arg <= 0:
        msg = "# (\{\})\n-# UwU [Pussyyyy](https://media1.tenor.com/m/Jc9jT66AJRwAAAAd/chipi-chipi-chapa-chapa.gif)"
    else:
        msg = f"8{'=' * arg}B"

    await ctx.send(msg)

    # Start a background task to decrement the counter after a specified time
    create_task(decrement_dick_counter(user_id, dick_counter))

    sec.arl(0.2)
