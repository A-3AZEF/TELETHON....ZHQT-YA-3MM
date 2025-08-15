from telethon import TelegramClient, events
from sessions import load_sessions
import private_commands
import account_commands
import group_commands
import translate_decorate_commands
import asyncio
import os

# إعدادات السورس
API_ID = 26845245  # استبدل بقيمك
API_HASH = '0d17e3caac8b751aa91089cebf3e2439'
BOT_TOKEN = 'your_bot_token_here'  # إذا كنت تستخدم بوت

async def main():
    # إنشاء عميل لكل جلسة
    clients = []
    
    # تحميل الجلسات المتاحة
    sessions = [f.split('.')[0] for f in os.listdir('sessions') if f.endswith('.session')]
    
    if not sessions:
        print("\n" + "="*40)
        phone = input("│ لم يتم العثور على جلسات، الرجاء إدخال رقم الهاتف (مثال: +20123456789): ")
        print("="*40 + "\n")
        sessions = [phone]

    for session in sessions:
        try:
            client = TelegramClient(f'sessions/{session}', API_ID, API_HASH)
            
            # إذا كانت الجلسة غير موجودة، نطلب كود التحقق
            if not os.path.exists(f'sessions/{session}.session'):
                await client.start(phone=session)
            else:
                await client.start()
            
            clients.append(client)
            print(f"✅ تم تسجيل الدخول كـ: {(await client.get_me()).first_name}")
            
            # تسجيل الأحداث لكل عميل
            register_events(client)
            
        except Exception as e:
            print(f"❌ خطأ في جلسة {session}: {str(e)}")
            if "session" in str(e):
                os.remove(f'sessions/{session}.session')
                print("تم حذف جلسة التالف، حاول التشغيل مرة أخرى")

    if not clients:
        print("❗ لا توجد جلسات صالحة للتشغيل")
        return
    
    print("تم تشغيل السورس بنجاح!")
    await asyncio.Event().wait()

def register_events(client):
    @client.on(events.NewMessage(pattern=r'^\.الاوامر$'))
    async def show_main_menu(event):
        menu = """
╔═══════《⛧ أوامـر سـورس 𝑨𝒂𝒛𝒆𝒇 ⛧》═══════╗

⌯ م1➪  اوامــر الــخــاص
⌯ م2➪  اوامــر الحساب
⌯ م3➪  اوامــر الجروبات والنشر التلقائي
⌯ م4➪  اوامــر الـترجمه والزخرفه

╚═════《 𝑺𝑶𝑼𝑹𝑪𝑬 𝑨𝒂𝒛𝒆𝒇 ⛧ 》═════╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)

    # استدعاء أوامر الملفات الأخرى
    private_commands.register(client)
    account_commands.register(client)
    group_commands.register(client)
    translate_decorate_commands.register(client)

if __name__ == '__main__':

    asyncio.run(main())

