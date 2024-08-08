import discord
import re

EMOJI_REGEX = r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>'

async def smessage(owner: discord.User, STALKUSERS, message: discord.Message):
    if str(message.author.id) in STALKUSERS:
        await  extr_emojis(message)
        newmsg = message.replace(EMOJI_REGEX, )
        await owner.send(
            f"*{message.author.name}* wrote:\n```{newmsg}```\n-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")


async def smessage_edit(owner: discord.User, STALKUSERS, before: discord.Message, after: discord.Message):
    if str(before.author.id) in STALKUSERS:
        await owner.send(f"*{before.author.name}* edited:\n```{before.content}```\nto\n```{after.content}```\n-# in **[{before.channel.name}]({after.jump_url})** on  **{before.channel.guild.name}**")


async def smessage_delete(owner: discord.User, STALKUSERS, message: discord.Message):
    if str(message.author.id) in STALKUSERS:
        await owner.send(
            f"*{message.author.name}* deleted message:\n```{message.content}```\n-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")




async def extr_emojis(message):
    emojis = re.findall(EMOJI_REGEX, message.content)

    for emoji in emojis:
        name = emoji[1]
        ext = "gif" if emoji[0] else "png"
        image_url = f"https://cdn.discordapp.com/emojis/{emoji[2]}.{ext}?size=96&quality=lossless"

    return emojis
