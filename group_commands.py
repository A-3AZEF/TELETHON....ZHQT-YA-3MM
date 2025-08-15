from telethon import events, functions, types
from telethon.tl import functions as tl_functions
import asyncio
from collections import defaultdict

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.م3$'))
    async def show_group_commands(event):
        menu = """
╔═✦═━《⛧ 𝗔𝗮𝘇𝗲𝗳 ⛧》━═✦═╗

⌯ م3➪  اوامــر الجروبات
✧ .نشر تلقائي <النص المراد نشره> ⌯ نشر في جميع الجروبات في الحساب
✧ .طرد ⌯ طرد العضو المشار إليه (الأونر أو الأدمن فقط)
✧ .كتم ⌯ كتم العضو المشار إليه (الأونر أو الأدمن فقط)
✧ .الغاء كتم ⌯ إلغاء كتم العضو المشار إليه (الأونر أو الأدمن فقط)
✧ .تفليش ⌯ طرد جميع أعضاء الجروب والأدمنية [للأونر فقط]
✧ .تفليش الجروب ⌯ طرد جميع أعضاء الجروب [للأونر والأدمن]
✧ .تحذير ⌯ بالرد على العضو؛ كل عضو له 3 تحذيرات، عند 3 تحذيرات يتم الطرد تلقائيًا
✧ .مسح التحذيرات ⌯ بالرد على العضو لمسح أي تحذير عليه
✧ .رفع ادمن ⌯ إعطاء صلاحية الأدمن للعضو المشار إليه (للأونر والأدمن في الجروب)
✧ .تنزيل ⌯ إزالة أي أدمن مهما كانت صلاحياته (للأونر فقط)

╚═✦═━《 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗮𝘇𝗲𝗳 ⛧ 》━═✦═╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)

# تخزين التحذيرات لكل مجموعة
warnings = defaultdict(lambda: defaultdict(int))

def register(client):
    # ... الأوامر الأخرى الموجودة سابقاً ...

    @client.on(events.NewMessage(pattern=r'^\.نشر تلقائي (.*)'))
    async def auto_spread(event):
        """نشر نص في جميع الجروبات"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        text = event.pattern_match.group(1).strip()
        if not text:
            await event.reply("⚠️ يرجى كتابة النص المراد نشره بعد الأمر")
            return

        await event.reply("⏳ جاري النشر في جميع الجروبات...")
        count = 0
        async for dialog in client.iter_dialogs():
            if dialog.is_group:
                try:
                    await client.send_message(dialog.id, text)
                    count += 1
                    await asyncio.sleep(2)  # تجنب حظر التليجرام
                except Exception as e:
                    print(f"Error sending to {dialog.id}: {str(e)}")
        
        await event.reply(f"✅ تم النشر في {count} مجموعة بنجاح")

    @client.on(events.NewMessage(pattern=r'^\.طرد$'))
    async def kick_member(event):
        """طرد عضو من الجروب"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة العضو المراد طرده")
            return

        try:
            # التحقق من صلاحيات المستخدم
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not (participant.is_admin or participant.is_creator):
                await event.reply("❌ تحتاج إلى صلاحية أدمن على الأقل لاستخدام هذا الأمر")
                return

            reply_msg = await event.get_reply_message()
            user_id = reply_msg.sender_id
            user = await client.get_entity(user_id)

            # لا يمكن طرد المالك أو الأدمن
            target_perms = await client.get_permissions(event.chat_id, user_id)
            if target_perms.is_creator:
                await event.reply("❌ لا يمكنك طرد مالك الجروب!")
                return
            if target_perms.is_admin and not participant.is_creator:
                await event.reply("❌ لا يمكنك طرد أدمن آخر إلا إذا كنت المالك!")
                return

            await client.kick_participant(event.chat_id, user_id)
            await event.reply(f"✅ تم طرد العضو [{user.first_name}](tg://user?id={user_id}) بنجاح")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء الطرد: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.كتم$'))
    async def mute_member(event):
        """كتم عضو في الجروب"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة العضو المراد كتمه")
            return

        try:
            # التحقق من صلاحيات المستخدم
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not (participant.is_admin or participant.is_creator):
                await event.reply("❌ تحتاج إلى صلاحية أدمن على الأقل لاستخدام هذا الأمر")
                return

            reply_msg = await event.get_reply_message()
            user_id = reply_msg.sender_id
            user = await client.get_entity(user_id)

            # لا يمكن كتم المالك
            target_perms = await client.get_permissions(event.chat_id, user_id)
            if target_perms.is_creator:
                await event.reply("❌ لا يمكنك كتم مالك الجروب!")
                return

            await client.edit_permissions(
                event.chat_id,
                user_id,
                send_messages=False
            )
            await event.reply(f"✅ تم كتم العضو [{user.first_name}](tg://user?id={user_id}) بنجاح")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء الكتم: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.الغاء كتم$'))
    async def unmute_member(event):
        """إلغاء كتم عضو في الجروب"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة العضو المراد إلغاء كتمه")
            return

        try:
            # التحقق من صلاحيات المستخدم
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not (participant.is_admin or participant.is_creator):
                await event.reply("❌ تحتاج إلى صلاحية أدمن على الأقل لاستخدام هذا الأمر")
                return

            reply_msg = await event.get_reply_message()
            user_id = reply_msg.sender_id
            user = await client.get_entity(user_id)

            await client.edit_permissions(
                event.chat_id,
                user_id,
                send_messages=True
            )
            await event.reply(f"✅ تم إلغاء كتم العضو [{user.first_name}](tg://user?id={user_id}) بنجاح")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء إلغاء الكتم: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.تفليش$'))
    async def full_kick(event):
        """طرد جميع الأعضاء والأدمنية (للمالك فقط)"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        try:
            # التحقق من أن المستخدم هو المالك
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not participant.is_creator:
                await event.reply("❌ هذا الأمر للمالك فقط!")
                return

            await event.reply("⏳ جاري طرد جميع الأعضاء والأدمنية...")
            count = 0
            async for user in client.iter_participants(event.chat_id):
                if user.id != event.sender_id:  # لا تطرد نفسك
                    try:
                        await client.kick_participant(event.chat_id, user.id)
                        count += 1
                        await asyncio.sleep(1)  # تجنب حظر التليجرام
                    except:
                        pass
            
            await event.reply(f"✅ تم طرد {count} عضو/أدمن بنجاح")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء التفليش: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.تفليش الجروب$'))
    async def members_kick(event):
        """طرد جميع الأعضاء فقط (للمالك والأدمن)"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        try:
            # التحقق من صلاحيات المستخدم
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not (participant.is_admin or participant.is_creator):
                await event.reply("❌ تحتاج إلى صلاحية أدمن على الأقل لاستخدام هذا الأمر")
                return

            await event.reply("⏳ جاري طرد جميع الأعضاء...")
            count = 0
            async for user in client.iter_participants(event.chat_id):
                # طرد الأعضاء فقط (ليس الأدمنية أو المالك)
                user_perms = await client.get_permissions(event.chat_id, user.id)
                if not (user_perms.is_admin or user_perms.is_creator) and user.id != event.sender_id:
                    try:
                        await client.kick_participant(event.chat_id, user.id)
                        count += 1
                        await asyncio.sleep(1)  # تجنب حظر التليجرام
                    except:
                        pass
            
            await event.reply(f"✅ تم طرد {count} عضو بنجاح")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء التفليش: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.تحذير$'))
    async def warn_member(event):
        """إعطاء تحذير لعضو"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة العضو المراد تحذيره")
            return

        try:
            # التحقق من صلاحيات المستخدم
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not (participant.is_admin or participant.is_creator):
                await event.reply("❌ تحتاج إلى صلاحية أدمن على الأقل لاستخدام هذا الأمر")
                return

            reply_msg = await event.get_reply_message()
            user_id = reply_msg.sender_id
            user = await client.get_entity(user_id)

            # لا يمكن تحذير المالك أو الأدمن
            target_perms = await client.get_permissions(event.chat_id, user_id)
            if target_perms.is_admin or target_perms.is_creator:
                await event.reply("❌ لا يمكنك تحذير أدمن أو مالك الجروب!")
                return

            chat_id = event.chat_id
            warnings[chat_id][user_id] += 1

            if warnings[chat_id][user_id] >= 3:
                await client.kick_participant(chat_id, user_id)
                warnings[chat_id][user_id] = 0
                await event.reply(f"🚨 تم طرد العضو [{user.first_name}](tg://user?id={user_id}) تلقائياً بسبب 3 تحذيرات!")
            else:
                await event.reply(
                    f"⚠️ تم تحذير العضو [{user.first_name}](tg://user?id={user_id})\n"
                    f"عدد التحذيرات: {warnings[chat_id][user_id]}/3\n"
                    f"عند 3 تحذيرات سيتم الطرد تلقائياً"
                )
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء التحذير: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.مسح التحذيرات$'))
    async def clear_warnings(event):
        """مسح تحذيرات عضو"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة العضو المراد مسح تحذيراته")
            return

        try:
            # التحقق من صلاحيات المستخدم
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not (participant.is_admin or participant.is_creator):
                await event.reply("❌ تحتاج إلى صلاحية أدمن على الأقل لاستخدام هذا الأمر")
                return

            reply_msg = await event.get_reply_message()
            user_id = reply_msg.sender_id
            user = await client.get_entity(user_id)

            chat_id = event.chat_id
            if chat_id in warnings and user_id in warnings[chat_id]:
                warnings[chat_id][user_id] = 0
                await event.reply(f"✅ تم مسح تحذيرات العضو [{user.first_name}](tg://user?id={user_id}) بنجاح")
            else:
                await event.reply(f"ℹ️ لا يوجد تحذيرات للعضو [{user.first_name}](tg://user?id={user_id})")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء مسح التحذيرات: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.رفع ادمن$'))
    async def promote_admin(event):
        """رفع عضو إلى أدمن"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة العضو المراد رفعه")
            return

        try:
            # التحقق من صلاحيات المستخدم
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not (participant.is_admin or participant.is_creator):
                await event.reply("❌ تحتاج إلى صلاحية أدمن على الأقل لاستخدام هذا الأمر")
                return

            reply_msg = await event.get_reply_message()
            user_id = reply_msg.sender_id
            user = await client.get_entity(user_id)

            # لا يمكن رفع المالك
            target_perms = await client.get_permissions(event.chat_id, user_id)
            if target_perms.is_creator:
                await event.reply("❌ هذا العضو هو مالك الجروب بالفعل!")
                return

            # صلاحيات الأدمن (يمكن تعديلها حسب الرغبة)
            admin_rights = types.ChatAdminRights(
                change_info=True,
                post_messages=True,
                edit_messages=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                add_admins=False,  # فقط المالك يمكنه إضافة أدمنية
                manage_call=True
            )

            await client(
                functions.channels.EditAdminRequest(
                    channel=event.chat_id,
                    user_id=user_id,
                    admin_rights=admin_rights,
                    rank="Admin"
                )
            )
            await event.reply(f"✅ تم رفع العضو [{user.first_name}](tg://user?id={user_id}) إلى أدمن بنجاح")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء رفع الأدمن: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.تنزيل$'))
    async def demote_admin(event):
        """تنزيل أدمن"""
        if not event.is_group:
            await event.reply("⚠️ هذا الأمر يعمل فقط في الجروبات!")
            return

        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على رسالة الأدمن المراد تنزيله")
            return

        try:
            # التحقق من أن المستخدم هو المالك
            participant = await client.get_permissions(event.chat_id, event.sender_id)
            if not participant.is_creator:
                await event.reply("❌ هذا الأمر للمالك فقط!")
                return

            reply_msg = await event.get_reply_message()
            user_id = reply_msg.sender_id
            user = await client.get_entity(user_id)

            # لا يمكن تنزيل المالك
            target_perms = await client.get_permissions(event.chat_id, user_id)
            if target_perms.is_creator:
                await event.reply("❌ لا يمكن تنزيل مالك الجروب!")
                return

            await client(
                functions.channels.EditAdminRequest(
                    channel=event.chat_id,
                    user_id=user_id,
                    admin_rights=types.ChatAdminRights(),
                    rank=""
                )
            )
            await event.reply(f"✅ تم تنزيل الأدمن [{user.first_name}](tg://user?id={user_id}) بنجاح")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء تنزيل الأدمن: {str(e)}")
    # باقي الأوامر بنفس الطريقة...

