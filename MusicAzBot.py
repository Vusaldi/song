from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from youtube_search import YoutubeSearch
from config import Config
from pyrogram.handlers import MessageHandler
import os
import youtube_dl
import requests
import time
#Qurulum
bot = Client(
    'RcSongBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)
#Saat funksiyası
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))
## Əmrlər --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    darkprince = f'[👋](https://telegra.ph/file/cc97cc907aa3e4faa0fbf.jpg) Salam @{message.from_user.username}\n\nMən sizin üçün musiqini yükləmə botuyam.Məndən istifadə etmək çox asanddır.\nMusiqi  yükləmək üçün:\n1) /song (musiqinin adı)\n2) /song (youtubeden birlink)\nXəta əmələ gələrsə sahiblə əlaqə yaradın'
    message.reply_text(
        text=darkprince, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('🧑‍💻Sahib', url='https://t.me/Roxy_Boss'),
                    InlineKeyboardButton('🤖Support🤖', url='https://t.me/rcteamsupport'),
                    InlineKeyboardButton('❤Meni Qrupa Elave Ele❤', url='https://t.me/RcSongBot?startgroup=a')
                  ],[
                    InlineKeyboardButton('Sahib', url='T.me/Roxy_Boss')
                ]
            ]
        )
    )
@bot.on_message(filters.command(['song']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🎧Musiqini Axtariram...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Dostum musiqini tapa bilmirəm🤕. Xaiş edirəm mənə 1 şans daha ver 🥲')
            return
    except Exception as e:
        m.edit(
            "Dostum musiqini tapa bilmirəm🤕. Xaiş edirəm mənə 1 şans daha ver 🥲"
        )
        print(str(e))
        return
    m.edit("🔹️Musiqini Tapmisam Bu Deyqe Yukleyirem🔘")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🇦🇿 **Başlıq**: [{title[:35]}]({link})\n⏳ **Deqiqe**: `{duration}`\n👁‍🗨 **Goruntu sayi**: `{views} @piramidasohbet -Sohbet Kanalimiza Qatilmagi Unutma`'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('Xaiş edirəm bu mesajı sahibimə xəbərdar ele!')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
