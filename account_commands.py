from telethon import events
import asyncio

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.م2$'))
    async def show_account_commands(event):
        menu = """
╔═✦═━《⛧ 𝗔𝗮𝘇𝗲𝗳 ⛧》━═✦═╗

⌯ م2➪  اوامــر الحساب
✧ .تفعيل الساعه ⌯ تفعيل الوقت في First Name بتوقيت مصر ويتم تغييره كل دقيقة بأرقام مزخرفة
✧ .الغاء الساعه ⌯ إلغاء تفعيل الساعة واستبدالها بنقطة في First Name
✧ .حذف الصور ⌯ حذف جميع صور البروفايل
✧ .تغيير الاسم <الاسم الجديد> ⌯ لتغيير الاسم
✧ .تغيير اليوزر <اليوزر الجديد> ⌯ لتغيير الـ username
✧ .تغيير البايو <البايو الجديد> ⌯ لتغيير البايو
✧ .اضافه الصوره <اسم الصوره> ⌯ البحث في Pinterest واضافتها للبروفايل
✧ .اخفاء رقمي ⌯ إخفاء الرقم من البروفايل
✧ .اظهار رقمي ⌯ اظهار الرقم
✧ .الغاء التحقق الثنائي <باسورد التحقق الحالي> ⌯ لإلغاء التحقق الثنائي بدون بريد
✧ .اضافه تحقق ثنائي <باسورد جديد> ⌯ لإضافة التحقق الثنائي بدون بريد أو تلميح

╚═✦═━《 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗮𝘇𝗲𝗳 ⛧ 》━═✦═╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)

   from telethon import events, functions, types
from telethon.tl import functions as tl_functions
import asyncio
import pytz
from datetime import datetime
import requests
import os
from bs4 import BeautifulSoup

# متغيرات الساعة
clock_active = {}
clock_task = {}

# زخرفة الأرقام (يمكن إضافة المزيد من الأنماط)
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
                first_name=f"⏰ {decorated_time}"
            ))
        except Exception as e:
            print(f"Error updating clock: {e}")
        
        await asyncio.sleep(60)  # انتظر دقيقة

def register(client):
    # ... الأوامر الأخرى الموجودة سابقاً ...

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

    @client.on(events.NewMessage(pattern=r'^\.اضافه الصوره (.*)'))
    async def add_profile_photo(event):
        """إضافة صورة بروفايل من بنترست"""
        query = event.pattern_match.group(1).strip()
        if not query:
            await event.reply("⚠️ يرجى كتابة اسم الصورة للبحث عنها")
            return
        
        try:
            await event.reply("🔍 جاري البحث عن الصورة في بنترست...")
            
            # البحث في بنترست (هذا مثال بسيط، قد تحتاج لاستخدام API رسمي)
            url = f"https://www.pinterest.com/search/pins/?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            img_url = soup.find('img')['src']  # هذا مثال مبسط
            
            # تحميل الصورة
            img_data = requests.get(img_url).content
            img_path = f"{query}.jpg"
            with open(img_path, 'wb') as handler:
                handler.write(img_data)
            
            # رفع الصورة
            await client(tl_functions.photos.UploadProfilePhotoRequest(
                file=await client.upload_file(img_path)
            ))
            os.remove(img_path)
            
            await event.reply(f"✅ تم إضافة الصورة بنجاح من بحث: {query}")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء إضافة الصورة: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.اخفاء رقمي$'))
    async def hide_phone_number(event):
        """إخفاء رقم الهاتف من البروفايل"""
        try:
            await client(tl_functions.account.UpdateProfileRequest(
                phone_number=''
            ))
            await event.reply("✅ تم إخفاء رقم الهاتف من البروفايل")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء إخفاء الرقم: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.اظهار رقمي$'))
    async def show_phone_number(event):
        """إظهار رقم الهاتف في البروفايل"""
        me = await client.get_me()
        if me.phone:
            try:
                await client(tl_functions.account.UpdateProfileRequest(
                    phone_number=me.phone
                ))
                await event.reply(f"✅ تم إظهار رقم الهاتف: {me.phone}")
            except Exception as e:
                await event.reply(f"❌ حدث خطأ أثناء إظهار الرقم: {str(e)}")
        else:
            await event.reply("ℹ️ لا يوجد رقم هاتف مرتبط بهذا الحساب")

    @client.on(events.NewMessage(pattern=r'^\.الغاء التحقق الثنائي (.*)'))
    async def disable_2fa(event):
        """إلغاء التحقق الثنائي"""
        password = event.pattern_match.group(1).strip()
        if not password:
            await event.reply("⚠️ يرجى إدخال كلمة السر الحالية للتحقق الثنائي")
            return
        
        try:
            await client(tl_functions.account.UpdatePasswordSettingsRequest(
                password=password,
                new_settings=types.account.PasswordInputSettings(
                    new_algo=None,
                    new_password_hash=None,
                    hint=None,
                    email=None,
                    new_secure_settings=None
                )
            ))
            await event.reply("✅ تم إلغاء التحقق الثنائي بنجاح")
        except Exception as e:
            await event.reply(f"❌ خطأ في إلغاء التحقق الثنائي: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.اضافه تحقق ثنائي (.*)'))
    async def enable_2fa(event):
        """إضافة تحقق ثنائي"""
        new_password = event.pattern_match.group(1).strip()
        if not new_password:
            await event.reply("⚠️ يرجى إدخال كلمة السر الجديدة للتحقق الثنائي")
            return
        
        try:
            await client(tl_functions.account.UpdatePasswordSettingsRequest(
                password='',  # إذا لم يكن هناك تحقق ثنائي سابق
                new_settings=types.account.PasswordInputSettings(
                    new_algo=types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow(
                        salt1=os.urandom(32),
                        salt2=os.urandom(32),
                        g=3,
                        p=bytes.fromhex('''\
                        C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F\
                        48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C\
                        3720FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C6\
                        95F851F'''[::2])
                    ),
                    new_password_hash=await client._compute_password_hash(
                        new_password,
                        types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow(
                            salt1=os.urandom(32),
                            salt2=os.urandom(32),
                            g=3,
                            p=bytes.fromhex('''\
                            C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F\
                            48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C\
                            3720FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C6\
                            95F851F'''[::2])
                        )
                    ),
                    hint="",  # لا يوجد تلميح
                    email=None,  # لا يوجد بريد إلكتروني
                    new_secure_settings=None
                )
            ))
            await event.reply("✅ تم تفعيل التحقق الثنائي بنجاح")
        except Exception as e:
            await event.reply(f"❌ خطأ في تفعيل التحقق الثنائي: {str(e)}")
    # باقي الأوامر بنفس الطريقة...
