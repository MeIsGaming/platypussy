import discord
import re

EMOJI_REGEX = r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>'


async def send_stalk_message(owner: discord.User, STALK_USERS, message: discord.Message, content: str):
    """
    Sends a message to the owner if the message author is in the STALK_USERS list.
    """
    if str(message.author.id) in STALK_USERS:
        await owner.send(content)


def replace_emojis_with_urls(content: str) -> str:
    """
    Replaces emojis in the content with their image URLs.
    """
    def get_url(match):
        animated, name, emoji_id = match.groups()
        ext = "gif" if animated else "png"
        return f" ``` [{name}](https://cdn.discordapp.com/emojis/{emoji_id}.{ext}?size=96&quality=lossless) ||{emoji_id}|| ``` "

    return re.sub(EMOJI_REGEX, get_url, content)


def generate_content(action: str, message: discord.Message, before_content: str = None, after_content: str = None) -> str:
    """
    Generates content based on the action performed on a message.

    Args:
        action (str): The action performed on the message.
        ...
    """
    if action == "write":
        return (f"*{message.author.name}* wrote:\n```{before_content} ```\n"
                f"-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")
    elif action == "edit":
        return (f"*{message.author.name}* edited:\n```{before_content} ```\nto\n```{after_content} ```\n"
                f"-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")
    elif action == "delete":
        return (f"*{message.author.name}* deleted message:\n```{before_content} ```\n"
                f"-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")
    else:
        return (f"Not an action({action}) in stalker.py")


async def smessage(owner: discord.User, STALK_USERS, message: discord.Message):
    """
    Sends a message to the owner if a message of a STALK_USER is sent.
    """
    newmsg = replace_emojis_with_urls(message.content)
    content = generate_content("write", message, before_content=newmsg)
    await send_stalk_message(owner, STALK_USERS, message, content)


async def smessage_edit(owner: discord.User, STALK_USERS, before: discord.Message, after: discord.Message):
    """
    Sends a message to the owner if a message of a STALK_USER is edited.
    """
    before_msg = replace_emojis_with_urls(before.content)
    after_msg = replace_emojis_with_urls(after.content)
    content = generate_content(
        "edit", before, before_content=before_msg, after_content=after_msg)
    await send_stalk_message(owner, STALK_USERS, before, content)


async def smessage_delete(owner: discord.User, STALK_USERS, message: discord.Message):
    """
    Sends a message to the owner if a message of a STALK_USER is deleted.
    """
    newmsg = replace_emojis_with_urls(message.content)
    content = generate_content("delete", message, before_content=newmsg)
    await send_stalk_message(owner, STALK_USERS, message, content)
