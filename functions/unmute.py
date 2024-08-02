import discord

ADMIN_IDS = [871497360658800640, 1227610698373140553, 314760782187462657]


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
            if after.mute:
                await member.edit(mute=False)
            if after.deaf:
                await member.edit(deafen=False)
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
