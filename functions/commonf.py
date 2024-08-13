import asyncio
import platy_sec as sec


"""
Handles the ping command to measure the bot's latency and respond with a 'Pong!' message.

Args:
    ctx: The context of the command.

Returns:
    None
"""


async def handle_ping(ctx, bot, BANNED_GUILDS):
    if str(ctx.guild.id) not in BANNED_GUILDS:
        calc = round(bot.latency * 1000, 1)
        await ctx.send(f"Pong! {calc}ms")
        sec.arl(0.1)


async def decrement_dick_counter(user_id, dick_counter):
    # Specify the time interval for decrementing the counter (e.g., 60 seconds)
    await asyncio.sleep(60)
    if user_id in dick_counter:
        dick_counter[user_id] -= 1
