from telethon import events

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

    @client.on(events.NewMessage(pattern=r'^\.كتم$'))
    async def mute_user(event):
        # كود كتم المستخدم
        pass

    @client.on(events.NewMessage(pattern=r'^\.الغاء كتم$'))
    async def unmute_user(event):
        # كود إلغاء كتم المستخدم
        pass

    # باقي الأوامر بنفس الطريقة...