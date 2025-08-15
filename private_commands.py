from telethon import events, functions, types
from telethon.tl import functions as tl_functions
from telethon.tl.functions.users import GetFullUserRequest
from collections import defaultdict
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
import os
import asyncio


# متغيرات عامة
muted_chats = set()
original_profiles = {}

def register(client):
    async def is_owner(event):
        """تحقق إذا كان المرسل هو صاحب الحساب"""
        return event.sender_id == (await event.client.get_me()).id

    @client.on(events.NewMessage(pattern=r'^\.م1$'))
    async def show_private_commands(event):
        """عرض قائمة أوامر الخاص"""
        if not await is_owner(event):
            return

        menu = """
╔═✦═━《⛧ 𝗔𝗮𝘇𝗲𝗳 ⛧》━═✦═╗
⌯ م1➪  اوامــر الــخــاص
✧ .كتمم ⌯ كتم الدردشة الحالية
✧ .الغاء كتمم ⌯ إلغاء كتم الدردشة
✧ .انتحال ⌯ انتحال هوية مستخدم (بالرد)
✧ .تفليش شات ⌯ حذف الدردشة نهائياً
✧ .المكتومين ⌯ عرض الدردشات المكتومه حاليآ
✧ .حذف [عدد] ⌯ حذف عدد من الرسائل
✧ .id ⌯ عرض آيدي الدردشة أو المستخدم 
╚═✦═━《 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗮𝘇𝗲𝗳 ⛧ 》━═✦═╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)

    @client.on(events.NewMessage(pattern=r'^\.كتمم$'))
    async def mute_chat(event):
        """كتم الدردشة الحالية"""
        if not await is_owner(event):
            return

        chat_id = event.chat_id
        if chat_id not in muted_chats:
            muted_chats.add(chat_id)
            await event.reply("✅ تم كتم هذه الدردشة بنجاح")
        else:
            await event.reply("ℹ️ هذه الدردشة مكتومة بالفعل!")

    @client.on(events.NewMessage(pattern=r'^\.الغاء كتمم$'))
    async def unmute_chat(event):
        """إلغاء كتم الدردشة الحالية"""
        if not await is_owner(event):
            return

        chat_id = event.chat_id
        if chat_id in muted_chats:
            muted_chats.remove(chat_id)
            await event.reply("✅ تم إلغاء كتم هذه الدردشة")
        else:
            await event.reply("ℹ️ هذه الدردشة غير مكتومة!")

    @client.on(events.NewMessage(incoming=True))
    async def handle_muted_chats(event):
        """حذف رسائل الدردشات المكتومة"""
        if event.is_private and event.chat_id in muted_chats:
            # تجاهل إذا كان المرسل هو البوت نفسه
            if event.sender_id == (await event.client.get_me()).id:
                return

            await event.delete()
            try:
                await event.respond("", reply_to=event.id)
            except:
                pass

    @client.on(events.NewMessage(pattern=r'^\.انتحال$'))
    async def steal_identity(event):
        """انتحال هوية مستخدم (بالرد)"""
        me = await event.client.get_me()
        if event.sender_id != me.id:
            return
            
        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return
            
        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة المستخدم!")
            return
            
        try:
            reply = await event.get_reply_message()
            user = await event.client.get_entity(reply.sender_id)
            
            # حفظ البيانات الأصلية
            if event.sender_id not in original_profiles:
                full_user = await event.client(GetFullUserRequest(me.id))
                original_profiles[event.sender_id] = {
                    'first_name': me.first_name,
                    'last_name': me.last_name or "",
                    'bio': full_user.full_user.about or "",
                    'photo': await event.client.get_profile_photos('me')
                }
            
            # تغيير البروفايل
            full_user = await event.client(GetFullUserRequest(user.id))
            await event.client(UpdateProfileRequest(
                first_name=user.first_name,
                last_name=user.last_name or "",
                about=full_user.full_user.about or ""
            ))
            
            # تغيير الصورة
            if user.photo:
                photo = await event.client.download_profile_photo(user)
                await event.client(UploadProfilePhotoRequest(
                    file=await event.client.upload_file(photo)
                ))
                os.remove(photo)
            
            await event.reply(f"✅ تم انتحال هوية {user.first_name} بنجاح")
            
        except Exception as e:
            await event.reply(f"❌ حدث خطأ: {str(e)}")

    


    @client.on(events.NewMessage(pattern=r'^\.حذف (\d+)$'))
    async def delete_messages(event):
        """حذف عدد من الرسائل"""
        if not await is_owner(event):
            return

        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return

        try:
            count = int(event.pattern_match.group(1))
            if count < 1 or count > 100:
                await event.reply("⚠️ الرجاء إدخال عدد بين 1 و 100")
                return

            messages = []
            async for msg in event.client.iter_messages(event.chat_id, limit=count+1):
                messages.append(msg.id)

            await event.client.delete_messages(event.chat_id, messages[1:])
            await event.reply(f"✅ تم حذف {len(messages)-1} رسالة")

        except Exception as e:
            await event.reply(f"❌ حدث خطأ: {str(e)}")

    # أمر عرض الآيدي

    @client.on(events.NewMessage(pattern=r'^\.id$'))
    async def show_id(event):
        """عرض الآيدي"""
        # التحقق من أن المرسل هو صاحب الحساب
        me = await event.client.get_me()
        if event.sender_id != me.id:
            return
        
        if event.is_private:
            if event.reply_to_msg_id:
                user = await event.get_reply_message()
                await event.reply(f"👤 آيدي المستخدم: `{user.sender_id}`")
            else:
                await event.reply(f"👥 آيدي الدردشة: `{event.chat_id}`")
        else:
            await event.reply("⚠️ هذا الأمر للدردشات الخاصة فقط!")

    
    @client.on(events.NewMessage(pattern=r'^\.المكتومين$'))
    async def show_muted_chats(event):
        """عرض قائمة الدردشات المكتومة"""
        # التحقق من أن المرسل هو صاحب الحساب
        me = await event.client.get_me()
        if event.sender_id != me.id:
            return

        if not muted_chats:
            await event.reply("📭 لا توجد دردشات مكتومة حالياً")
            return

        message = "📋 قائمة الدردشات المكتومة:\n\n"
        for chat_id in muted_chats:
            try:
                chat = await event.client.get_entity(chat_id)
                message += f"- {chat.title if hasattr(chat, 'title') else chat.first_name} (ID: `{chat_id}`)\n"
            except:
                message += f"- دردشة غير معروفة (ID: `{chat_id}`)\n"

        await event.reply(message)
