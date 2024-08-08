import discord
import re

EMOJI_REGEX = r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>'


async def smessage(owner: discord.User, STALK_USERS, message: discord.Message):
    if str(message.author.id) in STALK_USERS:
        newmsg = replace_emojis_with_urls(message.content)
        await owner.send(
            f"*{message.author.name}* wrote:\n```{newmsg} ```\n-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")


async def smessage_edit(owner: discord.User, STALK_USERS, before: discord.Message, after: discord.Message):
    if str(before.author.id) in STALK_USERS:
        before_msg = replace_emojis_with_urls(before.content)
        after_msg = replace_emojis_with_urls(after.content)
        await owner.send(
            f"*{before.author.name}* edited:\n```{before_msg} ```\nto\n```{after_msg} ```\n-# in **[{before.channel.name}]({after.jump_url})** on  **{before.channel.guild.name}**")


async def smessage_delete(owner: discord.User, STALK_USERS, message: discord.Message):
    if str(message.author.id) in STALK_USERS:
        newmsg = replace_emojis_with_urls(message.content)
        await owner.send(
            f"*{message.author.name}* deleted message:\n```{newmsg} ```\n-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")


def replace_emojis_with_urls(content: str) -> str:
    def get_url(match):
        animated, name, emoji_id = match.groups()
        ext = "gif" if animated else "png"
        return f" ``` [{name}](https://cdn.discordapp.com/emojis/{emoji_id}.{ext}?size=96&quality=lossless) ||{emoji_id}|| ``` "

    return re.sub(EMOJI_REGEX, get_url, content)
