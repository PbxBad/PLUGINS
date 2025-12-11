from pymongo import MongoClient
from config import MONGO_DB_URI, DB_NAME
from BADMUSIC import app

client = MongoClient(MONGO_DB_URI)
db = client[DB_NAME]

coupledb = db.couple
karmadb = db.karma

async def get_image(cid: int):
    """Get stored couple image for a chat"""
    chat_data = coupledb.get(cid, {})
    image = chat_data.get("img", "")
    return image

async def _get_lovers(chat_id: int):
    """Get all lovers data for a chat"""
    lovers = coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers

async def get_couple(chat_id: int, date: str):
    """Get couple for a specific date"""
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False

async def save_couple(chat_id: int, date: str, couple: dict):
    """Save couple data to database"""
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    coupledb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"couple": lovers}}, 
        upsert=True
    )
