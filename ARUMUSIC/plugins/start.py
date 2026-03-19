import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


# ───────────── START COMMAND ─────────────

@bot.on_message(filters.command("start"))
async def start_cmd(_, msg: Message):
    # Pehle purana message delete karo (agar ho sake)
    try:
        await msg.delete()
    except:
        pass

    # Bot knamfo ek hi baar fetch kar lete hain performance ke liye
    me = await bot.get_me()
    bot_name = me.first_name
    bot_username = me.username
    
    # ──────── ANIMATION START ────────
    # 1st Phase: HEY
    m = await bot.send_message(msg.chat.id, "<b>ʜᴇʏ...</b>")
    await asyncio.sleep(0.8) # Thoda wait
    
    # 2nd Phase: HOW ARE YOU
    await m.edit_text("<b>ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ? ✨</b>")
    await asyncio.sleep(0.8)
    
    # 3rd Phase: I AM [BOTNAME] STARTING...
    bot_name = (await bot.get_me()).first_name
    await m.edit_text(f"<b>ɪ ᴀᴍ {bot_name} 🎵\nsᴛᴀʀᴛɪɴɢ.....</b>")
    await asyncio.sleep(1.0)
    
    # Animation khatam, ab message delete karke main menu bhejenge
    await m.delete()
    # ──────── ANIMATION END ────────

    START_IMG = "https://files.catbox.moe/uyum1c.jpg" 
    
    text = (
        "<b>╔══════════════════╗</b>\n"
        "<b>   🎵 ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ 🎵   </b>\n"
        "<b>╚══════════════════╝</b>\n\n"
        "<b>👋 ʜᴇʟʟᴏ! ɪ ᴀᴍ ᴀ ғᴀsᴛ & ᴘᴏᴡᴇʀғᴜʟ</b>\n"
        "<b>ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ.</b>\n\n"
        "✨ <b>ᴍᴀᴅᴇ ᴡɪᴛʜ ❤️ ʙʏ:</b> <a href='https://t.me/sxyaru'>sxyaru</a>"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("❓ ʜᴇʟᴘ", callback_data="help_menu"),
            InlineKeyboardButton("📂 ʀᴇᴘᴏ", callback_data="repo_menu")
        ],
        [
            InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url="https://t.me/sxyaru"),
            InlineKeyboardButton("📢 sᴜᴘᴘᴏʀᴛ", url="https://t.me/your_channel")
        ],
        [
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{(await bot.get_me()).username}?startgroup=true")
        ]
    ])

    await bot.send_photo(
        msg.chat.id,
        photo=START_IMG,
        caption=text,
        reply_markup=buttons
    )
