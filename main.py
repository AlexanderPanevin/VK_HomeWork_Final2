import sys
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from api import Handler
from database import Session, DB_User
from settings import bot_token, user_token, V
from vk_api.exceptions import ApiError
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from modules import send_photo
from random import randrange
import time

vk = vk_api.VkApi(token=bot_token)
longpoll = VkLongPoll(vk)
def write_msg(message_user_id, message):
    try:
        vk.method('messages.send', {'user_id': message_user_id, 'message': message, 'random_id': randrange(10 ** 7)})
    except ApiError:
        for longlist_event in longpoll.listen():
                      write_msg(longlist_event.user_id, 'К сожалению, получился слишком длинный список. Покажу в следующий раз. Перезапусти программу "бот"')
                      sys.exit()
        print('ошибка ApiError "слишком длинное сообщение"' )
    else:
        return
url = 'https://api.vk.com/method/'
bot_params = {
    'access_token': user_token,
    'v': V
}
class Bot:
    url = 'https://api.vk.com/method/'
    def __init__(self):
        self.token = user_token
        self.version = V
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
    @staticmethod
    def sex_persone():
        user_info_url = url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'sex'
        }
        response = requests.get(user_info_url, params={**bot_params, **user_params}).json()
        response_list = response['response']
        print(response_list)
        for i in response_list:
            if i.get('sex') == 2:
                sex = 1
                return sex
            elif i.get('sex') == 1:
                sex = 2
                return sex
            else:
                while True:
                    write_msg(user_id, 'Кого ищем?:\n1 - женщину;\n2 - мужчину')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            request = event.text.lower()
                            try:
                                sex = int(request)
                                print(sex)
                                if int(request) == 1 or str(request) == 2:
                                    pass
                                else:
                                    write_msg(event.user_id, 'Нужно ввести 1, если ищем женщину, а если мужчину, то 2')
                            except ValueError:
                                write_msg(event.user_id,
                                          'Нужно ввести цифру 1, если ищем женщину, а если мужчину, то цифру 2')
                                print('ошибка ввода цифры')
                                break
                            else:
                                return sex

    @staticmethod
    def age_from_persone():
        user_info_url = url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'bdate'
        }
        resp = requests.get(user_info_url, params={**bot_params, **user_params})
        response = resp.json()
        print('for age_from_person',response)
        try:
            response_list = response['response']
            for i in response_list:
                date = i.get('bdate')
                date_list = date.split('.')
                print(date_list)
                if len(date_list) == 3:
                    year_bdate = int(date_list[2])
                    year_today = int(datetime.date.today().year)
                    age_from = (year_today - year_bdate)-2
                    print(age_from)
                    return age_from
                elif len(date_list) != 3 or date not in response_list:
                    write_msg(user_id, 'Укажите минимально возможный возраст для поиска')
                    while True:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                request = event.text.lower()
                                try:
                                    age_from = int(request)
                                    if int(request) > 17:
                                        pass
                                    else:
                                        write_msg(event.user_id,
                                                  'Действует ограничение "не моложе 18 лет", введите другое значение возраста')
                                        break
                                except ValueError:
                                    write_msg(event.user_id, 'Неправильный ввод, надо  выбрать ЦИФРУ от 18 и больше')
                                    print('ошибка ввода цифры')
                                    break
                                else:
                                    return age_from
        except Exception as err:
                print(f'Другая ошибка: {err}')

    @staticmethod
    def age_to_persone():
        user_info_url = url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'bdate'
        }
        resp = requests.get(user_info_url, params={**bot_params, **user_params})
        response = resp.json()
        print('for age_to_person',response)
        try:
            response_list = response['response']
            for i in response_list:
                date = i.get('bdate')
                date_list = date.split('.')
                if len(date_list) == 3:
                    year_bdate = int(date_list[2])
                    year_today = int(datetime.date.today().year)
                    age_to = (year_today - year_bdate) + 2
                    return age_to
                elif len(date_list) != 3 or date not in response_list:
                    write_msg(user_id, 'Укажите максимально возможный возраст для поиска')
                    while True:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                request = event.text.lower()
                                try:
                                    age_to = int(request)
                                    if age_to > int(Bot.age_from_persone()):
                                        pass
                                    else:
                                        write_msg(event.user_id,
                                                  'Значение верхней границы возраста должно быть больше выбранной нижней границы')
                                        break
                                except ValueError:
                                    write_msg(event.user_id,
                                              'Неправильный ввод, надо  выбрать ЦИФРУ от 18 и больше')
                                    print('ошибка ввода цифры')
                                    break
                                else:
                                    return age_to
        except Exception as err:
            print(f'Другая ошибка: {err}')

    @staticmethod
    def relat_persone():
        global data_relation
        user_info_url = url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'relation'
        }
        resp = requests.get(user_info_url, params={**bot_params, **user_params})
        time.sleep(0.5)
        response = resp.json()
        print('relat',response)
        try:
            response_list = response['response']
            print('response_list',response_list)
            for i in response_list:
                print('i.get(relation)', i.get('relation'))
                if i.get('relation') != 0:
                    data_relation = i.get('relation')
                    return data_relation
                    pass
                else:
                    pass

        except KeyError:
            print(KeyError)
            pass
        else:
            write_msg(user_id,
                      'Выбери семейное положение кандидата:\n1 - не женат(не замужем);'
                      '\n2 - встречается;\n3 - помолвлен(-а); \n4 - женат (замужем); \n5 - всё сложно;'
                      '\n6 - в активном поиске; \n7 - влюблен(-а); \n8 - в гражданском браке.'
                      )
            while True:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        request = event.text.lower()
                        try:
                            data_relation = int(request)
                            if 0 < int(request) < 9:
                                print('выбрано',data_relation )
                                return data_relation
                                pass
                            else:
                                write_msg(event.user_id, 'Введена неправильная цифра, надо выбрать от 1 до 8')
                                break
                        except ValueError:
                            write_msg(event.user_id, 'Неправильный ввод, надо  выбрать ЦИФРУ от 1 до 8')
                            print('ошибка ввода цифры')
                            break

    @staticmethod
    def home_town_persone ():
        user_info_url = url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'home_town'
        }
        resp = requests.get(user_info_url, params={**bot_params, **user_params})
        time.sleep(0.4)
        response = resp.json()
        print('response',response)
        try:
            response_list = response['response']
            print('response_list',response_list)
            response_dict = response_list[0]
            print('response_dict', response_dict)
            for i in response_list:
                if 'home_town' in response_dict.keys() and response_dict['home_town'] !='':
                    print(i.get('home_town'))
                    home_town = i.get('home_town')
                    print('i.get(home_town)',home_town)
                    return home_town
                    pass
                else:
                    write_msg(user_id,'Введите название своего города')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            request = event.text.lower()
                            print('request',request)
                            try:
                                home_town = request
                                return home_town
                                pass
                            except Exception:
                                print(TypeError)
                                break

        except KeyError:
            print(KeyError)
            pass
        else:
            pass
Bot()

if __name__ == '__main__':
        global user_id
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.lower()
                user_id = str(event.user_id)
                msg = event.text.lower()
                print(user_id)
                if request == 'бот':
                    write_msg(event.user_id, 'Привет! Начнём поиск?')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            request = event.text.lower()
                            if request == 'нет':
                                write_msg(event.user_id, 'Если буду нужен, вызови меня, напиши "бот"')
                                break
                            elif request != 'нет' and request != 'да':
                                write_msg(event.user_id, 'Нужно написать "да" или "нет"')
                                break
                            elif request == 'да':
                                sex = Bot.sex_persone()
                                age_from = Bot.age_from_persone()
                                print(f'Диапазон поиска составит от {age_from}')
                                age_to = Bot.age_to_persone()
                                print(f'до {age_to} лет')
                                status = int(Bot.relat_persone())
                                print('relation', status)
                                hometown = str.capitalize(Bot.home_town_persone())
                                print(f'Bot home_town, {hometown}')
                                write_msg(event.user_id, 'Результаты поиска')
                                vk_client = Handler(bot_token, V)
                                get_user_info = vk_client.get_user_info(event.user_id)
                                print(f'get_user_info, {get_user_info}')
                                get_persone_info = vk_client.get_persone_info(event.user_id)
                                print(f'get_persone_info, {get_persone_info}')
                                users_search = vk_client.users_search(get_user_info, sex, age_from, age_to, status, hometown)
                                print(f'users_search, {users_search}')
                                persones_list = []
                                while True:
                                    for persone_id in users_search:
                                        try:
                                            get_photos = vk_client.get_photos(persone_id)
                                            get_pers_inf = vk_client.get_persone_info(persone_id)
                                            get_attachments = vk_client.messages_send(get_photos, persone_id)
                                            send_photo(event.user_id, f'Персона vk.com/id{persone_id}', get_attachments)
                                        except ApiError:
                                            print('Hет доступа к фото')
                                        persones_data = DB_User(name=f'vk.com/id{persone_id}')
                                        with Session() as session:
                                            try:
                                                session.add(persones_data)
                                                session.commit()
                                            except (IntegrityError, UniqueViolation):
                                                print('попытка дублирующей записи')
                                                write_msg(event.user_id,
                                                          'Пошли по второму кругу. Продолжить?')
                                                session.rollback()
                                            else:
                                                add_result = session.query(DB_User).all()
                                        for item in add_result:
                                            name = item.name
                                            persones_list.append(name)
                                            print(persones_list)
                                        write_msg(event.user_id, 'Продолжаем искать?')
                                        for event in longpoll.listen():
                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                request = event.text.lower()
                                                if request == 'да':
                                                    break
                                                else:
                                                    write_msg(
                                                        event.user_id,
                                                        f'Поиск закончен. '
                                                        f'Вот список найденных кандидатов.:{persones_list}'
                                                        f'\n Продолжить!'
                                                    )
                                                    for event in longpoll.listen():
                                                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                            request = event.text.lower()
                                                            if request != 'да':
                                                                write_msg(
                                                                    event.user_id, f'До свидания!')
                                                                session.close()
                                                                sys.exit()
                                                            else:
                                                                write_msg(
                                                                    event.user_id,
                                                                    f'Продолжаем поиск по тем же критериям?')
                                                                break

