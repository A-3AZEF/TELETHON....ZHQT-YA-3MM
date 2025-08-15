from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.م4$'))
    async def show_translate_decorate_commands(event):
        menu = """
╔═✦═━《⛧ 𝗔𝗮𝘇𝗲𝗳 ⛧》━═✦═╗

⌯ م4➪  اوامــر الترجمه والزخرفه
✧ .ترجمه ⌯ بالرد على أي نص لترجمته
✧ .زخرفه <النص> ⌯ لزخرفة النص المكتوب

╚═✦═━《 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗮𝘇𝗲𝗳 ⛧ 》━═✦═╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)

    @client.on(events.NewMessage(pattern=r'^\.زخرفه (.*)'))
    async def decorate_text(event):
        text = event.pattern_match.group(1)
        # كود الزخرفة هنا
        decorated_text = f"زخرفة النص: {text}"
        await event.reply(decorated_text)

    # باقي الأوامر بنفس الطريقة...