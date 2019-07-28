import vk_api, random, sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType

#делаем функцию отправки сообщения покороче
def send_it(user_id, message):
    random_id = random.randint(100000000, 999999999)
    vk.method('messages.send', {'user_id':user_id, 'random_id':random_id, 'message':message})

#авторизуемся в вк
token = 'token'
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

#проверяем, есть ли файл бд, создаем, если нет
try:
    db_file = open('hataraku.db', 'r')
except FileNotFoundError or IOError:
    db_file = open('hataraku.db', 'w')
db_file.close()

#соединяемся с дб, создаем таблицу, если такой еще не существует
conn = sqlite3.connect("hataraku.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS head
                  (vk_id TEXT, name TEXT,
                   age TEXT, exp TEXT,
                   skills TEXT, education TEXT,
                   about TEXT)"""
                )

#начинаем беседу
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
#создаем запись о новом соискателе

            if request.lower().rfind('хочу работать!') != -1:
                cursor.execute("""INSERT INTO head
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (event.user_id, 'None', 'None', 'None', 'None', 'None', 'None')
               )
                conn.commit()
                send_it(event.user_id, '''Это замечательно!\nДля начала, мне хотелось бы узнать как Вас зовут. Чтобы я верно Вас поняла, отправьте:\n\nМеня зовут - \"Ваши ФИО\".\n\nНапример:\n\nМеня зовут - Бот Хатараку Пайтоновна''')

#добавляем имя в бд
            elif request.lower().rfind('меня зовут - ') != -1:
                cursor.execute("""UPDATE head 
                    SET name = ? 
                    WHERE vk_id = ?""", (request.lower().replace('меня зовут - ', ''), event.user_id)
                )
                conn.commit()
                send_it(event.user_id, '''Приятно с вами познакомиться! Теперь мне хотелось бы узнать ваш возраст.\nМожете указать таким образом:\n\nМой возраст - \"ваш позраст\".\n\nНапример:\n\nМой возраст - 25 лет''')

#добавляем возраст в бд
            elif request.lower().rfind('мой возраст - ') != -1:
                cursor.execute("""UPDATE head 
                    SET age = ? 
                    WHERE vk_id = ?""", (request.lower().replace('мой возраст - ', ''), event.user_id)
                )
                conn.commit()
                send_it(event.user_id, '''Отлично! Так же мне очень интересено какой у вас опыт программирования. Его вы можете указать после фразы \"Мой опыт\".\n\nНапример:\n\nМой опыт - отсутствует\n\nили\n\nМой опыт - Тимлид 1 год в комании \"Программистеры\"''')

#добавляем запись об опыте работы в бд
            elif request.lower().rfind('мой опыт - ') != -1:
                cursor.execute("""UPDATE head 
                    SET exp = ? 
                    WHERE vk_id = ?""", (request.lower().replace('мой опыт - ', ''), event.user_id)
                )
                conn.commit()
                send_it(event.user_id, '''А какими навыками вы обладаете? Опишите, пожалуйста, через запятую:\n\nМои навыки - \"ваши навыки\".\n\nНапример:\n\nМои навыки - Python, C++/C, Java''')

#добавляем запись о навыках в бд
            elif request.lower().rfind('мои навыки - ') != -1:
                cursor.execute("""UPDATE head 
                    SET skills = ? 
                    WHERE vk_id = ?""", (request.lower().replace('мои навыки - ', ''), event.user_id)
                )
                conn.commit()
                send_it(event.user_id, '''Чудесно! Вы изучали это самостоятельно или в учебном заведении? Да, кстати, можете рассказать мне о вашем образовании?\n\nНапример:\n\nМое образование - НГТУ им. Алексеева, ИРИТ, Прикладная математика, 2 года''')

#добавляем запись об образовании в бд
            elif request.lower().rfind('мое образование - ') != -1:
                cursor.execute("""UPDATE head 
                    SET education = ? 
                    WHERE vk_id = ?""", (request.lower().replace('мое образование - ', ''), event.user_id)
                )
                conn.commit()
                send_it(event.user_id, '''Я думаю, что работадателю так же будет очень интересно узнать о ваших хобби, увлечениях, личных достижениях. Рассказать ему об этом можно фразой:\n\nОбо мне - \"дополнительная информация о Вас\"\n\nНапример:\n\nОбо мне - в свободное время отвечаю на вопросы соискателей под псевдонимом @hataraku_hr(Hataraku HR Bot)''')

#добавляем дополнительную информацию о соискателе и прощаемся
            elif request.lower().rfind('обо мне - ') != -1:
                cursor.execute("""UPDATE head 
                    SET about = ? 
                    WHERE vk_id = ?""", (request.lower().replace('обо мне - ', ''), event.user_id)
                )
                conn.commit()
                send_it(event.user_id, '''Замечательно! Спасибо, что рассказали мне так много интересного о себе. Мы свяжемся с Вами в ближайшее время посредством \"Вконтакте\".\n Всего доброго! &#128522;''')

#если нет соответствий - приветствие
            else:
                send_it(event.user_id, '''Здравствуйте! Меня зовут - @hataraku_hr(Hataraku HR Bot), бот для социальной сети \"ВКонтакте\".\n\nЕсли вас интересует работа, отправьте мне : "Хочу работать!".''')
