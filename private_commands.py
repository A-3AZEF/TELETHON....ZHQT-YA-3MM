from telethon import events
from telethon import events, functions
from telethon.tl.types import InputPeerUser, PeerUser
import asyncio
from telethon import events, functions, types
from telethon.tl import functions as tl_functions
import os

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.م1$'))
    async def show_private_commands(event):
        menu = """
╔═✦═━《⛧ 𝗔𝗮𝘇𝗲𝗳 ⛧》━═✦═╗

⌯ م1➪  اوامــر الــخــاص
✧ .كـتـم ⌯ كتم الشات الخاص
✧ .الغـاء كـتـم ⌯ الغاء الكتم عن الشات
✧ .المـكـتومين ⌯ اظهار قائمة المكتومين منك
✧ .انـتـحال ⌯ لانتحال الشات الي كتبت فيه الامر
✧ .الغـاء انـتـحال ⌯ لاعادة بروفايلك كما كان
✧ .تفـلـيش شات ⌯ حذف الشات عند الطرفين
✧ .حـذف [عدد الرسائل] ⌯ لحذف الرسائل  
✧ .id ⌯ اظهار ايدي الشخص الي بتكلمه

╚═✦═━《 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗮𝘇𝗲𝗳 ⛧ 》━═✦═╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)


# قاموس لحفظ المستخدمين المكتومين
muted_users = {}

def register(client):
    # ... الأوامر الأخرى الموجودة سابقاً ...
    
    @client.on(events.NewMessage(pattern=r'^\.كتم$'))
    async def mute_user(event):
        """كتم المستخدم في الدردشة الخاصة"""
        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return
            
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            user = await event.client.get_entity(user_id)
            
            # التحقق من أن المستخدم ليس هو البوت نفسه
            if user_id == event.sender_id:
                await event.reply("❌ لا يمكنك كتم نفسك!")
                return
                
            # التحقق من أن المستخدم ليس مطور السورس
            if user_id == 12345678:  # استبدل بـ ID المطور
                await event.reply("❌ لا يمكنك كتم المطور!")
                return
            
            # إضافة المستخدم للقائمة المكتومين
            chat_id = event.chat_id
            if chat_id not in muted_users:
                muted_users[chat_id] = []
                
            if user_id not in muted_users[chat_id]:
                muted_users[chat_id].append(user_id)
                await event.reply(f"✅ تم كتم المستخدم [{user.first_name}](tg://user?id={user_id}) بنجاح!")
            else:
                await event.reply("ℹ️ هذا المستخدم مكتوم بالفعل!")
        else:
            await event.reply("⚠️ يرجى الرد على رسالة المستخدم الذي تريد كتمه!")
    
    @client.on(events.NewMessage(incoming=True))
    async def check_muted_users(event):
        """منع الرسائل من المستخدمين المكتومين"""
        if event.is_private:
            chat_id = event.chat_id
            user_id = event.sender_id
            
            if chat_id in muted_users and user_id in muted_users[chat_id]:
                await event.delete()
                try:
                    await event.client.send_message(
                        entity=user_id,
                        message="🚫 تم كتمك من قبل المستخدم ولا يمكنك إرسال الرسائل!",
                        reply_to=event.id
                    )
                except:
                    pass
    
    @client.on(events.NewMessage(pattern=r'^\.الغاء كتم$'))
    async def unmute_user(event):
        """إلغاء كتم المستخدم"""
        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return
            
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            user = await event.client.get_entity(user_id)
            
            chat_id = event.chat_id
            if chat_id in muted_users and user_id in muted_users[chat_id]:
                muted_users[chat_id].remove(user_id)
                await event.reply(f"✅ تم إلغاء كتم المستخدم [{user.first_name}](tg://user?id={user_id}) بنجاح!")
            else:
                await event.reply("ℹ️ هذا المستخدم غير مكتوم!")
        else:
            await event.reply("⚠️ يرجى الرد على رسالة المستخدم الذي تريد إلغاء كتمه!")
    
    @client.on(events.NewMessage(pattern=r'^\.المكتومين$'))
    async def show_muted_users(event):
        """عرض قائمة المكتومين"""
        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return
            
        chat_id = event.chat_id
        if chat_id in muted_users and muted_users[chat_id]:
            message = "📋 قائمة المستخدمين المكتومين:\n\n"
            for user_id in muted_users[chat_id]:
                try:
                    user = await event.client.get_entity(user_id)
                    message += f"- [{user.first_name}](tg://user?id={user_id}) (ID: `{user_id}`)\n"
                except:
                    message += f"- مستخدم غير معروف (ID: `{user_id}`)\n"
            await event.reply(message)
        else:
            await event.reply("ℹ️ لا يوجد مستخدمين مكتومين حالياً!")
            
# قاموس لحفظ البيانات الأصلية لكل حساب
original_profiles = {}

def register(client):
    # ... الأوامر السابقة مثل كتم ...
    
    @client.on(events.NewMessage(pattern=r'^\.انتحال$'))
    async def steal_identity(event):
        """انتحال هوية المستخدم في الدردشة الخاصة"""
        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return
            
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            user = await event.client.get_entity(user_id)
            
            # حفظ البيانات الأصلية إذا كانت المرة الأولى
            if event.sender_id not in original_profiles:
                me = await event.client.get_me()
                original_profiles[event.sender_id] = {
                    'first_name': me.first_name,
                    'last_name': me.last_name,
                    'bio': (await event.client(tl_functions.account.GetProfileRequest())).about,
                    'photo': None
                }
                # حفظ الصورة الأصلية إذا كانت موجودة
                if me.photo:
                    original_profiles[event.sender_id]['photo'] = await event.client.download_profile_photo('me')
            
            # تغيير الاسم
            await event.client(tl_functions.account.UpdateProfileRequest(
                first_name=user.first_name,
                last_name=user.last_name or ""
            ))
            
            # تغيير البايو
            try:
                user_full = await event.client(tl_functions.users.GetFullUserRequest(user))
                await event.client(tl_functions.account.UpdateProfileRequest(about=user_full.full_user.about or ""))
            except:
                pass
            
            # تغيير الصورة
            if user.photo:
                photo_path = await event.client.download_profile_photo(user)
                await event.client(tl_functions.photos.UploadProfilePhotoRequest(
                    file=await event.client.upload_file(photo_path)
                ))
                os.remove(photo_path)
            
            await event.reply(f"✅ تم انتحال هوية [{user.first_name}](tg://user?id={user_id}) بنجاح!")
        else:
            await event.reply("⚠️ يرجى الرد على رسالة المستخدم الذي تريد انتحاله!")
    
    @client.on(events.NewMessage(pattern=r'^\.الغاء انتحال$'))
    async def revert_identity(event):
        """إعادة البروفايل إلى الحالة الأصلية"""
        if event.sender_id in original_profiles:
            original = original_profiles[event.sender_id]
            
            # استعادة الاسم
            await event.client(tl_functions.account.UpdateProfileRequest(
                first_name=original['first_name'],
                last_name=original['last_name'] or ""
            ))
            
            # استعادة البايو
            await event.client(tl_functions.account.UpdateProfileRequest(about=original['bio'] or ""))
            
            # استعادة الصورة
            await event.client(tl_functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos('me')
            ))
            if original['photo']:
                await event.client(tl_functions.photos.UploadProfilePhotoRequest(
                    file=await event.client.upload_file(original['photo'])
                ))
                os.remove(original['photo'])
            
            del original_profiles[event.sender_id]
            await event.reply("✅ تم إعادة البروفايل إلى وضعه الأصلي بنجاح!")
        else:
            await event.reply("ℹ️ لم تقم بعملية انتحال من قبل!")
    
    @client.on(events.NewMessage(pattern=r'^\.تفليش شات$'))
    async def delete_chat(event):
        """حذف الدردشة نهائياً"""
        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return
            
        try:
            await event.client(functions.messages.DeleteHistoryRequest(
                peer=event.chat_id,
                max_id=0,
                just_clear=True
            ))
            await event.reply("✅ تم حذف الدردشة بنجاح!")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء محاولة حذف الدردشة: {str(e)}")
    
    @client.on(events.NewMessage(pattern=r'^\.حذف (\d+)$'))
    async def delete_messages(event):
        """حذف عدد معين من الرسائل"""
        if not event.is_private:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")
            return
            
        count = int(event.pattern_match.group(1))
        if count <= 0 or count > 100:
            await event.reply("⚠️ يرجى تحديد عدد بين 1 و 100")
            return
            
        messages = []
        async for msg in event.client.iter_messages(event.chat_id, limit=count + 1):
            messages.append(msg.id)
        
        if len(messages) > 1:  # نتجاهل الرسالة الحالية (الأمر نفسه)
            await event.client.delete_messages(event.chat_id, messages[1:])
            await event.reply(f"✅ تم حذف {len(messages)-1} رسالة!")
        else:
            await event.reply("ℹ️ لا توجد رسائل لحذفها!")
    
    @client.on(events.NewMessage(pattern=r'^\.id$'))
    async def show_id(event):
        """عرض آيدي الدردشة أو المستخدم"""
        if event.is_private:
            if event.reply_to_msg_id:
                reply_message = await event.get_reply_message()
                user = await event.client.get_entity(reply_message.sender_id)
                await event.reply(f"👤 آيدي المستخدم: `{user.id}`")
            else:
                chat = await event.get_chat()
                await event.reply(f"👤 آيدي الدردشة: `{chat.id}`")
        else:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الدردشات الخاصة!")


    # باقي الأوامر بنفس الطريقة...
