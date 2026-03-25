import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

TAG_STOP = {}

@Client.on_message(filters.command(["tagall", "all", "utag"]) & filters.group)
async def tag_all_members(client: Client, message: Message):
    chat_id = message.chat.id

    # bot alive check
    try:
        m = await message.reply("⚡ Processing TagAll...")
    except:
        return

    # ❗ IMPORTANT: force correct client
    app = client

    # admin check
    try:
        user = await app.get_chat_member(chat_id, message.from_user.id)
        if user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await m.edit("❌ Only admins can use this!")
    except Exception as e:
        return await m.edit(f"Admin check error: {e}")

    # safe text
    tag_text = "Hey, wake up!"
    if len(message.command) > 1:
        try:
            tag_text = message.text.split(None, 1)[1]
        except:
            pass

    TAG_STOP[chat_id] = False

    count = 0
    usertxt = ""

    # ❗ FIX: safe members fetch
    try:
        async for member in app.get_chat_members(chat_id):

            if TAG_STOP.get(chat_id):
                break

            user = member.user

            if not user:
                continue

            if user.is_bot or user.is_deleted:
                continue

            usertxt += f"[{user.first_name}](tg://user?id={user.id}) "
            count += 1

            # send in chunks
            if count % 5 == 0:
                try:
                    await message.reply(f"{tag_text}\n\n{usertxt}")
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                    await message.reply(f"{tag_text}\n\n{usertxt}")
                except Exception:
                    pass

                await asyncio.sleep(2)
                usertxt = ""

    except Exception as e:
        return await message.reply(f"❌ Member fetch error:\n`{e}`")

    # last batch
    if usertxt:
        try:
            await message.reply(f"{tag_text}\n\n{usertxt}")
        except:
            pass

    await m.delete()
    await message.reply(f"✅ Tagging Done!\nTotal Users: `{count}`")


@Client.on_message(filters.command(["stop", "cancel"]) & filters.group)
async def stop_tag(client: Client, message: Message):
    TAG_STOP[message.chat.id] = True
    await message.reply("⏹ Stopping...")
