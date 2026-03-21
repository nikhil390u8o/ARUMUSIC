import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from ARUMUZIC.clients import bot # Make sure client name is 'bot'

# Stop tracking
TAG_STOP = {}

@bot.on_message(filters.command(["tagall", "utag", "all"], prefixes=["/", "!", ""]) & filters.group)
async def tag_all_members(client, message: Message):
    chat_id = message.chat.id
    
    # 1. Sabse pehle reply check (Testing if bot is alive)
    try:
        m = await message.reply("⚡ **ᴘʀᴏᴄᴇssɪɴɢ ᴛᴀɢɢᴀʟʟ...**")
    except Exception as e:
        print(f"Error in tagall: {e}")
        return

    # 2. Admin Check
    try:
        user = await client.get_chat_member(chat_id, message.from_user.id)
        if user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await m.edit("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!**")
    except:
        pass # Agar admin list fetch na ho toh continue

    tag_text = message.text.split(None, 1)[1] if len(message.command) > 1 else "ʜᴇʏ, ᴡᴀᴋᴇ ᴜᴘ!"
    TAG_STOP[chat_id] = False
    
    count = 0
    usertxt = ""
    
    try:
        async for member in client.get_chat_members(chat_id):
            if TAG_STOP.get(chat_id):
                break
            if member.user.is_bot or member.user.is_deleted:
                continue
            
            usertxt += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
            count += 1
            
            if count % 5 == 0:
                await client.send_message(chat_id, f"📢 **{tag_text}**\n\n{usertxt}")
                await asyncio.sleep(2) # Flood wait safety
                usertxt = ""
        
        await m.delete()
        await message.reply(f"✅ **ᴛᴀɢɢɪɴɢ ᴅᴏɴᴇ!**\nᴛᴏᴛᴀʟ: `{count}`")
    except Exception as e:
        await message.reply(f"❌ **ᴇʀʀᴏʀ:** `{e}`")

@bot.on_message(filters.command(["cancel", "stopall"], prefixes=["/", "!", ""]) & filters.group)
async def stop_tagging(client, message: Message):
    TAG_STOP[message.chat.id] = True
    await message.reply("⏳ **sᴛᴏᴘᴘɪɴɢ...**")
