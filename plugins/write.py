from pyrogram import filters
from BADMUSIC import app
from PIL import Image, ImageDraw, ImageFont
import textwrap, os, uuid

PAGE_PATH = "assets/page.jpg"
FONT_PATH = "assets/font.ttf"


def write_on_page(text):
    img = Image.open(PAGE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, 38)

    # notebook alignment (tuned like your sample)
    left_margin = 140
    top_margin = 155      # first ruled line
    line_gap = 58         # distance between lines
    max_width = 60        # characters per line

    lines = textwrap.wrap(text, width=max_width)

    y = top_margin
    for line in lines:
        draw.text((left_margin, y), line, fill=(30, 30, 30), font=font)
        y += line_gap

    out = f"/tmp/write_{uuid.uuid4().hex}.jpg"
    img.save(out, "JPEG", quality=95)
    return out


@app.on_message(filters.command("write"))
async def write_handler(_, message):
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    elif len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    else:
        return await message.reply(
            "❌ Reply to text or use\n`/write your text`"
        )

    m = await message.reply("✍️ writing like notebook...")

    try:
        img = write_on_page(text)
        await message.reply_photo(img)
        os.remove(img)
        await m.delete()
    except Exception as e:
        await m.edit(f"⚠️ Error:\n`{e}`")
