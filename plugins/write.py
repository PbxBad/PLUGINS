from pyrogram import filters
from BADMUSIC import app
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import uuid

FONT_PATH = "assets/font.ttf"


def create_write_image(text: str):
    width, height = 1080, 1080
    bg_color = (245, 245, 245)
    text_color = (20, 20, 20)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    font_size = 55
    font = ImageFont.truetype(FONT_PATH, font_size)

    # Auto wrap text
    lines = textwrap.wrap(text, width=25)

    total_height = sum(
        draw.textbbox((0, 0), line, font=font)[3] for line in lines
    ) + (len(lines) * 10)

    y = (height - total_height) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2]
        x = (width - text_width) // 2

        draw.text((x, y), line, font=font, fill=text_color)
        y += bbox[3] + 10

    path = f"/tmp/write_{uuid.uuid4().hex}.jpg"
    img.save(path, "JPEG")
    return path


@app.on_message(filters.command("write"))
async def write_handler(client, message):
    if message.reply_to_message and message.reply_to_message.text:
        txt = message.reply_to_message.text
    elif len(message.command) > 1:
        txt = message.text.split(None, 1)[1]
    else:
        return await message.reply(
            "❌ **Reply to text or use** `/write your text`"
        )

    m = await message.reply("✍️ Writing on cloud...")

    try:
        img_path = create_write_image(txt)
        await message.reply_photo(photo=img_path)
        os.remove(img_path)
        await m.delete()

    except Exception as e:
        await m.edit(f"⚠️ Error:\n`{e}`")


__MODULE__ = "ᴡʀɪᴛᴇ"
__HELP__ = """
**COMMANDS**:
- /write: ᴡʀɪᴛᴇ ᴛᴇxᴛ ᴏɴ ᴀɴ ᴄʟᴏᴜᴅ ᴀɴᴅ ɢᴇᴛ ᴀɴ ᴇᴅɪᴛᴇᴅ ᴘʜᴏᴛᴏ.

**INFO**:
- ᴍᴏᴅᴜʟᴇ ɴᴀᴍᴇ: ᴡʀɪᴛᴇ
- ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴡʀɪᴛᴇ ᴛᴇxᴛ ᴏɴ ᴀɴ ᴄʟᴏᴜᴅ ᴀɴᴅ ɢᴇᴛ ᴀɴ ᴇᴅɪᴛᴇᴅ ᴘʜᴏᴛᴏ.
- ᴄᴏᴍᴍᴀɴᴅs: /write
- ᴘᴇʀᴍɪssɪᴏɴs ɴᴇᴇᴅᴇᴅ: ɴᴏɴᴇ

**NOTE**:
- ᴜsᴇ ᴅɪʀᴇᴄᴛʟʏ ɪɴ ᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴡɪᴛʜ ᴍᴇ ғᴏʀ ᴛʜᴇ ʙᴇsᴛ ʀᴇsᴜʟᴛs."""
