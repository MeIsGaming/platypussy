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
            if member is None:
                print("member is None!")
            else:
                NAME = member.name
                NICK = member.nick or member.name

            BEFORE_CHANNEL = before.channel.name
            AFTER_CHANNEL = after.channel.name
            BEFORE_GUILD = before.channel.guild.name
            AFTER_GUILD = after.channel.guild.name

            TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"   "

            if after.mute:
                await member.edit(mute=False)
                print(
                    f"{TIMESTAMP}Unmuted {str(NICK)}({str(NAME)}) in {str(AFTER_CHANNEL)} on {str(AFTER_GUILD)}")
                arl(0.25)

            if after.deaf:
                await member.edit(deafen=False)
                print(
                    f"{TIMESTAMP}Undeafened {str(NICK)}({str(NAME)}) in {str(AFTER_CHANNEL)} on {str(AFTER_GUILD)}")
                arl(0.25)

            if before.channel is None:
                print(
                    f"{TIMESTAMP}{str(NICK)} joined {str(AFTER_CHANNEL)} on {str(AFTER_GUILD)}")
            elif after is None:
                print(
                    f"{TIMESTAMP}{str(NICK)} left {str(BEFORE_CHANNEL)} on {str(BEFORE_GUILD)}")
            elif before.channel is not after.channel:
                print(
                    f"{TIMESTAMP}{str(NICK)} left {str(BEFORE_CHANNEL)}({str(BEFORE_GUILD)}) and joined {str(AFTER_CHANNEL)}({str(AFTER_GUILD)})")


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
