import discord


async def smessage(owner: discord.User, STALKUSERS, message: discord.Message):
    if str(message.author.id) in STALKUSERS:
        await owner.send(
            f"*{message.author.name}* wrote:\n```{message.content}```\n-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")


async def smessage_edit(owner: discord.User, STALKUSERS, before: discord.Message, after: discord.Message):
    if str(before.author.id) in STALKUSERS:
        await owner.send(f"*{before.author.name}* edited:\n```{before.content}```\nto\n```{after.content}```\n-# in **[{before.channel.name}]({after.jump_url})** on  **{before.channel.guild.name}**")


async def smessage_delete(owner: discord.User, STALKUSERS, message: discord.Message):
    if str(message.author.id) in STALKUSERS:
        await owner.send(
            f"*{message.author.name}* deleted message:\n```{message.content}```\n-# in **[{message.channel.name}]({message.jump_url})** on  **{message.channel.guild.name}**")
