import asyncio  # 👈 'i' lowercase hona chahiye
from pyrogram import Client, idle
from pytgcalls import PyTgCalls  # 👈 'from pytgcalls' zaroori hai
import config

# 1. Main Bot Client
bot = Client(
    "ARUMUSIC_BOT",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="ARUMUZIC/plugins")
)

# 2. Userbot (Assistant) Client
assistant = Client(
    "ARUMUSIC_ASS",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING
)

# 3. PyTgCalls (Music Engine)
call = PyTgCalls(assistant)

async def start_bot():
    print("🚀 Starting ARUMUSIC Clients...")
    await bot.start()
    await assistant.start()
    
    # Music Engine Start
    await call.start()
    
    print("---------------------------------")
    print("✨ ARUMUSIC IS NOW ONLINE! ✨")
    print("✨ Powered by Arumusic & Panda ✨")
    print("---------------------------------")
    print("✅ ALL MODULES LOADED")
    
    await idle()
    
    # Clean Shutdown
    await bot.stop()
    await assistant.stop()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("\n🛑 Bot Stopped By User.")
