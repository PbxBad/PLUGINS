import random
import requests
import time
import asyncio

from pyrogram import filters
from pyrogram.enums import PollType, ChatAction
from BADMUSIC import app


# ---------------------------
#  RANDOM QUIZ FETCH FUNCTION
# ---------------------------

async def fetch_quiz(client, message):
    categories = [9, 17, 18, 20, 21, 27]  # GK, Computer, Science, etc.

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
    response = requests.get(url).json()

    question_data = response["results"][0]

    question = question_data["question"]
    correct_answer = question_data["correct_answer"]
    incorrect_answers = question_data["incorrect_answers"]

    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)

    correct_id = all_answers.index(correct_answer)

    await client.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=all_answers,
        is_anonymous=False,
        type=PollType.QUIZ,
        correct_option_id=correct_id,
    )


# ---------------------------
#  SINGLE QUIZ (/quiz)
# ---------------------------

last_time = {}

@app.on_message(filters.command(["quiz"]))
async def quiz_one(client, message):
    user_id = message.from_user.id
    now = time.time()

    if user_id in last_time and now - last_time[user_id] < 5:
        return await message.reply("⏳ Wait 5 seconds before using this again.")

    last_time[user_id] = now

    await fetch_quiz(client, message)



# ---------------------------
#  MULTIPLE QUIZ SENDER
# ---------------------------

async def send_multiple_quiz(client, message, count):
    await message.reply(f"📚 Sending {count} quizzes...\n⏳ 5 seconds gap each!")

    for i in range(count):
        await fetch_quiz(client, message)
        if i != count - 1:
            await asyncio.sleep(5)  # 5 second delay


# ---------------------------
#  /quiz5 → 5 Quizzes
# ---------------------------

@app.on_message(filters.command(["quiz5"]))
async def quiz_five(client, message):
    await send_multiple_quiz(client, message, 5)


# ---------------------------
#  /quiz10 → 10 Quizzes
# ---------------------------

@app.on_message(filters.command(["quiz10"]))
async def quiz_ten(client, message):
    await send_multiple_quiz(client, message, 10)



# ---------------------------
#  HELP & MODULE
# ---------------------------

__MODULE__ = "ǫᴜɪᴢ"
__HELP__ = """
🎯 **QUIZ COMMANDS**

/quiz - Send 1 random quiz  
/quiz5 - Auto send 5 quizzes (5 sec gap)  
/quiz10 - Auto send 10 quizzes (5 sec gap)  

Random categories include GK, Computer, Science, Mythology & more.
"""
