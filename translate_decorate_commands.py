from telethon import events
import requests
import random
import json

# قوالب زخرفة الإنجليزية الستة
EN_DECORATION_TEMPLATES = {
    "1": "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧",
    "2": "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
    "3": "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇",
    "4": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
    "5": "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",
    "6": "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
}

# زخرفة عربية بسيطة
AR_DECORATION_TEMPLATES = [
    "آ أ إ ء ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي",
    "آأإءبـتـثـجـحـخـدذرزسشصضطظعغفقلـمـنـهـوي",
    "⍟⍢⍣⍤⍥⍦⍧⍨⍩⍪⍫⍬⍭⍮⍯⍰⍱⍲⍳⍴⍵⍶⍷⍸⍹"
]

def decorate_text(text, style=None):
    """زخرفة النص بالإنجليزية أو العربية"""
    decorated = ""
    for char in text:
        lower_char = char.lower()
        if 'a' <= lower_char <= 'z':  # إنجليزية
            if style and style in EN_DECORATION_TEMPLATES:
                template = EN_DECORATION_TEMPLATES[style]
            else:
                template = random.choice(list(EN_DECORATION_TEMPLATES.values()))
            index = ord(lower_char) - ord('a')
            decorated_char = template[index]
            decorated += decorated_char if char.isupper() else decorated_char.lower()
        elif '\u0600' <= char <= '\u06FF':  # عربية
            template = random.choice(AR_DECORATION_TEMPLATES).split()
            decorated += random.choice(template)
        else:
            decorated += char  # أرقام ورموز تبقى كما هي
    return decorated

def translate_text(text, target_lang="ar"):
    """ترجمة النص باستخدام Google Translate"""
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

    @client.on(events.NewMessage(pattern=r'^\.م4$'))
    async def show_translate_decorate_commands(event):
        menu = """
╔═✦═━《⛧ 𝗔𝗮𝘇𝗲𝗳 ⛧》━═✦═╗
⌯ م4➪  اوامــر الترجمه والزخرفه
✧ .ترجمه ⌯ بالرد على أي نص لترجمته
✧ .زخرفه <النص> ⌯ زخرفة عشوائية
✧ .زخرفه <النمط> <النص> ⌯ زخرفة بالنمط المختار
✧ .انماط الزخرفه ⌯ عرض الأنماط مع أمثلة
╚═✦═━《 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗮𝘇𝗲𝗳 ⛧ 》━═✦═╝
⌯ المطور: @T_8l8
"""
        await event.reply(menu)

    @client.on(events.NewMessage(pattern=r'^\.ترجمه$'))
    async def translate_message(event):
        if not event.reply_to_msg_id:
            await event.reply("⚠️ يرجى الرد على الرسالة المراد ترجمتها")
            return
        reply_msg = await event.get_reply_message()
        text = reply_msg.text
        if not text:
            await event.reply("⚠️ لا يوجد نص للترجمة في الرسالة المرد عليها")
            return
        translated = translate_text(text, "ar")
        await event.reply(f"🌍 الترجمة:\n\n{translated}")

    @client.on(events.NewMessage(pattern=r'^\.زخرفه (.*)'))
    async def decorate_message(event):
        full_text = event.pattern_match.group(1).strip()
        if not full_text:
            await event.reply("⚠️ يرجى كتابة النص المراد زخرفته بعد الأمر")
            return

        parts = full_text.split(maxsplit=1)
        if len(parts) == 2 and parts[0] in EN_DECORATION_TEMPLATES:
            style = parts[0]
            text = parts[1]
        else:
            style = None
            text = full_text

        decorated = decorate_text(text, style=style)
        await event.reply(f"✨ النص المزخرف:\n\n{decorated}")

    @client.on(events.NewMessage(pattern=r'^\.انماط الزخرفه$'))
    async def show_styles(event):
        sample_text = "Bubble"
        msg = "📜 أنماط الزخرفة المتاحة مع أمثلة:\n\n"
        for style, _ in EN_DECORATION_TEMPLATES.items():
            decorated = decorate_text(sample_text, style=style)
            msg += f"✧ {style}: {decorated}\n"
        await event.reply(msg)
