import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

TAG_STOP = {}

@Client.on_message(filters.command(["tagall", "utag", "all"]) & filters.group)
async def tag_all_members(client, message: Message):
    chat_id = message.chat.id

    m = await message.reply("⚡ Processing TagAll...")

    # Admin check
    try:
        user = await client.get_chat_member(chat_id, message.from_user.id)
        if user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await m.edit("❌ Only admins can use this!")
    except Exception as e:
        return await m.edit(f"❌ Admin check failed: {e}")

    tag_text = "ʜᴇʏ, ᴡᴀᴋᴇ ᴜᴘ!"
    if len(message.command) > 1:
        tag_text = message.text.split(None, 1)[1]

    TAG_STOP[chat_id] = False

    count = 0
    usertxt = ""

    async for member in client.get_chat_members(chat_id):

        if TAG_STOP.get(chat_id):
            break

        user = member.user

        if user.is_bot or user.is_deleted:
            continue

        usertxt += f"[{user.first_name}](tg://user?id={user.id}) "
        count += 1

        if count % 5 == 0:
            try:
                await client.send_message(chat_id, f"📢 {tag_text}\n\n{usertxt}")
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
                await client.send_message(chat_id, f"📢 {tag_text}\n\n{usertxt}")

            await asyncio.sleep(2)
            usertxt = ""

    if usertxt:
        await client.send_message(chat_id, f"📢 {tag_text}\n\n{usertxt}")

    await m.delete()
    await message.reply(f"✅ Tagging Done! Total: `{count}`")


@Client.on_message(filters.command(["cancel", "stopall"]) & filters.group)
async def stop_tagging(client, message: Message):
    TAG_STOP[message.chat.id] = True
    await message.reply("⏳ Stopping TagAll...")
