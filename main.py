from telethon import TelegramClient, events
from sessions import load_sessions
import private_commands
import account_commands
import group_commands
import translate_decorate_commands
import asyncio
import os

# إعدادات السورس
API_ID = 12345  # استبدل بقيمك
API_HASH = 'your_api_hash_here'
BOT_TOKEN = 'your_bot_token_here'  # إذا كنت تستخدم بوت

# تحميل الجلسات
sessions = load_sessions()

async def main():
    # إنشاء عميل لكل جلسة
    clients = []
    for session in sessions:
        client = TelegramClient(f'sessions/{session}', API_ID, API_HASH)
        await client.start()
        clients.append(client)
        
        # تسجيل الأحداث لكل عميل
        register_events(client)
    
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