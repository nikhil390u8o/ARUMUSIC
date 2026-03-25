import asyncio
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import AudioVideoPiped, HighQualityAudio, HighQualityVideo
from ARUMUZIC.clients import bot, call
from urllib.parse import quote
import config

# --- SIMPLE BUTTONS ---
def get_v_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Ⅱ ᴘᴀᴜsᴇ", callback_data="pause_cb"),
            InlineKeyboardButton("▷ ʀᴇsᴜᴍᴇ", callback_data="resume_cb")
        ],
        [
            InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="skip_cb"),
            InlineKeyboardButton("▢ sᴛᴏᴘ", callback_data="stop_cb")
        ]
    ])

@bot.on_message(filters.command(["vplay", "video"]) & filters.group)
async def vplay_cmd(client, message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name if message.from_user else "User"
    
    if len(message.command) < 2:
        return await message.reply("❌ **ɢɪᴠᴇ ᴀ ǫᴜᴇʀʏ!**")
    
    query = message.text.split(None, 1)[1].strip()
    m = await message.reply("<blockquote>🎬 <b>ғᴇᴛᴄʜɪɴɢ...</b></blockquote>")

    # API Token directly using for safety
    api_url = f"http://api.nubcoder.com/info?token=pePKYb9ltY&q={quote(query)}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=20) as resp:
                data = await resp.json()
                
        if not data or "link" not in data:
            return await m.edit("❌ **ɴᴏᴛ ғᴏᴜɴᴅ!**")

        video_url = data.get("link")
        title = data.get("title", "Video")
        thumb = data.get("thumbnail") or "https://files.catbox.moe/cu442f.jpg"

        try:
            # Direct Join (No Queue for now to avoid crash)
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(video_url, HighQualityAudio(), HighQualityVideo())
            )
            
            await m.delete()
            await bot.send_photo(
                chat_id,
                photo=thumb,
                caption=f"<b>🎬 sᴛᴀʀᴛᴇᴅ :</b> <a href='{video_url}'>{title}</a>\n<b>👤 ʙʏ :</b> {user_name}",
                reply_markup=get_v_buttons()
            )

        except Exception as e:
            if "Already in a group call" in str(e):
                await call.change_stream(chat_id, AudioVideoPiped(video_url, HighQualityAudio(), HighQualityVideo()))
                await m.edit(f"✅ **sᴡɪᴛᴄʜᴇᴅ ᴛᴏ:** `{title}`")
            else:
                await m.edit(f"❌ **ᴠᴄ ᴇʀʀᴏʀ:** `{e}`")

    except Exception as e:
        await m.edit(f"❌ **ᴀᴘɪ ᴇʀʀᴏʀ:** `{e}`")
