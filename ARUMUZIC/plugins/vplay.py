import asyncio
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import AudioVideoPiped, HighQualityAudio, HighQualityVideo
from ARUMUZIC.clients import bot, call
from ARUMUZIC.utils.queue import put # Aapka existing queue function
from urllib.parse import quote
import config

# --- BUTTONS CONFIG ---
def get_v_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Ⅱ ᴘᴀᴜsᴇ", callback_data="pause_cb"),
            InlineKeyboardButton("▷ ʀᴇsᴜᴍᴇ", callback_data="resume_cb"),
            InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="skip_cb")
        ],
        [
            InlineKeyboardButton("▢ sᴛᴏᴘ", callback_data="stop_cb"),
            InlineKeyboardButton("🗑️ ᴄʟᴏsᴇ", callback_data="close_cb")
        ]
    ])

@bot.on_message(filters.command(["vplay", "video"]) & filters.group)
async def vplay_cmd(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if len(message.command) < 2:
        return await message.reply("❌ **ɢɪᴠᴇ ᴀ ǫᴜᴇʀʏ ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏ!**")
    
    query = message.text.split(None, 1)[1].strip()
    m = await message.reply("<blockquote>🎬 <b>ғᴇᴛᴄʜɪɴɢ ᴠɪᴅᴇᴏ...</b></blockquote>")

    # --- NUBCODER API INTEGRATION ---
    # Token: pePKYb9ltY
    api_call_url = f"http://api.nubcoder.com/info?token=pePKYb9ltY&q={quote(query)}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_call_url, timeout=20) as resp:
                data = await resp.json()
                
        if not data or "link" not in data:
            return await m.edit("❌ **ᴠɪᴅᴇᴏ ɴᴏᴛ ғᴏᴜɴᴅ ᴏʀ ᴀᴘɪ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ!**")

        video_url = data.get("link")
        title = data.get("title", "Unknown Video")
        duration = data.get("duration", "00:00")
        thumb = data.get("thumbnail") # Thumbnail seedha API se

        # --- QUEUE & PLAY LOGIC ---
        if await call.get_call(chat_id):
            try:
                # Adding to your existing queue system
                await put(chat_id, video_url, title, thumb, duration, user_id, "video")
                return await m.edit(f"➕ **ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ:**\n`{title}`")
            except Exception as e:
                return await m.edit(f"❌ **ǫᴜᴇᴜᴇ ᴇʀʀᴏʀ:** `{e}`")

        # --- START PLAYING ---
        try:
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(
                    video_url,
                    HighQualityAudio(),
                    HighQualityVideo()
                )
            )
            
            await m.delete()
            
            caption = (
                f"<b>❍ sᴛᴀʀᴛᴇᴅ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍɪɴɢ |</b>\n\n"
                f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href='{video_url}'>{title}</a>\n"
                f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> <code>{duration}</code>\n"
                f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n"
                f"<b>‣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : ɴᴜʙᴄᴏᴅᴇʀ ᴀᴘɪ</b>"
            )
            
            await bot.send_photo(
                chat_id,
                photo=thumb, # API ka thumbnail
                caption=caption,
                reply_markup=get_v_buttons() # Yahan buttons add ho gaye
            )

        except Exception as e:
            await m.edit(f"❌ **ᴠᴄ ᴇʀʀᴏʀ:** `{e}`")

    except Exception as e:
        await m.edit(f"❌ **ᴀᴘɪ sᴇʀᴠᴇʀ ᴇʀʀᴏʀ:** `{e}`")
