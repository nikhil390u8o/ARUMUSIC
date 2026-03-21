import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from ARUMUZIC.clients import bot # Make sure 'bot' hi hai aapka client name

# Stop tracking dictionary
TAG_STOP = {}

@bot.on_message(filters.command(["tagall", "utag"], prefixes=["/", "!", ""]) & filters.group)
async def tag_all_members(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None

    # --- ADMIN CHECK ---
    try:
        user = await client.get_chat_member(chat_id, user_id)
        if user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!**")
    except Exception:
        return # Agar admin fetch nahi hua toh chup raho

    # --- TAG TEXT ---
    tag_text = "ʜᴇʏ, ᴡᴀᴋᴇ ᴜᴘ!"
    if len(message.command) > 1:
        tag_text = message.text.split(None, 1)[1]

    TAG_STOP[chat_id] = False
    m = await message.reply(f"✨ **ᴛᴀɢɢɪɴɢ sᴛᴀʀᴛᴇᴅ...**\n`Query: {tag_text}`")
    
    count = 0
    usertxt = ""

    try:
        # Pytgcalls/Pyrogram v2 mein members fetch karne ke liye bot ka ADMIN hona must hai
        async for member in client.get_chat_members(chat_id):
            if TAG_STOP.get(chat_id):
                break
            
            if member.user.is_bot or member.user.is_deleted:
                continue

            # Mention Link
            usertxt += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
            count += 1

            # Har 5 members par message send karo
            if count % 5 == 0:
                await client.send_message(chat_id, f"📢 **{tag_text}**\n\n{usertxt}")
                await asyncio.sleep(2.5) # Flood wait safety
                usertxt = ""

        # Last remaining members
        if usertxt and not TAG_STOP.get(chat_id):
            await client.send_message(chat_id, f"📢 **{tag_text}**\n\n{usertxt}")

    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")

    await m.edit(f"✅ **ᴛᴀɢɢɪɴɢ ᴅᴏɴᴇ!**\nᴛᴏᴛᴀʟ: `{count}`")
    TAG_STOP[chat_id] = False

@bot.on_message(filters.command(["cancel", "stopall"], prefixes=["/", "!", ""]) & filters.group)
async def stop_tagging(client, message: Message):
    TAG_STOP[message.chat.id] = True
    await message.reply("⏳ **sᴛᴏᴘᴘɪɴɢ ᴛᴀɢɢᴀʟʟ...**")
