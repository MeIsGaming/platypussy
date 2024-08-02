import discord
from functions.arl import arl


# Define a new function to clone a guild
async def clone_guild(ctx, clone_from: int, clone_to: int, bot):
    guild_from = bot.get_guild(clone_from)
    if not guild_from:
        await ctx.send("Source server not found.")
        return

    guild_to = bot.get_guild(clone_to)
    if not guild_to:
        await ctx.send("Target server not found.")
        return

    for channel in guild_to.channels:
        try:
            arl(1)
            await channel.delete()
            print(f"Deleted Channel: {channel.name}")
        except discord.Forbidden:
            print(f"Error While Deleting Channel: {channel.name}")
        except discord.HTTPException:
            print(f"Unable To Delete Channel: {channel.name}")

    channels = guild_from.categories
    channel: discord.CategoryChannel
    new_channel: discord.CategoryChannel
    for channel in channels:
        try:
            # overwrites_to = {}
            # for key, value in channel.overwrites.items():
            # role = discord.utils.get(guild_to.roles, name=key.name)
            # overwrites_to[role] = value
            arl(1)
            new_channel = await guild_to.create_category(
                name=channel.name,
                position=channel.position
                # overwrites=overwrites_to
            )
            # await new_channel.edit()
            print(f"Created Category: {channel.name}")
        except discord.Forbidden:
            print(f"Error While Deleting Category: {channel.name}")
        except discord.HTTPException:
            print(f"Unable To Delete Category: {channel.name}")

    channel_text: discord.TextChannel
    channel_voice: discord.VoiceChannel
    category = None
    for channel_text in guild_from.text_channels:
        try:
            for category in guild_to.categories:
                try:
                    if category.name == channel_text.category.name:
                        break
                except AttributeError:
                    print(
                        f"Channel {channel_text.name} doesn't have any category!")
                    category = None
                    break

                # overwrites_to = {}
                # for key, value in channel_text.overwrites.items():
                # role = discord.utils.get(guild_to.roles, name=key.name)
                # overwrites_to[role] = value
            try:
                arl(1)
                new_channel = await guild_to.create_text_channel(
                    name=channel_text.name,
                    # overwrites=overwrites_to,
                    position=channel_text.position,
                    topic=channel_text.topic,
                    slowmode_delay=channel_text.slowmode_delay,
                    nsfw=channel_text.nsfw)
            except:
                arl(1)
                new_channel = await guild_to.create_text_channel(
                    name=channel_text.name,
                    # overwrites=overwrites_to,
                    position=channel_text.position)
            if category is not None:
                await new_channel.edit(category=category)
            print(f"Created Text Channel: {channel_text.name}")
        except discord.Forbidden:
            print(
                f"Error While Creating Text Channel: {channel_text.name}")
        except discord.HTTPException:
            print(f"Unable To Creating Text Channel: {channel_text.name}")
        except:
            print(
                f"Error While Creating Text Channel: {channel_text.name}")

    category = None
    for channel_voice in guild_from.voice_channels:
        try:
            for category in guild_to.categories:
                try:
                    if category.name == channel_voice.category.name:
                        break
                except AttributeError:
                    print(
                        f"Channel {channel_voice.name} doesn't have any category!")
                    category = None
                    break

                # overwrites_to = {}
                # for key, value in channel_voice.overwrites.items():
                # role = discord.utils.get(guild_to.roles, name=key.name)
                # overwrites_to[role] = value
            try:
                arl(1)
                new_channel = await guild_to.create_voice_channel(
                    name=channel_voice.name,
                    # overwrites=overwrites_to,
                    position=channel_voice.position,
                    bitrate=channel_voice.bitrate,
                    user_limit=channel_voice.user_limit,
                )
            except:
                arl(1)
                new_channel = await guild_to.create_voice_channel(
                    name=channel_voice.name,
                    # overwrites=overwrites_to,
                    position=channel_voice.position)
            if category is not None:
                arl(1)
                await new_channel.edit(category=category)
            print(f"Created Voice Channel: {channel_voice.name}")
        except discord.Forbidden:
            print(
                f"Error While Creating Voice Channel: {channel_voice.name}")
        except discord.HTTPException:
            print(
                f"Unable To Creating Voice Channel: {channel_voice.name}")
        except:
            print(
                f"Error While Creating Voice Channel: {channel_voice.name}")

    await ctx.send("Guild cloned.")
