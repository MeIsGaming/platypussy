import requests
import json



from GPUtil import getGPUs
from regex import regex as re

# Define a new function to process a suggestion
async def process_suggestion(ctx, suggestion, SUGG_WEBHOOK_URL):
    save_suggestion_to_file(suggestion)

    embed = {
        "title": "Vorschlag wurde übermittelt:",
        "description": suggestion,
        "color": 5814783,
        "author": {
            "name": ctx.author.name,
            "icon_url": ctx.author.avatar.url
        }
    }
    data = {
        "embeds": [embed]
    }
    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(SUGG_WEBHOOK_URL, data=json.dumps(data), headers=headers)

    if re.match(r"2\d\d", str(r.status_code)):
        await ctx.author.send("```Danke für deinen Vorschlag!```")
        await ctx.author.send(f"Dein Vorschlag \" *{suggestion}* \" wurde erfolgreich übermittelt. Bei genaueren Nachfragen etc wende dich bitte an **<@871497360658800640>** oder **<@1227610698373140553>**")
    elif re.match(r"4\d\d", str(r.status_code)):
        print(f"Error sending suggestion. Client error: {r.status_code} - {r.text}")
    elif re.match(r"5\d\d", str(r.status_code)):
        print(f"Error sending suggestion. Server error: {r.status_code} - {r.text}")
    else:
        print(f"Error sending suggestion: {r.status_code} - {r.text}")

def save_suggestion_to_file(suggestion):
    with open("suggestions.txt", "a") as file:
        file.write(suggestion + "\n")

