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
    
    if len(message.command) < 2:
        return await message.reply("❌ **ɢɪᴠᴇ ᴀ ǫᴜᴇʀʏ!**")
    
    query = message.text.split(None, 1)[1].strip()
    m = await message.reply("<blockquote>🎬 <b>ᴘʀᴏᴄᴇssɪɴɢ ᴠɪᴅᴇᴏ...</b></blockquote>")

    # API URL
    api_url = f"http://api.nubcoder.com/info?token={NUB_TOKEN}&q={quote(query)}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=20) as resp:
                data = await resp.json()
                
        # API Check
        video_url = data.get("stream_url")
        if not video_url:
            return await m.edit("❌ **sᴛʀᴇᴀᴍ ʟɪɴᴋ ɴᴏᴛ ғᴏᴜɴᴅ!**")

        title = data.get("title", "Video")
        thumb = data.get("thumbnail")

        try:
            # IMPORTANT: Hum AudioVideoPiped hi use karenge
            # Par agar link 'audio/mp4' (itag 140) ka hai toh video black screen ho sakti hai
            # Isliye HighQualityVideo ke saath fallback logic rakha hai
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(
                    video_url,
                    HighQualityAudio(),
                    HighQualityVideo() # It requires a source with video tracks
                )
            )
            
            await m.delete()
            await bot.send_photo(
                chat_id,
                photo=thumb,
                caption=f"<b>🎬 sᴛᴀʀᴛᴇᴅ :</b> <a href='{video_url}'>{title}</a>\n\n⚠️ *Note: If only audio plays, the API provided an audio-only link.*",
                reply_markup=get_v_buttons()
            )

        except Exception as e:
            if "Already in a group call" in str(e):
                await call.change_stream(chat_id, AudioVideoPiped(video_url, HighQualityAudio(), HighQualityVideo()))
                await m.edit(f"✅ **sᴡɪᴛᴄʜᴇᴅ :** `{title}`")
            else:
                await m.edit(f"❌ **sᴛʀᴇᴀᴍ ᴇʀʀᴏʀ:** `{e}`\n*(API might be sending audio-only link)*")

    except Exception as e:
        await m.edit(f"❌ **ᴀᴘɪ ᴇʀʀᴏʀ:** `{e}`")
