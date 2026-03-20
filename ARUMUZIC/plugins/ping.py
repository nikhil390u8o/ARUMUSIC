import time
import psutil
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ARUMUZIC.clients import bot # Import the actual bot instance
import config

# Bot kab start hua uske liye ek fallback (agar config mein na ho)
START_TIME = datetime.now()

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

@Client.on_message(filters.command("ping"))
async def ping_cmd(client, msg: Message):
    # Command delete karne ka try
    try:
        await msg.delete()
    except:
        pass

    start_time = time.time()
    
    # Typing action aur initial message
    m = await msg.reply_text("<code>ᴘɪɴɢɪɴɢ..</code>")
    
    # Latency calculation
    end_time = time.time()
    latency = round((end_time - start_time) * 1000, 2)
    
    # Uptime calculation (Safe Way)
    bot_uptime = getattr(config, "BOT_START_TIME", START_TIME)
    uptime_sec = (datetime.now() - bot_uptime).total_seconds()
    uptime = get_readable_time(int(uptime_sec))
    
    # System Stats
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    text = (
        "<b>🏓 ᴘᴏɴɢ! sᴛᴀᴛs ᴀʀᴇ ʜᴇʀᴇ</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 <b>ʟᴀᴛᴇɴᴄʏ:</b> <code>{latency} ms</code>\n"
        f"🆙 <b>ᴜᴘᴛɪᴍᴇ:</b> <code>{uptime}</code>\n"
        f"💻 <b>ᴄᴘᴜ:</b> <code>{cpu}%</code>\n"
        f"📊 <b>ʀᴀᴍ:</b> <code>{ram}%</code>\n"
        f"💾 <b>ᴅɪsᴋ:</b> <code>{disk}%</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👤 <b>ᴏᴡɴᴇʀ:</b> <a href='https://t.me/sxyaru'>ᴀʀᴜ × ᴀᴘɪ [ʙᴏᴛs]</a>"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sxyaru"),
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/ll_PANDA_BBY_ll")
        ]
    ])

    PING_IMG = "https://files.catbox.moe/nacfzm.jpg" 
    
    # Pehle wala "Pinging..." delete karo aur naya photo bhejo
    await m.delete()
    await client.send_photo(
        msg.chat.id,
        photo=PING_IMG,
        caption=text,
        reply_markup=buttons
    )
