from BADMUSIC import app
import requests, json
from pyrogram import client, filters
from pyrogram.errors import MediaCaptionTooLong
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InputMediaPhoto
from pyrogram.enums import ChatAction, ParseMode
from config import LOG_GROUP_ID

BUTTON = InlineKeyboardMarkup(
       [
              [
                     InlineKeyboardButton(
                            text=f"〆 ᴄʟᴏsᴇ 〆",
                            callback_data="close",
                    )
              ]
       ]
)              

url = "https://nandha-api.onrender.com/ai/bard"

async def send_to_gpt(api_url: str, query: str) -> tuple:
    try:
        response = requests.get(f"{api_url}/{query}")
        response.raise_for_status()
        data = response.json()
        return data.get("content", "No response from the API."), data.get("images", False)
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {e}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

@app.on_message(filters.command(["gemini", "bard"]))
async def bardai(bot, message):
    try:
        chat_id = message.chat.id
        message_id = message.id
        await bot.send_chat_action(chat_id, ChatAction.TYPING)
        if message.reply_to_message:
            Msg = message.reply_to_message.text
        else:
            Msg = " ".join(message.command[1:])
        if message.reply_to_message:
            Msg = message.reply_to_message.text + " " + Msg

        api_response, images = await send_to_gpt(url, Msg)

        medias = []
        bard = str(api_response)
        if images:
            if len(images) > 1:
                for image_url in images:
                    medias.append(InputMediaPhoto(media=image_url, caption=None))

                medias[-1] = InputMediaPhoto(media=images[-1], caption=bard)

                try:
                    await app.send_media_group(chat_id=chat_id, media=medias, reply_to_message_id=message_id)
                    return
                except Exception as e:
                    await app.send_message(LOG_GROUP_ID, f"An error occurred in BARD :{str(e)}")
            elif len(images) == 1:
                image_url = images[0]
                try:
                    await message.reply_photo(photo=image_url, caption=bard, reply_markup=BUTTON)
                    return
                except MediaCaptionTooLong:
                    await message.reply_text(bard, reply_markup=BUTTON)
                except Exception as e:
                    await app.send_message(LOG_GROUP_ID, f"An error occurred in bard: {str(e)}")
            else:
                pass
        else:
            try:
                await message.reply_text(bard)
            except Exception as e:
                await app.send_message(LOG_GROUP_ID, f"An error occurred in bard: {str(e)}")
    except Exception as e:
        await app.send_message(LOG_GROUP_ID, f"An unhandled exception bard: {str(e)}")
        
