import random
from pyrogram import filters
from BADMUSIC import app


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "Love is in the air but needs a little spark.",
                "A good start but there's room to grow.",
                "It's just the beginning of something beautiful.",
            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "A strong connection is there. Keep nurturing it.",
                "You've got a good chance. Work on it.",
                "Love is blossoming, keep going.",
            ]
        )
    else:
        return random.choice(
            [
                "Wow! It's a match made in heaven!",
                "Perfect match! Cherish this bond.",
                "Destined to be together. Congratulations!",
            ]
        )


@app.on_message(filters.command("love"))
async def love_command(client, message):
    args = message.text.split()

    if len(args) >= 3:
        name1 = args[1]
        name2 = args[2]

        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = (
            f"💞 **Love Calculator Result** 💞\n\n"
            f"**{name1}** ❤️ + **{name2}** ❤️ = **{love_percentage}%**\n\n"
            f"💬 *{love_message}*"
        )
    else:
        response = "Please enter two names like:\n`/love Rahul Priya`"

    await message.reply_text(response)


__MODULE__ = "ʟᴏᴠᴇ"
__HELP__ = """
**💘 ʟᴏᴠᴇ ᴄᴀʟᴄᴜʟᴀᴛᴏʀ 💘**

• `/love [name1] [name2]`
    → Cᴀʟᴄᴜʟᴀᴛᴇs ᴛʜᴇ ʟᴏᴠᴇ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ ʙᴇᴛᴡᴇᴇɴ ᴛᴡᴏ ᴘᴇᴏᴘʟᴇ.

**Example:**
`/love Aman Simran`
"""
