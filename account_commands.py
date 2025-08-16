from telethon import events, functions, types
from telethon.tl import functions as tl_functions
import pytz
from datetime import datetime
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
import time
import asyncio
from collections import defaultdict

warnings = defaultdict(lambda: defaultdict(int))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.م2$'))
    async def show_account_commands(event):
        me = await event.client.get_me()
        if event.sender_id != me.id:
            return

        menu = """
╔═✦═━《⛧ 𝗔𝗮𝘇𝗲𝗳 ⛧》━═✦═╗

⌯ م2➪  اوامــر الحساب
✧ .تفعيل الساعه ⌯ تفعيل الوقت في First Name بتوقيت مصر ويتم تغييره كل دقيقة بأرقام مزخرفة
✧ .الغاء الساعه ⌯ إلغاء تفعيل الساعة واستبدالها بنقطة في First Name
✧ .حذف الصور ⌯ حذف جميع صور البروفايل
✧ .تغيير الاسم <الاسم الجديد> ⌯ لتغيير الاسم
✧ .تغيير اليوزر <اليوزر الجديد> ⌯ لتغيير الـ username
✧ .تغيير البايو <البايو الجديد> ⌯ لتغيير البايو
✧ .اضافه الصوره <اسم الصوره> ⌯ اضافه صوره عشوائيه😂
╚═✦═━《 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗮𝘇𝗲𝗳 ⛧ 》━═✦═╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)

    # متغيرات الساعة
    clock_active = {}
    clock_task = {}

    # زخرفة الأرقام
    DECORATION_STYLES = {
        '1': '𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗',
        '2': '𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡',
        '3': '０１２３４５６７８９',
        '4': '₀₁₂₃₄₅₆₇₈₉'
    }

    def decorate_number(number, style='1'):
        """تحويل الأرقام إلى أرقام مزخرفة"""
        decorated = ''
        for digit in str(number):
            if digit.isdigit():
                index = int(digit)
                decorated += DECORATION_STYLES[style][index]
            else:
                decorated += digit
        return decorated

    async def update_clock(client, user_id):
        """تحديث الساعة كل دقيقة"""
        while clock_active.get(user_id, False):
            try:
                # الحصول على الوقت الحالي بتوقيت مصر
                tz = pytz.timezone('Africa/Cairo')
                now = datetime.now(tz)
                time_str = now.strftime("%I:%M %p")  # 12-hour format with AM/PM

                # تزيين الأرقام
                decorated_time = decorate_number(time_str, style='1')

                # تحديث الاسم الأول
                await client(tl_functions.account.UpdateProfileRequest(
                    first_name=f" {decorated_time}"
                ))
            except Exception as e:
                print(f"Error updating clock: {e}")

            await asyncio.sleep(60)  # انتظر دقيقة

    @client.on(events.NewMessage(pattern=r'^\.تفعيل الساعه$'))
    async def activate_clock_cmd(event):
        """تفعيل الساعة في الاسم الأول"""
        user_id = event.sender_id

        if user_id in clock_active and clock_active[user_id]:
            await event.reply("ℹ️ الساعة مفعلة بالفعل!")
            return

        clock_active[user_id] = True
        clock_task[user_id] = asyncio.create_task(update_clock(client, user_id))
        await event.reply("✅ تم تفعيل الساعة في الاسم الأول (توقيت مصر)")

    @client.on(events.NewMessage(pattern=r'^\.الغاء الساعه$'))
    async def deactivate_clock_cmd(event):
        """إلغاء تفعيل الساعة"""
        user_id = event.sender_id

        if user_id in clock_active and clock_active[user_id]:
            clock_active[user_id] = False
            if user_id in clock_task:
                clock_task[user_id].cancel()

            # إعادة تعيين الاسم الأول إلى نقطة
            await client(tl_functions.account.UpdateProfileRequest(
                first_name="•"
            ))
            await event.reply("✅ تم إلغاء تفعيل الساعة")
        else:
            await event.reply("ℹ️ الساعة غير مفعلة بالفعل")

    @client.on(events.NewMessage(pattern=r'^\.حذف الصور$'))
    async def delete_profile_photos(event):
        """حذف جميع صور البروفايل"""
        photos = await client.get_profile_photos('me')
        if photos:
            await client(tl_functions.photos.DeletePhotosRequest(photos))
            await event.reply("✅ تم حذف جميع صور البروفايل بنجاح")
        else:
            await event.reply("ℹ️ لا توجد صور بروفايل لحذفها")

    @client.on(events.NewMessage(pattern=r'^\.تغيير الاسم (.*)'))
    async def change_name(event):
        """تغيير الاسم الأول والأخير"""
        new_name = event.pattern_match.group(1).strip()
        if not new_name:
            await event.reply("⚠️ يرجى كتابة الاسم الجديد بعد الأمر")
            return

        parts = new_name.split(maxsplit=1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        await client(tl_functions.account.UpdateProfileRequest(
            first_name=first_name,
            last_name=last_name
        ))
        await event.reply(f"✅ تم تغيير الاسم إلى: {first_name} {last_name}")

    @client.on(events.NewMessage(pattern=r'^\.تغيير اليوزر (.*)'))
    async def change_username(event):
        """تغيير اسم المستخدم"""
        new_username = event.pattern_match.group(1).strip().lower()
        if not new_username:
            await event.reply("⚠️ يرجى كتابة اليوزر الجديد بعد الأمر")
            return

        try:
            await client(tl_functions.account.UpdateUsernameRequest(
                username=new_username
            ))
            await event.reply(f"✅ تم تغيير اليوزر إلى: @{new_username}")
        except Exception as e:
            await event.reply(f"❌ خطأ في تغيير اليوزر: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.تغيير البايو (.*)'))
    async def change_bio(event):
        """تغيير البايو"""
        new_bio = event.pattern_match.group(1).strip()
        if not new_bio:
            await event.reply("⚠️ يرجى كتابة البايو الجديد بعد الأمر")
            return

        await client(tl_functions.account.UpdateProfileRequest(
            about=new_bio
        ))
        await event.reply(f"✅ تم تغيير البايو إلى: {new_bio}")

    UNSPLASH_ACCESS_KEY = "jBR40ugRIKrKLfGyVVGYBIQQvs3kyvyhORFOil88BoM"

    @client.on(events.NewMessage(pattern=r'^\.اضافه الصوره (.*)'))
    async def add_profile_photo(event):
        query = event.pattern_match.group(1).strip()
        if not query:
            await event.reply("⚠️ يرجى كتابة اسم للبحث عن صورة")
            return

        try:
            await event.reply("🔍 جاري البحث عن صورة...")

            # البحث في Unsplash API
            search_url = "https://api.unsplash.com/search/photos"
            params = {
                "query": query,
                "per_page": 20,
                "client_id": UNSPLASH_ACCESS_KEY
            }

            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code != 200:
                await event.reply("❌ فشل في الحصول على النتائج من Unsplash")
                return

            data = response.json()
            results = data.get("results", [])
            if not results:
                await event.reply("❌ لم يتم العثور على أي صور")
                return

            # اختيار صورة عشوائية
            img_url = random.choice(results)["urls"]["regular"]

            # تحميل الصورة
            img_response = requests.get(img_url, stream=True, timeout=15)
            img_response.raise_for_status()

            img_path = f"temp_profile_{int(time.time())}.jpg"
            with open(img_path, "wb") as handler:
                for chunk in img_response.iter_content(1024):
                    handler.write(chunk)

            # رفع الصورة للبروفايل
            await client(functions.photos.UploadProfilePhotoRequest(
                file=await client.upload_file(img_path)
            ))

            await event.reply(f"✅ تم تحديث صورة البروفايل بنجاح\n🔍 من بحث: {query}")

        except Exception as e:
            await event.reply(f"❌ خطأ: {str(e)}")

        finally:
            if 'img_path' in locals() and os.path.exists(img_path):
                os.remove(img_path)




    
