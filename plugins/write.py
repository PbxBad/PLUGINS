from pyrogram import filters
from pyrogram.types import Message
from BADMUSIC import app
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap
import os
import uuid

# ================= CONFIG =================

PAGE_PATH = "assets/page.jpg"
FONT_PATH = "assets/handwriting.ttf"

API_WRITE_CMD = "write"        # cloud api style
NOTEBOOK_WRITE_CMD = "nwrite"  # notebook handwriting style

# ==========================================


def small_caps(text: str):
    # basic smallcap feel without unicode break
    return text.lower()


# ---------- NOTEBOOK IMAGE LOGIC ----------
def write_on_page(text):
    img = Image.open(PAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, 38)

    left_margin = 140
    top_margin = 155
    line_gap = 58
    max_width = 60

    lines = textwrap.wrap(text, width=max_width)

    y = top_margin
    for line in lines:
        draw.text((left_margin, y), line, fill=(35, 35, 35), font=font)
        y += line_gap

    out = f"/tmp/write_{uuid.uuid4().hex}.jpg"
    img.save(out, "JPEG", quality=95)
    return out


# ---------- API WRITE ----------
@app.on_message(filters.command(API_WRITE_CMD))
async def api_write(_, message: Message):
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    elif len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    else:
        return await message.reply("❌ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴏʀ ᴡʀɪᴛᴇ ᴛᴇxᴛ")

    m = await message.reply_text("✍️ ᴡʀɪᴛɪɴɢ...")

    try:
        url = requests.get(
            "https://apis.xditya.me/write",
            params={"text": text},
            timeout=10
        ).url

        caption = small_caps(
            f"""
successfully written text ✨
🥀 requested by : {message.from_user.mention}
"""
        )

        await m.delete()
        await message.reply_photo(photo=url, caption=caption)

    except Exception as e:
        await m.edit(f"⚠️ error:\n`{e}`")


# ---------- NOTEBOOK WRITE ----------
@app.on_message(filters.command(NOTEBOOK_WRITE_CMD))
async def notebook_write(_, message: Message):
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    elif len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    else:
        return await message.reply("❌ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴏʀ ᴡʀɪᴛᴇ ᴛᴇxᴛ")

    m = await message.reply("📖 ᴡʀɪᴛɪɴɢ ʟɪᴋᴇ ɴᴏᴛᴇʙᴏᴏᴋ...")

    try:
        img = write_on_page(text)

        caption = small_caps(
            f"""
handwritten notebook text ✅
🥀 requested by : {message.from_user.mention}
"""
        )

        await message.reply_photo(img, caption=caption)
        os.remove(img)
        await m.delete()

    except Exception as e:
        await m.edit(f"⚠️ error:\n`{e}`")


# ================= HELP =================

__MODULE__ = "ᴡʀɪᴛᴇ"

__HELP__ = """
**COMMANDS**:
- /write → ᴄʟᴏᴜᴅ sᴛʏʟᴇ ᴡʀɪᴛɪɴɢ
- /nwrite → ɴᴏᴛᴇʙᴏᴏᴋ ʜᴀɴᴅᴡʀɪᴛɪɴɢ

**USAGE**:
- ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ
- ᴏʀ ᴜsᴇ:  
  `/write text`  
  `/nwrite text`

**INFO**:
- ʟᴏᴄᴀʟ + ᴀᴘɪ ʙᴏᴛʜ sᴜᴘᴘᴏʀᴛᴇᴅ
- ғᴜʟʟ ʜᴅ ɪᴍᴀɢᴇ
- ɴᴏ ʀᴀᴛᴇ ʟɪᴍɪᴛ

**NOTE**:
- ɴᴏᴛᴇʙᴏᴏᴋ ᴍᴏᴅᴇ ʀᴇǫᴜɪʀᴇs `page.jpg` & `handwriting.ttf`
"""
