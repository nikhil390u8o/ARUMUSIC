import asyncio 
import aiohttp
import time
from urllib.parse import quote
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from pytgcalls.types import AudioPiped, HighQualityAudio
from ARUMUZIC.clients import bot, assistant, call 
import config

# --- Utils ---
def fmt_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"

def gen_btn_progressbar(total_sec, current_sec):
    bar_length = 8 
    if total_sec <= 0: total_sec = 1
    percentage = min(100, max(0, (current_sec / total_sec) * 100))
    filled_blocks = int(percentage / (100 / bar_length))
    bar = "▬" * filled_blocks + "●" + "▬" * (bar_length - filled_blocks)
    return f"{fmt_time(current_sec)} {bar} {fmt_time(total_sec)}"

# --- Timer & Loop Logic ---
async def update_timer(chat_id, message_id, duration):
    start_time = time.time()
    while chat_id in config.queues and config.queues[chat_id]:
        await asyncio.sleep(10)
        # Check if paused/stopped
        if chat_id not in config.queues or not config.queues[chat_id]: break
        
        elapsed_time = min(duration, int(time.time() - start_time))
        new_prog = gen_btn_progressbar(duration, elapsed_time)
        
        try:
            await bot.edit_message_reply_markup(
                chat_id, message_id,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=new_prog, callback_data="prog_update")],
                    [
                        InlineKeyboardButton("▷", callback_data="resume_cb"),
                        InlineKeyboardButton("Ⅱ", callback_data="pause_cb"),
                        InlineKeyboardButton("⏭", callback_data="skip_cb"),
                        InlineKeyboardButton("▢", callback_data="stop_cb")
                    ],
                    [
                        InlineKeyboardButton("⏮ -20s", callback_data="seek_back"),
                        InlineKeyboardButton("↺", callback_data="replay_cb"),
                        InlineKeyboardButton("+20s ⏭", callback_data="seek_forward")
                    ],
                    [
                        InlineKeyboardButton("ᴏᴡɴᴇʀ↗", url="https://t.me/ll_PANDA_BBY_ll"),
                        InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ↗", url="https://t.me/sxyaru")
                    ]
                ])
            )
            if elapsed_time >= duration:
                # Auto Play Next when finished
                config.queues[chat_id].pop(0)
                await play_next(chat_id)
                break
        except: break

# --- Core Functions ---
async def play_next(chat_id: int):
    if chat_id not in config.queues or not config.queues[chat_id]:
        await call.leave_group_call(chat_id)
        return

    song = config.queues[chat_id][0]
    title, url, duration, user = song["title"], song["url"], song["duration"], song["by"]
    
    try:
        await call.change_stream(chat_id, AudioPiped(url, HighQualityAudio()))
        
        # New Player Menu for Next Song
        text = f"<b>❍ Nᴇxᴛ Sᴏɴɢ Sᴛᴀʀᴛᴇᴅ |</b>\n\n<b>‣ Tɪᴛʟᴇ :</b> {title}\n<b>‣ Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> `{user}`"
        btn_prog = gen_btn_progressbar(duration, 0)
        
        # Same buttons logic
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text=btn_prog, callback_data="prog_update")],
            [InlineKeyboardButton("▷", "resume_cb"), InlineKeyboardButton("Ⅱ", "pause_cb"), InlineKeyboardButton("⏭", "skip_cb"), InlineKeyboardButton("▢", "stop_cb")],
            [InlineKeyboardButton("⏮ -20s", "seek_back"), InlineKeyboardButton("↺", "replay_cb"), InlineKeyboardButton("+20s ⏭", "seek_forward")],
            [InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/ll_PANDA_BBY_ll"), InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sxyaru")]])
        
        pmp = await bot.send_photo(chat_id, photo="https://files.catbox.moe/uyum1c.jpg", caption=text, reply_markup=buttons)
        asyncio.create_task(update_timer(chat_id, pmp.id, duration))
    except Exception as e:
        print(f"Play Next Error: {e}")

@Client.on_message(filters.command("play") & filters.group)
async def play_cmd(client, msg: Message):
    try: await msg.delete()
    except: pass
    
    chat_id = msg.chat.id
    user_name = msg.from_user.first_name if msg.from_user else "User"

    # Assistant Check
    try:
        ast_info = await assistant.get_me()
        try:
            ast_member = await client.get_chat_member(chat_id, ast_info.id)
            if ast_member.status == ChatMemberStatus.BANNED:
                return await msg.reply(f"❌ Assistant Banned. ID: `{ast_info.id}`")
        except:
            link = await client.export_chat_invite_link(chat_id)
            await assistant.join_chat(link)
    except: pass

    if len(msg.command) < 2: return await msg.reply("❌ Give query!")
    query = msg.text.split(None, 1)[1].strip()
    m = await msg.reply("🔎 Searching...")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://jio-saa-van.vercel.app/result/?query={quote(query)}") as r:
            data = await r.json()

    if not data: return await m.edit("❌ No results.")
    track = data[0]
    title, duration = track.get("song"), int(track.get("duration", 0))
    stream_url = track.get("media_url") or track.get("download_url")

    song_data = {"title": title, "url": stream_url, "duration": duration, "by": user_name}
    
    # Queue Management Logic
    if chat_id in config.queues and len(config.queues[chat_id]) > 0:
        config.queues[chat_id].append(song_data)
        await m.edit(f"✅ **ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ (ᴘᴏsɪᴛɪᴏɴ #{len(config.queues[chat_id])-1})**\n🎵 **ᴛɪᴛʟᴇ:** {title}")
        return

    config.queues.setdefault(chat_id, []).append(song_data)
    await m.delete()

    # Play First Song
    await call.join_group_call(chat_id, AudioPiped(stream_url, HighQualityAudio()))
    
    text = f"<b>❍ Sᴛᴀʀᴛᴇᴅ Sᴛʀᴇᴀᴍɪɴɢ |</b>\n\n<b>‣ Tɪᴛʟᴇ :</b> {title}\n<b>‣ Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> `{user_name}`"
    btn_prog = gen_btn_progressbar(duration, 0)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text=btn_prog, callback_data="prog_update")],
        [InlineKeyboardButton("▷", "resume_cb"), InlineKeyboardButton("Ⅱ", "pause_cb"), InlineKeyboardButton("⏭", "skip_cb"), InlineKeyboardButton("▢", "stop_cb")],
        [InlineKeyboardButton("⏮ -20s", "seek_back"), InlineKeyboardButton("↺", "replay_cb"), InlineKeyboardButton("+20s ⏭", "seek_forward")],
        [InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/ll_PANDA_BBY_ll"), InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sxyaru")]])

    pmp = await client.send_photo(chat_id, photo="https://files.catbox.moe/uyum1c.jpg", caption=text, reply_markup=buttons)
    asyncio.create_task(update_timer(chat_id, pmp.id, duration))
