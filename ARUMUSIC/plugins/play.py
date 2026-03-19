import time
import math
import psutil
from datetime import datetime, timedelta
import asyncio
import aiohttp
from urllib.parse import quote
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram.errors import FloodWait
from pyrogram import Client, filters, idle
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from pyrogram.enums import ChatMemberStatus # Ye line sabse upar imports mein add kar dena
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import AudioPiped, HighQualityAudio


# --- Ye aapka Updated Play Command hai ---
@bot.on_message(filters.command("play"))
async def play_cmd(_, msg: Message):
    try:
        await msg.delete()
    except:
        pass
    chat_id = msg.chat.id
    user_name = msg.from_user.first_name if msg.from_user else "User"

    # 1. Assistant Status & Admin Checks
    try:
        assistant_info = await assistant.get_me()
        ast_id = assistant_info.id
        ast_username = f"@{assistant_info.username}" if assistant_info.username else "Assistant"
        
        try:
            ast_member = await bot.get_chat_member(chat_id, ast_id)
            if ast_member.status == ChatMemberStatus.BANNED:
                return await msg.reply(f"❌ **ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴ!**\nᴘʟs ᴜɴʙᴀɴ {ast_username} (ɪᴅ: <code>{ast_id}</code>)")
            if ast_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await msg.reply(f"❌ **ᴀssɪsᴛᴀɴᴛ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!**\nᴍᴀᴋᴇ {ast_username} ᴀs ᴀᴅᴍɪɴ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ")
        except Exception as e:
            if "USER_NOT_PARTICIPANT" in str(e):
                m = await msg.reply(f"🔄 **ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ɢʀᴏᴜᴘ...**")
                try:
                    invitelink = await bot.export_chat_invite_link(chat_id)
                    await assistant.join_chat(invitelink)
                    return await m.edit(f"✅ **ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ ᴍᴀᴋᴇ ᴀᴅᴍɪɴ ᴛʜᴇɴ /play**")
                except: return await m.edit("❌ ᴀᴜᴛᴏ ɪɴᴠɪᴛɪɴɢ ғᴀɪʟᴇᴅ ᴀᴅᴅ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴍᴀɴᴜᴀʟʟʏ")
            pass
    except Exception as e:
        return await msg.reply(f"❌ Assistant Error: {e}")

    # 2. Search Logic
    if len(msg.command) < 2:
        return await msg.reply("❌ **ɢɪᴠᴇ ǫᴜᴇʀʏ!**")

    query = msg.text.split(None, 1)[1].strip()
    m = await msg.reply("🔎 <b>sᴇᴀʀᴄʜɪɴɢ...</b>")

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://jio-saa-van.vercel.app/result/?query={quote(query)}"
            async with session.get(url, timeout=12) as r:
                data = await r.json()
    except: return await m.edit("❌ API Error!")

    if not data or len(data) == 0:
        return await m.edit("❌ No results found.")

    track = data[0]
    title = track.get("song", "Unknown")
    duration = int(track.get("duration", 0))
    stream_url = track.get("media_url") or track.get("download_url")
    thumb = "https://files.catbox.moe/uyum1c.jpg"

    # 3. Queue Logic
    song_data = {"title": title, "url": stream_url, "duration": duration, "by": user_name}
    queues.setdefault(chat_id, []).append(song_data)

    # 4. 🔥 CRITICAL STEP: TRY JOINING FIRST 🔥
    # Pehle join karne ki koshish (True/False return)
    # Humein play_next variable mein return status capture karna hai
    try:
        join_status = await play_next(chat_id)
    except:
        join_status = False # play_next failed explicitly

    if not join_status:
        # Agar join fail hua, toh searching message delete karo aur menu mat bhejo
        await m.delete()
        return

    # 5. UI Layout (Buttons set to Small/Compact and Timer fix)
    # gen_btn_progressbar function upar paste kiya hai
    btn_prog = gen_btn_progressbar(duration, 0) 
    
    text = (
        f"<b>❍ Sᴛᴀʀᴛᴇᴅ Sᴛʀᴇᴀᴍɪɴɢ |</b>\n\n"
        f"<b>‣ Tɪᴛʟᴇ :</b> <a href='{stream_url}'>{title}</a>\n"
        f"<b>‣ Dᴜʀᴀᴛɪᴏɴ :</b> <code>{fmt_time(duration)} ᴍs</code>\n"
        f"<b>‣ Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> `{user_name}`\n"
        f"<b>‣ ʙᴏᴛ ʙᴀsᴇᴅ ᴏɴ : ᴀʀᴜ x ᴊɪᴏsᴀᴠᴀɴ</b>\n"
        f"<b>‣ ᴀᴘɪ ʙʏ: <a href='https://t.me/sxyaru'>ᴀʀᴜ × ᴀᴘɪ [ʙᴏᴛs]</a></b>\n"
        f"<b>‣ ᴀᴘɪ ᴍᴀᴅᴇ ʙʏ: <a herf='href=https://t.me/ll_PANDA_BBY_ll'>ᴘᴀɴᴅᴀ-ʙᴀʙʏ</a></b>"
    )

    # Exact Photo Style (Row 2 mein 4 compact buttons)
    buttons = InlineKeyboardMarkup([
        [
            # Row 1: Progress Bar Button (10 blocks)
            InlineKeyboardButton(text=btn_prog, callback_data="prog_update")
        ],
        [
            # Row 2: 4 Buttons (Isse buttons baraber 'Small' dikhenge)
            InlineKeyboardButton("▷", callback_data="resume_cb"),
            InlineKeyboardButton("Ⅱ", callback_data="pause_cb"),
            InlineKeyboardButton("⏭", callback_data="skip_cb"),
            InlineKeyboardButton("▢", callback_data="stop_cb")
        ],
        [
            # Row 3: 3 Buttons
            InlineKeyboardButton("⏮ -20s", callback_data="seek_back"),
            InlineKeyboardButton("↺", callback_data="replay_cb"),
            InlineKeyboardButton("+20s ⏭", callback_data="seek_forward")
        ],
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ↗", url="https://t.me/ll_PANDA_BBY_ll"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ↗", url="https://t.me/sxyaru")
        ]
    ])

    await m.delete()
    
    # 6. SEND PHOTO AND START TIMER
    # Sent message ko pmp capture kiya hai ID timer ko dene ke liye
    pmp = await bot.send_photo(chat_id, photo=thumb, caption=text, reply_markup=buttons)
    
    # Ye line progress bar timer ko background mein start kar degi
    asyncio.create_task(update_timer(chat_id, pmp.id, duration))







async def play_next(chat_id: int):
    # 1. Check karo queue mein gaana hai ya nahi
    if chat_id not in queues or not queues[chat_id]:
        return False
    
    song = queues[chat_id][0]
    url = song["url"]

    try:
        # 2. Assistant ko join ya stream change karwana
        try:
            # Latest version mein 'stream_type' hat gaya hai, 
            # PyTgCalls ab khud handle karta hai.
            await call.join_group_call(
                chat_id,
                AudioPiped(
                    url, 
                    HighQualityAudio() 
                )
            )
        except Exception:
            # Agar pehle se VC mein hai toh sirf stream badlo
            await call.change_stream(
                chat_id,
                AudioPiped(url, HighQualityAudio())
            )
        
        return True
            
    except Exception as e:
        print(f"Assistant Join Error: {e}")
        
        if chat_id in queues:
            queues[chat_id].pop(0)
            
        error_text = f"❌ **Assistant join nahi kar pa raha!**\n\n"
        
        # Latest Error Strings check
        err_msg = str(e).lower()
        if "chat_admin_required" in err_msg:
            error_text += "💡 **Reason:** Assistant ko 'Manage Video Chats' permission do!"
        elif "not in a group call" in err_msg or "group_call_not_modified" in err_msg:
            error_text += "💡 **Reason:** Group mein Voice Chat (VC) start nahi hai!"
        else:
            error_text += f"💬 **Error:** <code>{e}</code>"
            
        await bot.send_message(chat_id, error_text)
        return False
