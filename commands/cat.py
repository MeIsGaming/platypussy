import platy_sec

"""
Handles commands to display cat images or GIFs from the 'cataas' API.

Args:
    ctx: The context of the command.
    command_type: The type of command ('cat', 'cif', 'meow').
    text: Optional text to display on the cat image (default is None).

Returns:
    None
"""


async def handle_cat_command(ctx, command_type, text=None):
    base_url = "https://cataas.com/cat"
    url_map = {
        "cat": f"{base_url}?type=medium",
        "cif": f"{base_url}/gif?type=medium",
        "meow": f"{base_url}/says/{text}?fontSize=50&fontColor=violet" if text else f"{base_url}/says/hehe?fontSize=50&fontColor=violet",
    }
    url = url_map.get(command_type, f"{base_url}?type=medium")
    if command_type not in url_map:
        url = f"Not a specified command_type({command_type}) in (cat.py)"
    await ctx.send(url)
    await platy_sec.arl(0.1)
