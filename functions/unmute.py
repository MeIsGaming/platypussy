import discord
import datetime

from functions.arl import arl

ADMIN_IDS = [871497360658800640, 1227610698373140553,
             314760782187462657, 671036411343798292]


async def unmute(member: discord.Member, before: any, after: any) -> None:
    """
    Event handler for when a member's voice state is updated.

    Args:
        member (discord.Member): The member whose voice state was updated.
        before (discord.VoiceState): The member's voice state before the update.
        after (discord.VoiceState): The member's voice state after the update.
    """
    try:

        if member.id in ADMIN_IDS:
            NAME = member.name
            NICK = member.nick or member.name

            CHANNEL = member.voice.channel.name
            SERVER = member.voice.channel.guild
            SERVERNAME = SERVER.name
            TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"   "
            if after.mute:
                await member.edit(mute=False)
                print(
                    f"{TIMESTAMP}Unmuted {NICK}({NAME}) in {CHANNEL} on {SERVERNAME}")
                arl(0.5)

            if after.deaf:
                await member.edit(deafen=False)
                print(
                    f"{TIMESTAMP}Undeafened {NICK}({NAME}) in {CHANNEL} on {SERVERNAME}")
                arl(0.5)

            if before.channel is None:
                print(
                    f"{TIMESTAMP}{NICK} joined {after.channel.name} on {after.channel.guild.name}")

            if after is None:
                print(
                    f"{TIMESTAMP}{NICK} left {before.channel.name} on {before.channel.guild.name}")


#        if member.id in BAD_IDS:
#            if after.channel == member.guild.me.voice.channel:
#                await member.edit(voice_channel=None)
#        if member.id in ANNOYING_IDS:
#            if after.channel:
#                    sleep(1.2)
#                    await member.edit(voice_channel=choice(member.guild.voice_channels))
#        if member.id in NO_TALKI:
#            if after.channel:
#                if after.channel == member.guild.me.voice.channel:
#                    await member.edit(voice_channel=choice(member.guild.voice_channels))

    except Exception as error:
        print(error)
