# -*- coding: utf-8 -*-
import requests
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from random import randint


headers = {"X-Yandex-API-Key": "прописать-API-ключ-от-Яндекс-погода"}
pogoda = requests.get(url="https://api.weather.yandex.ru/v2/informers?lat=54.735220&lon=55.959214&lang=ru_RU", headers = headers) # координаты насленного пункта
b = pogoda.json()


osad = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями', 'overcast': 'пасмурно',
       'drizzle': 'морось', 'light-rain': 'небольшой дождь', 'rain': 'дождь', 'moderate-rain': 'умеренно сильный дождь',
       'heavy-rain': 'сильный дождь', 'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
       'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег', 'snow-showers': 'снегопад',
       'hail': 'град', 'thunderstorm': 'гроза', 'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'}

wind = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное', 'se': 'юго-восточное',
's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'c': 'штиль'}

#print('Температура: ', b['fact']['temp'], ', ощущается как ', b['fact']['feels_like'], 
#      '\nДавление: ', b['fact']['pressure_mm'], ' мм рт.ст.\n',
#      'Влажность: ', b['fact']['humidity'], '%\n',
#      osad[b['fact']['condition']],
#      '\nветер:', b['fact']['wind_speed'], 'м/с, направление: ', wind[b['fact']['wind_dir']], sep='')
#print(pogoda.json())
#text = 'Температура: ' + str(b['fact']['temp']) + ', ощущается как ' + str(b['fact']['feels_like']) + '\nДавление: ' + str(b['fact']['pressure_mm']) + ' мм рт.ст.\n' + 'Влажность: ' + str(b['fact']['humidity']) + '%\n' + osad[b['fact']['condition']] + '\nветер:' + str(b['fact']['wind_speed']) + 'м/с, направление: ' + wind[b['fact']['wind_dir']];
#print(text)


# открываем фоновый рисунок
img = Image.open('D:/1.jpg') # путь к фоновому рисунку 800 х 500

new_width  = 800 # ширина фонового рисунка
new_height = int(new_width * img.size[1] / img.size[0])
img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

#вычисляем центр изображения
hs = img.size[0] / 2 # горизонт
vs = img.size[1] / 2 # вертикаль

# размер вставки
w1, h1, w2, h2 = (300, 400, 300, 400)

# первая картинка
im1 = ImageDraw.Draw(img, 'RGBA')
im1.rectangle((hs-w1, vs-h1/2, hs, vs + h1/2), fill=(100,100,200,230))

# вторая картинка
im2 = ImageDraw.Draw(img, 'RGBA')
im2.rectangle((hs, vs-h2/2, hs+w2, vs + h2/2), fill=(200,200,200,230))


# Название времени суток
part_name = {'night': 'ночью', 'morning': 'утром', 'day': 'днем', 'evening': 'вечером'}
# дни недели
day_week = {'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда', 'Thursday': 'четверг', 'Friday': 'пятница', 'Saturday': 'суббота', 'Sunday': 'воскресенье'}
# названия месяцев
month = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'май', '06': 'июнь', '07': 'июль', '08': 'август', '09': 'сентябрь', '10': 'окрябрь', '11': 'ноябрь', '12': 'декабрь'}


# начало формирования картинки с погодой
d = ImageDraw.Draw(img,'RGBA')

#фактическая температура
d.text((hs-w1/2, vs-h1/2+130), str(b['fact']['temp']), fill="white", anchor="ms", font=ImageFont.truetype("arial.ttf", 120))

#населенный пункт
d.text((hs-w1/2, vs-h1/2+180), 'ЦЕЛИННОЕ', fill="white", anchor="ms", font=ImageFont.truetype("arial.ttf", 40))

#осадки
d.text((hs-w1/2, vs-h1/2+220), osad[b['fact']['condition']], fill="white", anchor="ms", font=ImageFont.truetype("arial.ttf", 22))

#восход/заход солнца
d.text((hs-w1/2, vs-h1/2+270), 'ВОСХОД В ' + b['forecast']['sunrise'], fill="white", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))
d.text((hs-w1/2, vs-h1/2+300), 'ЗАХОД В ' + b['forecast']['sunset'], fill="white", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))

#дата
d.text((hs-w1/2, vs-h1/2+350), day_week[datetime.fromtimestamp(b['now']).strftime("%A")] + ', ' + datetime.fromtimestamp(b['now']).strftime("%d") + ' ' + month[datetime.fromtimestamp(b['now']).strftime("%m")], fill="white", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))


# Вторая картинка #
# температура первого периода
d.text((hs+w2/2, vs-h2/2+70), part_name[b['forecast']['parts'][0]['part_name']].upper() + ' ' +str(b['forecast']['parts'][0]['temp_avg']), fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 40))

#влажность
d.text((hs+w2/2, vs-h2/2+100), 'ВЛАЖНОСТЬ', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))
d.text((hs+w2/2, vs-h2/2+125), str(b['forecast']['parts'][0]['humidity'])+ '%', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))

#ветер
d.text((hs+w2/2, vs-h2/2+150), 'ВЕТЕР', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))
d.text((hs+w2/2, vs-h2/2+175), str(b['forecast']['parts'][0]['wind_speed'])+ ' м/с', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))

# температура второго периода
d.text((hs+w2/2, vs-h2/2+230), part_name[b['forecast']['parts'][1]['part_name']].upper() + ' ' +str(b['forecast']['parts'][1]['temp_avg']), fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 40))

#влажность
d.text((hs+w2/2, vs-h2/2+260), 'ВЛАЖНОСТЬ', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))
d.text((hs+w2/2, vs-h2/2+285), str(b['forecast']['parts'][1]['humidity'])+ '%', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))

#ветер
d.text((hs+w2/2, vs-h2/2+315), 'ВЕТЕР', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))
d.text((hs+w2/2, vs-h2/2+340), str(b['forecast']['parts'][1]['wind_speed'])+ ' м/с', fill="black", anchor="ms", font=ImageFont.truetype("arial.ttf", 20))


img.save('image_to_vk.png')
#img.show() # открыть картинку


# отправка картинки на сервер VK
token = 'токен-доступа-ВК'

# получение ссылки для отпарвки фото
param1 = {'access_token': token, 'group_id': ИД_ГРУППЫ, 'v': 5.131}
method = 'photos.getWallUploadServer'
get_address = requests.get(url=f'https://api.vk.com/method/{method}', params = param1)
#print('\n')
# ответ сервера
c = get_address.json()
print(c)

# загрузка файла на сервер
url = c['response']['upload_url'] # полученный url
# открываем файл на чтение в бинарном режиме ('rb')
fp = open('image_to_vk.png', 'rb')
# помещаем объект файла в словарь в качестве значения с ключом 'file'
files = {'file': fp}
# передаем созданный словарь аргументу `files`
upload = requests.post(url, files=files)
fp.close()
d = upload.json()
#print(c)
#print('\n')


# сохранение загруженного фото на сервере
param2 = {'access_token': token, 'group_id': ИД_ГРУППЫ, 'photo': d['photo'], 'server': d['server'], 'hash': d['hash'], 'v': 5.131}
method = 'photos.saveWallPhoto'
save_photo = requests.get(url=f'https://api.vk.com/method/{method}', params = param2)
#print(save_photo.json())
e = save_photo.json()

# запостить на стену сообщение + фото
param3 = {'access_token': token, 'owner_id': -ИД_ГРУППЫ, 'message': 'Доброе утро, город!',
         "attachments": 'photo'+str(e['response'][0]['owner_id'])+'_'+str(e['response'][0]['id']), 'v': 5.131}
method = 'wall.post'
rec4 = requests.get(url=f'https://api.vk.com/method/{method}', params = param3)
print(rec4.json())






