from telethon import events
import requests
from bs4 import BeautifulSoup
import arabic_reshaper
from bidi.algorithm import get_display
import pyfiglet

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

  # قوالب الزخرفة المختلفة
DECORATION_TEMPLATES = [
    "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
    "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
    "αႦƈԃҽϝɠԋιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥ",
    "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ",
    "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",
    "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
    "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
    "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
    "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",
    "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
    "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹",
    "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭",
    "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # إنجليزية عادية
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘϙʀꜱᴛᴜᴠᴡxyᴢ",
    "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",
    "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉",
    "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
]

def decorate_text(text):
    """زخرفة النص باستخدام قوالب مختلفة"""
    # اختيار قالب عشوائي
    template = random.choice(DECORATION_TEMPLATES)
    decorated = ""
    
    for char in text:
        lower_char = char.lower()
        if 'a' <= lower_char <= 'z':
            # حروف إنجليزية
            index = ord(lower_char) - ord('a')
            decorated_char = template[index]
            # الحفاظ على حالة الحرف (كبير/صغير)
            decorated += decorated_char if char.isupper() else decorated_char.lower()
        elif char == ' ':
            decorated += ' '
        else:
            # الحفاظ على الحروف الأخرى كما هي (أرقام، رموز، حروف عربية)
            decorated += char
    
    return decorated

def translate_text(text, target_lang="ar"):
    """ترجمة النص باستخدام واجهة Google Translate"""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={requests.utils.quote(text)}"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data[0][0][0]
        return "❌ فشل في الحصول على الترجمة"
    except Exception as e:
        return f"❌ حدث خطأ في الترجمة: {str(e)}"

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.ترجمه$'))
    async def translate_message(event):
        """ترجمة النص المدعوم بالرد"""
        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على الرسالة المراد ترجمتها")
            return

        try:
            reply_msg = await event.get_reply_message()
            text = reply_msg.text
            if not text:
                await event.reply("⚠️ لا يوجد نص للترجمة في الرسالة المرد عليها")
                return

            # ترجمة النص إلى العربية
            translated = translate_text(text, "ar")
            await event.reply(f"🌍 الترجمة:\n\n{translated}")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء الترجمة: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.زخرفه (.*)'))
    async def decorate_message(event):
        """زخرفة النص المطلوب"""
        text = event.pattern_match.group(1).strip()
        if not text:
            await event.reply("⚠️ يرجى كتابة النص المراد زخرفته بعد الأمر")
            return

        try:
            decorated = decorate_text(text)
            await event.reply(f"✨ النص المزخرف:\n\n{decorated}")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ أثناء الزخرفة: {str(e)}")


    # باقي الأوامر بنفس الطريقة...
