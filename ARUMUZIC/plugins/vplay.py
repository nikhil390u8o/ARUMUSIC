import asyncio
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import AudioVideoPiped, HighQualityAudio, HighQualityVideo
from ARUMUZIC.clients import bot, call
from urllib.parse import quote

# Token & API Config
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
        return await message.reply("❌ **ɢɪᴠᴇ ᴀ ǫᴜᴇʀʏ!**")
    
    query = message.text.split(None, 1)[1].strip()
    m = await message.reply("<blockquote>🎬 <b>ғᴇᴛᴄʜɪɴɢ sᴛʀᴇᴀᴍ...</b></blockquote>")

    # API URL
    api_url = f"http://api.nubcoder.com/info?token={NUB_TOKEN}&q={quote(query)}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=20) as resp:
                data = await resp.json()
                
        # API Response Keys Check (stream_url and thumbnail)
        video_url = data.get("stream_url")
        if not video_url:
            return await m.edit("❌ **sᴛʀᴇᴀᴍ ᴜʀʟ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴀᴘɪ!**")

        title = data.get("title", "Unknown Video")
        thumb = data.get("thumbnail") # Seedha API wala thumbnail
        duration = data.get("duration", "00:00")
        yt_link = data.get("youtube_link", "https://youtube.com")

        try:
            # Pytgcalls Video Streaming
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
                f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href='{yt_link}'>{title}</a>\n"
                f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> <code>{duration}</code>\n"
                f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {user_name}\n"
                f"<b>‣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : ɴᴜʙᴄᴏᴅᴇʀ ᴀᴘɪ</b>"
            )
            
            await bot.send_photo(
                chat_id,
                photo=thumb,
                caption=caption,
                reply_markup=get_v_buttons()
            )

        except Exception as e:
            if "Already in a group call" in str(e):
                await call.change_stream(chat_id, AudioVideoPiped(video_url, HighQualityAudio(), HighQualityVideo()))
                await m.edit(f"✅ **sᴡɪᴛᴄʜᴇᴅ ᴛᴏ:** `{title}`")
            else:
                await m.edit(f"❌ **ᴠᴄ ᴇʀʀᴏʀ:** `{e}`")

    except Exception as e:
        await m.edit(f"❌ **ᴀᴘɪ ᴇʀʀᴏʀ:** `{type(e).__name__}`")
