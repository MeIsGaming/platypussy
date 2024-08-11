import asyncio


async def decrement_dick_counter(user_id, dick_counter):
    # Specify the time interval for decrementing the counter (e.g., 60 seconds)
    await asyncio.sleep(60)
    if user_id in dick_counter:
        dick_counter[user_id] -= 1
