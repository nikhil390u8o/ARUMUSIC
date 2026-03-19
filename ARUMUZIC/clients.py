# ARUMUZIC/clients.py
from pyrogram import Client
from pytgcalls import PyTgCalls
import config

bot = Client(
    "ARUMUSIC_BOT",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="ARUMUZIC/plugins")
)

assistant = Client(
    "ARUMUSIC_ASS",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING
)

call = PyTgCalls(assistant)
