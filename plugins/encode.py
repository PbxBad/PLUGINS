import base64
from pyrogram import filters
from BADMUSIC import app


def encode_text(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def decode_text(text: str) -> str:
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return "❌ Invalid encoded text!"


@app.on_message(filters.command("encode"))
async def encode_handler(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Example:\n\n`/encode Hello World`")

    text = message.text.split(" ", 1)[1]
    encoded = encode_text(text)

    msg = f"""
🔐 **Encoded Text:**  
`{encoded}`
"""
    await message.reply_text(msg, quote=True)


@app.on_message(filters.command("decode"))
async def decode_handler(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Example:\n\n`/decode aGVsbG8=`")

    text = message.text.split(" ", 1)[1]
    decoded = decode_text(text)

    msg = f"""
🔓 **Decoded Text:**  
`{decoded}`
"""
    await message.reply_text(msg, quote=True)


__MODULE__ = "ᴇɴᴄᴏᴅᴇ-ᴅᴇᴄᴏᴅᴇ"
__HELP__ = """
**🔐 ENCODE & DECODE TEXT**

• `/encode text` – Convert text into Base64 encrypted format  
• `/decode encoded_text` – Decode Base64 into normal text  

**Examples:**
- `/encode BADMUSIC`
- `/decode QkFETVVTSUM=`
"""
