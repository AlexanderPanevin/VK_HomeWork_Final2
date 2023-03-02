import vk_api
from vk_api.longpoll import VkLongPoll
from settings import bot_token
from random import randrange
from vk_api.exceptions import ApiError
import sys

vk = vk_api.VkApi(token=bot_token)
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    try:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})
    except ApiError:
        for event in longpoll.listen():
                      write_msg(event.user_id,'К сожалению, получился слишком длинный список. Покажу в следующий раз. Перезапусти программу "бот"')
                      sys.exit()
        print('ошибка ApiError "слишком длинное сообщение"' )
    else:
        return

def send_photo(user_id, message, attachments):
    try:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': ','.join(attachments),
                                    'random_id': randrange(10 ** 7), })
    except TypeError:
        for event in longpoll.listen():
                      write_msg(event.user_id,'К сожалению, не могу показать фото.')
                      break
        print('ошибка TypeError в модуле send_photo')
        pass
    else:
        return

