# Couples.py - Fully Fixed & Cleaned (Only runs on command, not on normal text)
# Copyright (C) 2024 by Badhacker98@Github
# Owner: https://t.me/ll_BAD_MUNDA_ll

import os
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw

from pyrogram import filters
from pyrogram.enums import ChatAction
from BADMUSIC import app
from utils.couple import get_couple, save_couple


# ====================== Date Functions ======================
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    return dt_string.split(" ")

def dt_tom():
    d, m, y = dt()[0].split("/")
    return f"{int(d)+1:02d}/{m}/{y}"

today = dt()[0].split(" ")[0]  # Only date part
tomorrow = dt_tom()

# ====================== Constants ======================
COUPLES_PIC = "https://envs.sh/n4c.jpg"
FALLBACK_PFP = "resources/image/C/coupless.png"
BG_FOLDER = "assets/image/C/"

OWNER_ID = "7616808278"

CAPTION_TEXT = """
✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴛʜᴇ ᴅᴀʏ ✧
❍═══════════════════❍
{} + {} = 💞
❍═══════════════════❍
ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {}
"""

OWNER_SPECIAL = """
✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧
❍═══════════════════❍
{} + ( PGM[](https://t.me/BadMundaXD) + 花火[](https://t.me/JXTT_5911) + ゼロツー[](https://t.me/PBX_CHAT) ) = 💞
❍═══════════════════❍
ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {}
"""


# ====================== Image Creator ======================
async def create_couple_image(c1_id, c2_id, chat_id):
    try:
        user1 = await app.get_chat(c1_id)
        user2 = await app.get_chat(c2_id)

        photo1 = user1.photo.big_file_id if user1.photo else None
        photo2 = user2.photo.big_file_id if user2.photo else None

        p1 = FALLBACK_PFP
        p2 = FALLBACK_PFP

        if photo1:
            try:
                p1 = await app.download_media(photo1, file_name=f"pfp1_{chat_id}.png")
            except:
                p1 = FALLBACK_PFP
        if photo2:
            try:
                p2 = await app.download_media(photo2, file_name=f"pfp2_{chat_id}.png")
            except:
                p2 = FALLBACK_PFP

        img1 = Image.open(p1).resize((680, 680))
        img2 = Image.open(p2).resize((680, 680))

        # Circular mask
        mask = Image.new("L", (680, 680), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 680, 680), fill=255)
        img1.putalpha(mask)
        img2.putalpha(mask)

        # Random background
        bg_files = [f for f in os.listdir(BG_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and f.startswith("Bad")]
        if not bg_files:
            return None
        bg_path = os.path.join(BG_FOLDER, random.choice(bg_files))
        bg = Image.open(bg_path).convert("RGBA")

        # Paste pfps
        bg.paste(img1, (185, 359), img1)
        bg.paste(img2, (1696, 359), img2)

        output = f"couple_{chat_id}_{random.randint(1,9999)}.png"
        bg.save(output)

        # Cleanup temp pfps
        for f in [f"pfp1_{chat_id}.png", f"pfp2_{chat_id}.png"]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass

        return output

    except Exception as e:
        print(f"Image Error: {e}")
        return None


# ====================== Main Command (FIXED!) ======================
@app.on_message(filters.command(["couple", "couples", "lover", "shipping"]))
async def nibba_nibbi(client, message):
    if message.from_user.id == OWNER_ID:
        me = await client.get_users(OWNER_ID)
        return await message.reply_photo(
            photo=COUPLES_PIC,
            caption=OWNER_SPECIAL.format(me.mention, tomorrow)
        )

    try:
        chat_id = message.chat.id
        loading = await message.reply_text("❤️")

        couple = await get_couple(chat_id, today)

        if not couple:
            members = []
            async for m in client.get_chat_members(chat_id, limit=100):
                if not m.user.is_bot:
                    members.append(m.user.id)

            if len(members) < 2:
                return await loading.edit("ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴛᴏ ᴍᴀᴋᴇ ᴀ ᴄᴏᴜᴘʟᴇ 💔")

            c1_id = random.choice(members)
            c2_id = random.choice(members)
            while c1_id == c2_id:
                c2_id = random.choice(members)

            c1 = await client.get_users(c1_id)
            c2 = await client.get_users(c2_id)

            await save_couple(chat_id, today, {"c1_id": c1_id, "c2_id": c2_id})
        else:
            c1_id = int(couple["c1_id"])
            c2_id = int(couple["c2_id"])
            c1 = await client.get_users(c1_id)
            c2 = await client.get_users(c2_id)

        # Generate image
        await client.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
        img_path = await create_couple_image(c1_id, c2_id, chat_id)

        next_reset = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

        caption = CAPTION_TEXT.format(c1.mention, c2.mention, next_reset)

        if img_path and os.path.exists(img_path):
            await message.reply_photo(photo=img_path, caption=caption)
            try:
                os.remove(img_path)
            except:
                pass
        else:
            await message.reply_photo(photo=COUPLES_PIC, caption=caption)

        await loading.delete()

    except Exception as e:
        print(f"Couples Error: {e}")
        try:
            await message.reply_text("ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴄʜᴏᴏsɪɴɢ ᴄᴏᴜᴘʟᴇ 😔")
        except:
            pass
