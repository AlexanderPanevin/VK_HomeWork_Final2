import requests
from requests.exceptions import HTTPError
from settings import user_token, V
import time

class Handler:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = user_token
        self.version = V
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_user_info(self, user_id):
        user_info_url = self.url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'sex, bdate, relation, city, home_town',
            'name_case': 'nom'
        }
        resp = requests.get(user_info_url, params={**self.params, **user_params})
        respJS = resp.json()
        for url in [user_info_url]:
            try:
                resp = requests.get(url)
                print('resp',resp)
                resp.raise_for_status()
                print('raise_for_status',resp.raise_for_status)
            except HTTPError as http_err:
                print(f'HTTP-ошибка: {http_err}')
            except Exception as err:
                print(f'Другая ошибка: {err}')
            else:
                print('Успешное соединение get_user')
        # print(respJS)
        return respJS

    def users_search(self, get_user_info, sex, age_from, age_to, relation, home_town):
        persone_id_list = []
        while True:
            for items in get_user_info['response']:
                users_search_url = self.url + 'users.search'
                user_params = {
                    'count': 20,
                    'has_photo': 1,
                    'sex': sex,
                    'age_from': age_from,
                    'age_to': age_to,
                    'relation': relation,
                    'home_town': home_town
                }
                response = requests.get(users_search_url, params={**self.params, **user_params}).json()
                if 'error' in response and response['error'].get('error_code') == 6:
                    time.sleep(1.0)
                    print('перекур')
                    break
                try:
                    pass
                except TypeError as type_err:
                    print(f'Type_Error: {type_err}')
                except HTTPError as http_err:
                    print(f'HTTP-ошибка: {http_err}')
                except Exception as err:
                    print(f'Другая ошибка: {err}')
                else:
                    print(
                        'Успешное соединение user_search')
                persone_id_list = [item.get('id') for item in response['response']['items']]
                print(persone_id_list)
            return persone_id_list

    def get_persone_info(self, persone_id):
        user_info_url = self.url + 'users.get'
        user_params = {
            'user_ids': persone_id,
            'fields': 'sex, bdate, relation, city, home_town',
            'name_case': 'nom'
        }
        response = requests.get(user_info_url, params={**self.params, **user_params}).json()
        for url in [user_info_url]:
            try:
                resp = requests.get(url)
                resp.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP-ошибка: {http_err}')
            except Exception as err:
                print(f'Другая ошибка: {err}')
            else:
                print('Успешное соединение')
        # print(response)
        return response

    def get_photos(self, persone_id):
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': persone_id,
            'album_id': 'profile',
            'extended': '1',
            'can_comment': '0',
            'count': '20',
            'photo_sizes': '1'
        }
        try:
            response = requests.get(photos_url, params={**self.params, **photos_params}).json()
            photo_list = []
            best_photo_list = []
            for value in response.values():
                items = value.get('items')
                print(items)
                for item in items:
                    like_id_list = []
                    likes = item.get('likes')
                    like = likes.get('count')
                    like_id_list.append(like)
                    comment_id_list = []
                    comments = item.get('comments')
                    comment = comments.get('count')
                    comment_id_list.append(comment)
                    photo_id = item.get('id')
                    like_id_list.append(photo_id)
                    comment_id_list.append(photo_id)
                    photo_list.append(like_id_list)
                    photo_list.append(comment_id_list)
            photo_list.sort()
            print(photo_list)
            if len(photo_list) >= 3:
                best_photo_list.append(photo_list[-1])
                best_photo_list.append(photo_list[-2])
                best_photo_list.append(photo_list[-3])
            elif len(photo_list) == 2:
                best_photo_list.append(photo_list[-1])
                best_photo_list.append(photo_list[-2])
            else:
                best_photo_list.append(photo_list[-1])
            print(best_photo_list)
        except TypeError:
            print('ошибка TypeError в модуле get_photos')
            pass
        else:
            return best_photo_list

    def messages_send(self, get_photos, persone_id):
        global attachments
        try:
            if len(get_photos) == 3:
                photo1 = f'photo{persone_id}_{get_photos[0][1]}'
                photo2 = f'photo{persone_id}_{get_photos[1][1]}'
                photo3 = f'photo{persone_id}_{get_photos[2][1]}'
                attachments = [photo1, photo2, photo3]
            elif len(get_photos) == 2:
                photo1 = f'photo{persone_id}_{get_photos[0][1]}'
                photo2 = f'photo{persone_id}_{get_photos[1][1]}'
                attachments = [photo1, photo2]
            elif len(get_photos) == 1:
                photo1 = f'photo{persone_id}_{get_photos[0][1]}'
                attachments = [photo1]
        except TypeError:
            print ('ошибка TypeError в модуле messages_send')
            pass
        else:
            return attachments



