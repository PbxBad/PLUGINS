# Couples.py
# 1st code with image generation feature added

# Copyright (C) 2024 by Badhacker98@Github, < https://github.com/Badhacker98 >.
# Owner https://t.me/ll_BAD_MUNDA_ll

import os
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw

from pyrogram import filters
from pyrogram.enums import ChatAction

from BADMUSIC import app
from utils.couple import get_couple, save_couple


# <=======================================================================================================================================================================================================================================================================================================================================================================================================================================================================

# <================================================ FUNCTION =======================================================>

def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list

def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a

tomorrow = str(dt_tom())
today = str(dt()[0])

COUPLES_PIC = "https://envs.sh/n4c.jpg"
C = """
✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧
❍═══════════════════❍
{} + ( PGM🎀😶 (https://t.me/BadMundaXD) + 花火 (https://t.me/JXTT_5911) + ゼロツー (https://t.me/PBX_CHAT) ) = 💞
❍═══════════════════❍
ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {}
"""
CAP = """
✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧
❍═══════════════════❍
{} + {} = 💞
❍═══════════════════❍
ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {}
"""

CAP2 = """
✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧
❍═══════════════════❍
{} + {} = 💞
❍═══════════════════❍
ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴄᴀɴ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {}
"""

async def create_couple_image(client, c1_id, c2_id, chat_id):
    """Create couple image with profile pictures"""
    try:
        photo1 = (await client.get_chat(c1_id)).photo
        photo2 = (await client.get_chat(c2_id)).photo
        
        # Download profile pictures
        try:
            p1 = await client.download_media(photo1.big_file_id, file_name=f"pfp_{chat_id}_1.png")
        except Exception:
            p1 = "resources/image/C/coupless.png"
        
        try:
            p2 = await client.download_media(photo2.big_file_id, file_name=f"pfp_{chat_id}_2.png")
        except Exception:
            p2 = "resources/image/C/coupless.png"
        
        # Open images
        img1 = Image.open(p1)
        img2 = Image.open(p2)
        
        # Select random background
        xy = ["Bad1", "Bad2", "Bad3"]
        x = random.choice(xy)
        img = Image.open(f"resources/image/C/{x}.png")
        
        # Resize profile pictures
        img1 = img1.resize((680, 680))
        img2 = img2.resize((680, 680))
        
        # Create circular masks
        mask = Image.new('L', img1.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img1.size, fill=255)
        
        mask1 = Image.new('L', img2.size, 0)
        draw = ImageDraw.Draw(mask1)
        draw.ellipse((0, 0) + img2.size, fill=255)
        
        # Apply masks
        img1.putalpha(mask)
        img2.putalpha(mask1)
        
        # Paste images on background
        img.paste(img1, (185, 359), img1)
        img.paste(img2, (1696, 359), img2)
        
        # Save final image
        output_path = f'couple_{chat_id}.png'
        img.save(output_path)
        
        # Cleanup downloaded files
        try:
            if p1 != "resources/image/C/coupless.png":
                os.remove(p1)
            if p2 != "resources/image/C/coupless.png":
                os.remove(p2)
        except Exception:
            pass
        
        return output_path
    except Exception as e:
        print(f"Error creating couple image: {e}")
        return None

@app.on_message(["couple", "couples", "lover", "shipping"])
async def nibba_nibbi(client, message):
    if message.from_user.id == 5540249238:
        my = await client.get_users("rfxtuv")
        me = await client.get_users(5540249238)
        await message.reply_photo(
            photo=COUPLES_PIC, caption=C.format(me.mention, tomorrow)
        )
    else:
        try:
            chat_id = message.chat.id
            
            # Send loading message
            loading_message = await message.reply_text("❤️")
            
            is_selected = await get_couple(chat_id, today)
            
            if not is_selected:
                list_of_users = []
                async for i in client.get_chat_members(message.chat.id, limit=50):
                    if not i.user.is_bot:
                        list_of_users.append(i.user.id)
                
                if len(list_of_users) < 2:
                    await loading_message.delete()
                    return await message.reply_text("ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")
                
                c1_id = random.choice(list_of_users)
                c2_id = random.choice(list_of_users)
                while c1_id == c2_id:
                    c1_id = random.choice(list_of_users)
                
                c1_mention = (await client.get_users(c1_id)).mention
                c2_mention = (await client.get_users(c2_id)).mention
                
                # Create couple image
                await client.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
                image_path = await create_couple_image(client, c1_id, c2_id, chat_id)
                
                next_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d/%m/%Y 12 AM")
                caption = CAP2.format(c1_mention, c2_mention, next_date)
                
                if image_path and os.path.exists(image_path):
                    await message.reply_photo(photo=image_path, caption=caption)
                    # Cleanup
                    try:
                        os.remove(image_path)
                    except Exception:
                        pass
                else:
                    # Fallback to default image
                    await message.reply_photo(photo=COUPLES_PIC, caption=caption)
                
                await loading_message.delete()
                
                couple = {"c1_id": c1_id, "c2_id": c2_id}
                await save_couple(chat_id, today, couple)
            
            elif is_selected:
                c1_id = int(is_selected["c1_id"])
                c2_id = int(is_selected["c2_id"])
                
                c1_mention = (await client.get_users(c1_id)).mention
                c2_mention = (await client.get_users(c2_id)).mention
                
                # Create couple image
                await client.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
                image_path = await create_couple_image(client, c1_id, c2_id, chat_id)
                
                next_date = (datetime.utcnow() + timedelta(days=1)).strftime("%d/%m/%Y 12 AM")
                caption = CAP2.format(c1_mention, c2_mention, next_date)
                
                if image_path and os.path.exists(image_path):
                    await message.reply_photo(photo=image_path, caption=caption)
                    # Cleanup
                    try:
                        os.remove(image_path)
                    except Exception:
                        pass
                else:
                    # Fallback to default image
                    await message.reply_photo(photo=COUPLES_PIC, caption=caption)
                
                await loading_message.delete()
                
        except Exception as e:
            print(e)
            await message.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {str(e)}")
