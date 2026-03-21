import asyncio
import os
import importlib
from pyrogram import idle, Client
from ARUMUZIC.clients import bot, assistant, call 
import config

async def start_bot():
    print("🚀 Starting ARUMUZIC Clients...")
    
    # --- CLIENTS START ---
    await bot.start()
    await assistant.start()
    await call.start()

    # --- PLUGINS AUTO-LOADER ---
    # Ye folder ke andar ki saari files ko load karega
    plugins_path = "ARUMUZIC/plugins"
    if os.path.exists(plugins_path):
        for file in os.listdir(plugins_path):
            if file.endswith(".py") and not file.startswith("__"):
                module_path = f"ARUMUZIC.plugins.{file[:-3]}"
                try:
                    importlib.import_module(module_path)
                    print(f"✅ Loaded: {file}")
                except Exception as e:
                    print(f"❌ Failed to load {file}: {e}")

    print("---------------------------------")
    print("✨ ARUMUZIC IS NOW ONLINE! ✨")
    print("✅ ALL MODULES LOADED")
    print("---------------------------------")
    
    await idle()
    
    # Stopping clients on exit
    await bot.stop()
    await assistant.stop()
    await call.stop()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("\n🛑 Bot Stopped.")
