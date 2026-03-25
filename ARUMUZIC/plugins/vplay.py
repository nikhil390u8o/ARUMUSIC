import asyncio
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import AudioVideoPiped, HighQualityAudio, HighQualityVideo
from ARUMUZIC.clients import bot, call
from urllib.parse import quote

# Token Fixed
NUB_TOKEN = "pePKYb9ltY"

def get_v_buttons():
    return InlineKeyboardMarkup([[InlineKeyboardButton("▢ sᴛᴏᴘ", callback_data="stop_cb")]])

@bot.on_message(filters.command(["vplay", "video"]) & filters.group)
async def vplay_cmd(client, message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name if message.from_user else "User"
    
    if len(message.command) < 2:
        return await message.reply("❌ **ɢɪᴠᴇ ᴀ ǫᴜᴇʀʏ!**")
    
    query = message.text.split(None, 1)[1].strip()
    m = await message.reply("<blockquote>🎬 <b>ᴘʀᴏᴄᴇssɪɴɢ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ...</b></blockquote>")

    # API URL: Using /video-stream instead of /info for better video support
    api_url = f"http://api.nubcoder.com/video-stream?token={NUB_TOKEN}&q={quote(query)}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=25) as resp:
                data = await resp.json()
                
        # API Response Check
        # /video-stream might return 'video_link' or 'stream_url'
        video_url = data.get("video_link") or data.get("stream_url")
        if not video_url:
            return await m.edit("❌ **ᴠɪᴅᴇᴏ sᴏᴜʀᴄᴇ ɴᴏᴛ ғᴏᴜɴᴅ ᴏɴ ᴀᴘɪ!**")

        title = data.get("title", "Video Stream")
        thumb = data.get("thumbnail") or "https://files.catbox.moe/cu442f.jpg"

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
            await bot.send_photo(
                chat_id,
                photo=thumb,
                caption=f"<b>🎬 sᴛᴀʀᴛᴇᴅ :</b> <a href='{video_url}'>{title}</a>\n<b>👤 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {user_name}",
                reply_markup=get_v_buttons()
            )

        except Exception as e:
            if "Already in a group call" in str(e):
                await call.change_stream(chat_id, AudioVideoPiped(video_url, HighQualityAudio(), HighQualityVideo()))
                await m.edit(f"✅ **sᴡɪᴛᴄʜᴇᴅ ᴛᴏ :** `{title}`")
            else:
                await m.edit(f"❌ **sᴛʀᴇᴀᴍ ᴇʀʀᴏʀ:** `{e}`")

    except Exception as e:
        await m.edit(f"❌ **ᴀᴘɪ ᴇʀʀᴏʀ:** `{e}`")
