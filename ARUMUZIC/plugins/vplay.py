import asyncio
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import AudioVideoPiped, HighQualityAudio, HighQualityVideo
from ARUMUZIC.clients import bot, call
from urllib.parse import quote

# Token fixed as per your data
NUB_TOKEN = "pePKYb9ltY"

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
        return await message.reply("❌ **ɢɪᴠᴇ ᴀ ǫᴜᴇʀʏ!** (Example: /vplay starboy)")
    
    query = message.text.split(None, 1)[1].strip()
    m = await message.reply("<blockquote>🎬 <b>sᴇᴀʀᴄʜɪɴɢ...</b></blockquote>")

    # API URL for /info (Direct Search + Stream)
    api_url = f"http://api.nubcoder.com/info?token={NUB_TOKEN}&q={quote(query)}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=20) as resp:
                data = await resp.json()
                
        # --- DEBUGGING & FIXING ---
        # Agar /info directly link nahi deta, toh data check karo
        if not data or "link" not in data:
            # TRYING BACKUP SEARCH (If direct info fails)
            search_url = f"http://api.nubcoder.com/search?q={quote(query)}"
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url) as s_resp:
                    s_data = await s_resp.json()
                    if s_data and len(s_data) > 0:
                        # Pehla result uthao aur uska stream URL lo
                        video_id = s_data[0].get("id")
                        api_url = f"http://api.nubcoder.com/info?token={NUB_TOKEN}&q={video_id}"
                        async with session.get(api_url) as final_resp:
                            data = await final_resp.json()

        if not data or "link" not in data:
            return await m.edit("❌ **sᴛʀᴇᴀᴍ ʟɪɴᴋ ɴᴏᴛ ғᴏᴜɴᴅ! ᴛʀʏ ᴀɴᴏᴛʜᴇʀ sᴏɴɢ.**")

        video_url = data.get("link")
        title = data.get("title", "Video")
        thumb = data.get("thumbnail") or "https://files.catbox.moe/cu442f.jpg"

        try:
            # Play Logic
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
