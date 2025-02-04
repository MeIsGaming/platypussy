import random
from discord import Member, VoiceState

from datetime import datetime

from platy_sec.sec_main import arl

ADMIN_IDS = [871497360658800640, 314760782187462657,
             1102328237889167470, 1186602199757889539, 729707718730055773, 556889798170640384, 766992639916376064]

# 871497360658800640: Ashley
# 314760782187462657: Radde
# 1102328237889167470: Alki
# 1186602199757889539: zweit Account
# 729707718730055773: Joyce
# 556889798170640384: Felix
# 766992639916376064: Teuf

BAD_IDS = []
ANNOYING_IDS = []
BANNED_SERVER_IDS = [456856734875516933,
                     858335306468950036, 813245078340501557]


async def voicehandler(member: Member, before: VoiceState, after: VoiceState) -> None:
    """
    Event handler for when a member's voice state is updated.

    Args:
        member (discord.Member): The member whose voice state was updated.
        before (discord.VoiceState): The member's voice state before the update.
        after (discord.VoiceState): The member's voice state after the update.
    """
    try:
        # Get the member's name and nickname
        member_name = member.name
        member_nick = member.nick or member_name

        # Get the channel names and guild names before and after the update
        before_channel_name = before.channel.name if before.channel else "Unknown"
        after_channel_name = after.channel.name if after.channel else "Unknown"
        before_guild_name = before.channel.guild.name if before.channel and before.channel.guild else "Unknown"
        after_guild_name = after.channel.guild.name if after.channel and after.channel.guild else "Unknown"
        before_guild_id = before.channel.guild.id if before.channel and before.channel.guild else "Unknown"
        after_guild_id = after.channel.guild.id if after.channel and after.channel.guild else "Unknown"
        full_name = f"{member_nick}({member_name})"

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "   "

        # Event logging strings
        join_str = f"{timestamp}{full_name} joined {after_channel_name} on {after_guild_name}"
        leave_str = f"{timestamp}{full_name} left {before_channel_name} on {before_guild_name}"
        move_str = f"{timestamp}{full_name} moved from {before_channel_name} to {after_channel_name} on {after_guild_name}"
        server_change_str = f"{timestamp}{full_name} left {before_channel_name} on {before_guild_name} and joined {after_channel_name} on {after_guild_name}"
        unmute_str = f"{timestamp}Unmuted {full_name} in {after_channel_name} on {after_guild_name}"
        undeafen_str = f"{timestamp}Undeafened {full_name} in {after_channel_name} on {after_guild_name}"
        self_unmute_str = f"{timestamp}SELFUnmuted {full_name} in {after_channel_name} on {after_guild_name}"
        self_undeafen_str = f"{timestamp}SELFUndeafened {full_name} in {after_channel_name} on {after_guild_name}"
        start_stream_str = f"{timestamp}{full_name} started streaming in {after_channel_name} on {after_guild_name}"
        stop_stream_str = f"{timestamp}{full_name} stopped streaming in {before_channel_name} on {before_guild_name}"
        start_cam_str = f"{timestamp}{full_name} turned on their cam in {after_channel_name} on {after_guild_name}"
        stop_cam_str = f"{timestamp}{full_name} turned off their cam in {before_channel_name} on {before_guild_name}"
        kick_str = f"{timestamp}Kicked {full_name} from voice channel"
        move_member_str = f"{timestamp}Moved {full_name} to a random voice channel"

        # Append the event to the full voice log
        if (
            before_guild_id not in BANNED_SERVER_IDS
            and after_guild_id not in BANNED_SERVER_IDS
        ):

            # Check if the member is an admin
            if member.id in ADMIN_IDS:
                # Unmute the member if they were muted
                if after.mute:
                    await member.edit(mute=False)
                    print(f"🔊 {unmute_str}")
                    with open("logs/admin_voice_logs.txt", "a", encoding='utf-8') as f:
                        f.write(f"{unmute_str}\n")
                    arl(0.25, 0)

                # Undeafen the member if they were deafened
                if after.deaf:
                    await member.edit(deafen=False)
                    print(f"🔇 {undeafen_str}")
                    with open("logs/admin_voice_logs.txt", "a", encoding='utf-8') as f:
                        f.write(f"{undeafen_str}\n")
                    arl(0.25, 0)

            # Log the member's join or leave events
            if before.channel is None:
                print(f"➕ {join_str}")
                with open("logs/logs.txt", "a", encoding='utf-8') as f:
                    f.write(f"{join_str}\n")
            elif after.channel is None:
                print(f"➖ {leave_str}")
                with open("logs/logs.txt", "a", encoding='utf-8') as f:
                    f.write(f"{leave_str}\n")
            elif before.channel != after.channel:
                if before_guild_name == after_guild_name:
                    print(f"🔀 {move_str}")
                    with open("logs/logs.txt", "a", encoding='utf-8') as f:
                        f.write(f"{move_str}\n")
                else:
                    print(f"🔀 {server_change_str}")
                    with open("logs/logs.txt", "a", encoding='utf-8') as f:
                        f.write(f"{server_change_str}\n")

            # Check if the member is streaming
            if after.self_stream and not before.self_stream:
                print(f"🖥️ {start_stream_str}")
                with open("logs/logs.txt", "a", encoding='utf-8') as f:
                    f.write(f"{start_stream_str}\n")
            elif before.self_stream and not after.self_stream:
                print(f"🖥️ {stop_stream_str}")
                with open("logs/logs.txt", "a", encoding='utf-8') as f:
                    f.write(f"{stop_stream_str}\n")

            # Check if the member is activated  cam
            if after.self_video and not before.self_video:
                print(f"📹 {start_cam_str}")
                with open("logs/logs.txt", "a", encoding='utf-8') as f:
                    f.write(f"{start_cam_str}\n")
            elif before.self_video and not after.self_video:
                print(f"📹 {stop_cam_str}")
                with open("logs/logs.txt", "a", encoding='utf-8') as f:
                    f.write(f"{stop_cam_str}\n")

        # Special handling for certain member IDs (NOT WORKING!!)
        if member.id in BAD_IDS:
            if after.channel == member.guild.me.voice.channel:
                await member.edit(voice_channel=None)
                print("🦵 " + kick_str)
                with open("logs/logs.txt", "a", encoding='utf-8') as f:
                    f.write(f"{kick_str}\n")
        elif member.id in ANNOYING_IDS:
            if after.channel:
                arl(1.2, 0)
                await member.edit(voice_channel=random.choice(member.guild.voice_channels))
            if after.channel and after.channel == member.guild.me.voice.channel:
                await member.edit(voice_channel=random.choice(member.guild.voice_channels))
                if after.channel == member.guild.me.voice.channel:
                    await member.edit(voice_channel=random.choice(member.guild.voice_channels))
                    print(move_member_str)

    except Exception as error:
        print(error)
