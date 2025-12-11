from pyrogram import filters
from BADMUSIC import app
from TheAPI import api
import codecs


# ------------------ HASHTAG GENERATOR ------------------ #

@app.on_message(filters.command(["hashtag", "hastag"]))
async def hashtag_handler(_, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Example:\n\n`/hashtag python tutorial`"
        )

    text = message.text.split(" ", 1)[1]

    try:
        res = api.gen_hashtag(text)
    except Exception as e:
        return await message.reply_text(f"API Error:\n`{e}`")

    await message.reply_text(
        f"✨ **Generated Hashtags:**\n\n<pre>{res}</pre>",
        quote=True
    )


# ------------------ TEXT ENCODER ------------------ #

@app.on_message(filters.command(["encode"]))
async def encode_text(_, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Example:\n\n`/encode hello world`")

    text = message.reply_to_message.text if message.reply_to_message else message.text.split(" ", 1)[1]

    try:
        encoded = text.encode("unicode_escape").decode()
    except Exception as e:
        return await message.reply_text(f"Encoding Error:\n`{e}`")

    await message.reply_text(
        f"🔐 **Encoded Text:**\n\n<code>{encoded}</code>",
        quote=True
    )


# ------------------ TEXT DECODER ------------------ #

@app.on_message(filters.command(["decode"]))
async def decode_text(_, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Example:\n\n`/decode \\u0939\\u0948`")

    text = message.reply_to_message.text if message.reply_to_message else message.text.split(" ", 1)[1]

    try:
        decoded = codecs.decode(text, "unicode_escape")
    except Exception as e:
        return await message.reply_text(f"Decoding Error:\n`{e}`")

    await message.reply_text(
        f"🔓 **Decoded Text:**\n\n<code>{decoded}</code>",
        quote=True
    )


# ------------------ MODULE INFO ------------------ #

__MODULE__ = "ᴛᴇxᴛ ᴄᴏᴅᴇʀ"
__HELP__ = """
**HASHTAG GENERATOR**
• `/hashtag text` – Generate hashtags.

**TEXT ENCODER**
• `/encode text` – Encode into unicode escape (\\u).

**TEXT DECODER**
• `/decode text` – Decode unicode escape to normal text.
"""
