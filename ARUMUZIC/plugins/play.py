import asyncio 
import aiohttp
import time
import re
from urllib.parse import quote
from pyrogram.enums import ChatMemberStatus
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import AudioVideoPiped, HighQualityAudio, HighQualityVideo
from ARUMUZIC.clients import bot, assistant, call 
import config

# --- Configuration for Queues ---
if not hasattr(config, "queues"):
    config.queues = {}

# --- API Config ---
NUB_TOKEN = "pePKYb9ltY"
API_URL = "http://api.nubcoder.com/info"

# --- Utils ---
def fmt_time(seconds):
    try:
        seconds = int(seconds)
    except:
        return "00:00"
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"

def gen_btn_progressbar(total_sec, current_sec):
    try:
        total_sec = int(total_sec)
    except:
        total_sec = 1
    bar_length = 10 
    percentage = min(100, max(0, (current_sec / total_sec) * 100))
    filled_blocks = int(percentage / (100 / bar_length))
    bar = "▰" * filled_blocks + "▱" * (bar_length - filled_blocks)
    return f"{fmt_time(current_sec)} {bar} {fmt_time(total_sec)}"

# --- PLAYER BUTTONS ---
def get_player_buttons(duration, elapsed=0):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=gen_btn_progressbar(duration, elapsed), callback_data="prog_update")],
        [
            InlineKeyboardButton("▷", "resume_cb"), 
            InlineKeyboardButton("Ⅱ", "pause_cb"), 
            InlineKeyboardButton("↺", "replay_cb"), 
            InlineKeyboardButton("⏭", "skip_cb"), 
            InlineKeyboardButton("▢", "stop_cb")
        ],
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/ll_PANDA_BBY_ll"), 
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sxyaru")
        ],
        [InlineKeyboardButton("🗑️ ᴄʟᴏsᴇ", callback_data="close_cb")]
    ])

# --- Play Next Function ---
async def play_next(chat_id: int):
    if chat_id not in config.queues or len(config.queues[chat_id]) <= 1:
        config.queues[chat_id] = []
        try:
            await call.leave_group_call(chat_id)
        except:
            pass
        return

    config.queues[chat_id].pop(0) 
    song = config.queues[chat_id][0] 
    title = song["title"]
    stream_url = song["url"]
    duration = song["duration"]
    user_name = song["by"]
    thumbnail = song["thumb"]

    try:
        await call.change_stream(
            chat_id, 
            AudioVideoPiped(stream_url, HighQualityAudio(), HighQualityVideo())
        )
        
        text = (
            f"<b>❍ Sᴛᴀʀᴛᴇᴅ Sᴛʀᴇᴀᴍɪɴɢ |</b>\n\n"
            f"<b>‣ Tɪᴛʟᴇ :</b> <a href='{stream_url}'>{title}</a>\n"
            f"<b>‣ Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> `{user_name}`"
        )
        
        pmp = await bot.send_photo(chat_id, photo=thumbnail, caption=text, reply_markup=get_player_buttons(duration))
        asyncio.create_task(update_timer(chat_id, pmp.id, duration))
    except:
        await play_next(chat_id)

@call.on_stream_end()
async def stream_end_handler(_, update):
    chat_id = update.chat_id
    if chat_id in config.queues and len(config.queues[chat_id]) > 1:
        await play_next(chat_id)
    else:
        try:
            config.queues[chat_id] = [] 
            await call.leave_group_call(chat_id)
        except:
            pass

async def update_timer(chat_id, message_id, duration):
    start_time = time.time()
    try:
        total_d = int(duration)
    except:
        total_d = 1
        
    while True:
        await asyncio.sleep(12) 
        if chat_id not in config.queues or not config.queues[chat_id]:
            break
        
        elapsed_time = int(time.time() - start_time)
        
        if elapsed_time >= total_d:
            try:
                await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=get_player_buttons(total_d, total_d))
            except:
                pass
            break 
            
        try:
            await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=get_player_buttons(total_d, elapsed_time))
        except: 
            break

# --- MAIN PLAY COMMAND ---
@bot.on_message(filters.command(["play", "p"]) & filters.group)
async def play_cmd(client, msg: Message):
    try:
        await msg.delete()
    except:
        pass
    
    chat_id = msg.chat.id
    user_name = msg.from_user.first_name if msg.from_user else "User"
    if len(msg.command) < 2: 
        return await msg.reply("❌ **ɢɪᴠᴇ ᴀ ǫᴜᴇʀʏ!**")
    
    query = msg.text.split(None, 1)[1].strip()
    m = await msg.reply("<blockquote>🔎 <b>sᴇᴀʀᴄʜɪɴɢ...</b></blockquote>")

    # Assistant Join Logic
    try:
        ast_me = await assistant.get_me()
        ast_id = ast_me.id
        try:
            ast_member = await client.get_chat_member(chat_id, ast_id)
            if ast_member.status == ChatMemberStatus.BANNED:
                await client.unban_chat_member(chat_id, ast_id)
        except:
            pass
        
        # Invite Link Logic
        invitelink = await client.export_chat_invite_link(chat_id)
        await assistant.join_chat(invitelink)
    except:
        pass

    # API SEARCH
    try:
        api_call = f"{API_URL}?token={NUB_TOKEN}&q={quote(query)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_call, timeout=20) as r:
                data = await r.json()

        if not data or "stream_url" not in data:
            return await m.edit("❌ **ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ!**")

        title = data.get("title", "Video Stream")
        stream_url = data.get("stream_url")
        thumb_url = data.get("thumbnail") 
        
        raw_dur = data.get("duration", "0")
        if ":" in str(raw_dur):
            p = str(raw_dur).split(":")
            duration = int(p[0]) * 60 + int(p[1]) if len(p) == 2 else int(p[0])*3600 + int(p[1])*60 + int(p[2])
        else:
            duration = int(raw_dur)

    except Exception as e:
        return await m.edit(f"❌ **ᴀᴘɪ ᴇʀʀᴏʀ:** `{e}`")

    song_data = {"title": title, "url": stream_url, "duration": duration, "by": user_name, "thumb": thumb_url}

    if chat_id not in config.queues:
        config.queues[chat_id] = []

    if len(config.queues[chat_id]) > 0:
        try:
            await call.get_call(chat_id)
            config.queues[chat_id].append(song_data)
            return await m.edit(f"<b>✅ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ (#{len(config.queues[chat_id])-1})</b>\n🎵 {title}")
        except:
            config.queues[chat_id] = []

    config.queues[chat_id].append(song_data)
    await m.delete()

    try:
        await call.join_group_call(chat_id, AudioVideoPiped(stream_url, HighQualityAudio(), HighQualityVideo()))
        
        cap = (
            f"<b>❍ Sᴛᴀʀᴛᴇᴅ Sᴛʀᴇᴀᴍɪɴɢ |</b>\n\n"
            f"<b>‣ Tɪᴛʟᴇ :</b> <a href='{stream_url}'>{title}</a>\n"
            f"<b>‣ Dᴜʀᴀᴛɪᴏɴ :</b> <code>{fmt_time(duration)}</code>\n"
            f"<b>‣ Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> `{user_name}`"
        )

        pmp = await bot.send_photo(chat_id, photo=thumb_url, caption=cap, reply_markup=get_player_buttons(duration))
        asyncio.create_task(update_timer(chat_id, pmp.id, duration))

    except Exception as e:
        config.queues[chat_id] = []
        await bot.send_message(chat_id, f"❌ **Error:** `{e}`")
