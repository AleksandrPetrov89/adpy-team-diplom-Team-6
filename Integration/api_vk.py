from config import vk_app_token
import requests
import os
import json
import re
from datetime import datetime
from datetime import date


# TODO Добавить проверку на дубль выдачи
# TODO Добавить вывод, что в вашем городе подходящих кандидатов не осталось
# TODO Добавить проверку на ЧС
# TODO Добавить передачу инфы в БД
class VKApiRequests:
    URL = 'https://api.vk.com/method/'

    def __init__(self, vk_user_id, vk_user_token):
        self.user_token = vk_user_token
        self.user_id = vk_user_id
        if os.path.exists(f'Saved_sessions/Session_{self.user_id}.json'):
            with open(f'Saved_sessions/Session_{self.user_id}.json', 'r', encoding='utf-8') as f:
                self.user_info = json.load(f)
                self.first_name = self.user_info['first_name']
                self.second_name = self.user_info['second_name']
                self.age = self.user_info['age']
                self.sex = self.user_info['sex']
                self.partner_sex = self.user_info['partner_sex']
                self.city_id = self.user_info['city_id']
                self.groups = self.user_info['groups']
                self.interests = self.user_info['interests']
                self.music = self.user_info['music']
                self.books = self.user_info['books']
                self.offset = self.user_info['offset']
                self.match_users = self.user_info['match_users']
                self.viewed_users_id = self.user_info['viewed_users_id']
        else:
            self._get_init_user_info()

    def _get_init_user_info(self):
        method = 'users.get'
        params = {
            'user_ids': self.user_id,
            'fields': 'bdate, sex, city, music, interests, books',
            'access_token': self.user_token,
            'v': '5.131'
        }
        resp = requests.get(VKApiRequests.URL + method, params=params).json()
        check_errors(resp, self.user_id)
        giui_user_info = resp.json()
        self.viewed_users_id = []
        self.first_name = giui_user_info['response'][0]['first_name']
        self.second_name = giui_user_info['response'][0]['last_name']
        self.sex = giui_user_info['response'][0]['sex']
        if len(giui_user_info['response'][0]['bdate'].split('.')) == 3:
            birth_year = giui_user_info['response'][0]['bdate'][-1:-4]
        else:
            birth_year = None
        if birth_year:
            self.age = int(date.today()[:4]) - int(birth_year)
        else:
            self.age = None
        if giui_user_info['response'][0]['city']['id'] == '' or giui_user_info['response'][0]['city']['id'] is None:
            city_id = None
        else:
            city_id = giui_user_info['response'][0]['city']['id']
        self.city_id = city_id
        if giui_user_info['response'][0]['interests'] is None or giui_user_info['response'][0]['interests'] == '':
            interests = None
        else:
            interests = giui_user_info['response'][0]['interests']
        self.interests = interests
        if giui_user_info['response'][0]['music'] is None or giui_user_info['response'][0]['music'] == '':
            music = None
        else:
            music = giui_user_info['response'][0]['music']
        self.music = music
        if giui_user_info['response'][0]['books'] is None or giui_user_info['response'][0]['books'] == '':
            books = None
        else:
            books = giui_user_info['response'][0]['books']
        self.books = books
        self.groups = self._get_user_groups(self.user_id)
        self.offset = 0
        if self.sex == 1:
            self.partner_sex = self.sex + 1
        elif self.sex == 2:
            self.partner_sex = self.sex - 1

    def is_city_byear_exists(self):
        """
        Метод проверяет наличие данных о городе и годе рождения.
        Выводит - int
        1 - Надо получить и год, и город
        2 - Надо получить только год
        3 - Надо получить только город
        0 - Всё есть, ничего не надо
        """
        if self.age is None and self.city_id is None:
            result = 1
        elif self.age is None and self.city_id:
            result = 2
        elif self.age and self.city_id is None:
            result = 3
        else:
            result = 0
        return result

    def give_me_city_byear(self, city_name=None, birth_year=None):
        """
        Метод, который принимает полученную информацию от пользователя и вносит в атрибуты.
        """
        if city_name:
            self.city_id = self._get_city_id(city_name)
        if birth_year:
            self.age = int(date.today()[:4]) - int(birth_year)

    def _get_city_id(self, name):
        method = 'database.getCities'
        params = {
            'country_id': 1,
            'q': name,
            'count': 1,
            'access_token': self.user_token,
            'v': '5.131'
        }
        resp = requests.get(VKApiRequests.URL + method, params=params)
        check_errors(resp, self.user_id)
        result = resp.json()['response']['items']['id']
        return result

    def _get_user_groups(self, id_):
        method = 'groups.get'
        params = {
            'user_id': id_,
            'count': 1000,
            'access_token': self.user_token,
            'v': '5.131'
        }
        resp = requests.get(VKApiRequests.URL + method, params=params)
        check_errors(resp, self.user_id)
        result = resp.json()['response']['items']
        return result

    def give_me_candidates(self):
        """
        Метод запроса кандидатов.
        Выводит словарь в формате
            {
             user_id(int): {
                        'first_name': str,
                        'last_name': str,
                        'photo_links': [str,str,str...]
             }
        }
        """
        if self.match_users:
            return self.match_users
        else:
            self._get_candidates()
            return self.match_users

    def save_session(self, candidate_id):
        """
        Метод удаляет из списка кандидатов последнего просмотренного
        и сохраняет текущие данные пользователя и его списка кандидатов в файл сессии
        """
        self.match_users.pop(candidate_id)
        dict_for_save = {
            'first_name': self.first_name,
            'second_name': self.second_name,
            'age': self.age,
            'sex': self.sex,
            'partner_sex': self.partner_sex,
            'city_id': self.city_id,
            'groups': self.groups,
            'interests': self.interests,
            'music': self.music,
            'books': self.books,
            'offset': self.offset,
            'match_users': self.match_users,
            'viewed_users_id': self.viewed_users_id
        }
        with open(f'Saved_sessions/Session_{self.user_id}.json', 'w', encoding='utf-8') as f:
            json.dump(dict_for_save, f)

    # Собираем список подходящих кандидатов
    def _get_candidates(self):
        """
        Метод собирает перечень из 1000 пользователей из указанного города, сортирует их по совпдаению на
        возрастной диапазон, интересы, музыку, книги, группы, проверяет id кандидатов на предмет дубля выдачи
        и формирует итоговый перечень кандидатов
        """
        method = 'users.search'
        params = {
            'offset': self.offset,
            'count': 1000,
            'status': 6,
            'fields': 'bdate, music, interests, books',
            'city': self.city_id,
            'country': 1,
            'sex': self.partner_sex,
            'has_photo': 1,
            'access_token': self.user_token,
            'v': '5.131'
        }
        resp = requests.get(VKApiRequests.URL + method, params=params)
        check_errors(resp, self.user_id)
        match_users_raw = resp.json()
        for users in match_users_raw['response']['items']:
            m_user_id = users.values()['id']
            if m_user_id in self.viewed_users_id:
                continue
            m_first_name = users.values()['first_name']
            m_last_name = users.values()['last_name']
            if len(users.values()['bdate'].split('.')) == 3:
                m_birth_year = users.values()['bdate'][-1:-4]
                m_age = int(date.today()[:4]) - int(m_birth_year)
            else:
                continue
            m_interests = users.values()['interests']
            m_books = users.values()['books']
            m_music = users.values()['music']
            m_groups = self._get_user_groups(m_user_id)
            photo_inf = self._get_photo_links(users.values()['id'])
            m_photo_links = {}
            for item, value in photo_inf.items():
                m_photo_links[item] = value['photo_link']
            match_users_dict = {
                'first_name': m_first_name,
                'last_name': m_last_name,
                'photo_links': m_photo_links
            }
            if m_age == self.age:
                self.match_users[m_user_id] = match_users_dict
                self.viewed_users_id.append(m_user_id)
                continue
            elif (self.age - 10 <= m_age <= self.age - 1 or self.age + 1 <= m_age <= self.age + 10) and m_age > 18:
                cont_trigger = 0
                if m_interests:
                    for inter in m_interests:
                        if re.match(inter, self.interests, flags=0):
                            self.match_users[m_user_id] = match_users_dict
                            self.viewed_users_id.append(m_user_id)
                            cont_trigger = 1
                    if cont_trigger:
                        continue
                elif m_books:
                    for book in m_books:
                        if re.match(book, self.books, flags=0):
                            self.match_users[m_user_id] = match_users_dict
                            self.viewed_users_id.append(m_user_id)
                            cont_trigger = 1
                    if cont_trigger:
                        continue
                elif m_music:
                    for music in m_music:
                        if re.match(music, self.music, flags=0):
                            self.match_users[m_user_id] = match_users_dict
                            self.viewed_users_id.append(m_user_id)
                            cont_trigger = 1
                    if cont_trigger:
                        continue
                elif m_groups:
                    for group in m_groups:
                        if re.match(group, self.groups, flags=0):
                            self.match_users[m_user_id] = match_users_dict
                            self.viewed_users_id.append(m_user_id)
        self.offset += 999

    def _get_photo_links(self, owner_id):
        method = 'photos.get'
        params_profile = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'access_token': self.user_token,
            'v': '5.131'
        }
        params_with = {
            'owner_id': owner_id,
            'album_id': -9000,
            'extended': 1,
            'access_token': self.user_token,
            'v': '5.131'
        }
        resp_profile = requests.get(VKApiRequests.URL + method, params=params_profile)
        check_errors(resp_profile, self.user_id)
        photo_info_profile = resp_profile.json()
        resp_with = requests.get(VKApiRequests.URL + method, params=params_with)
        check_errors(resp_with, self.user_id)
        photo_info_with = resp_with.json()
        profile_dict = self._raw_photo_dict(photo_info_profile)
        with_dict = self._raw_photo_dict(photo_info_with)
        photo_dict = profile_dict | with_dict
        return photo_dict

    def _raw_photo_dict(self, api_response):
        result_dict = {}
        unsort_dict = {}
        for photo in api_response['response']['items']:
            likes = photo['likes']['count']
            photo_id = photo['id']
            photo_link = photo['sizes'][-1]['url']
            result_dict[photo_id] = {
                'likes': likes,
                'photo_link': photo_link
            }
            unsort_dict[photo_id] = likes
        if len(unsort_dict.items()) > 3:
            sort_dict = sorted(unsort_dict.items(), key=lambda x: x[1])
            for item in [id_ for id_ in dict(sort_dict)][:-3]:
                result_dict.pop(item)
        return result_dict

    def smash_like(self, candidate_id, photo_id):
        """
        Получает id кандидата и id фото на которую ставить лайк.
        Ставит лайк, отправляет данные в БД словарём в формате:
            {
             user_id(int): {
                        'candidate_id': int,
                        'photo_id': int
             }
         }
        """
        method = 'likes.add'
        params = {
            'type': 'photo',
            'owner_id': candidate_id,
            'item_id': photo_id,
            'access_token': self.user_token,
            'v': '5.131'
        }
        resp = requests.post(VKApiRequests.URL + method, params=params)
        check_errors(resp, self.user_id)
        result = 'Поставили лайк'
        return result

    def delete_like(self, candidate_id, photo_id):
        method = ''


def check_errors(response, user_id):
    """
    Функция проверяет наличие ошибки в ответе на АПИ запрос, заносит ошибку в лог и выводит строку об ошибке
    """
    resp_error = str(response).split()[1]
    with open('Errors/vk_errors.json', 'r', encoding='utf-8') as f:
        errors = json.load(f)
        if resp_error in errors.keys():
            with open(f'Logs/log_{user_id}.txt', 'a', encoding='utf-8') as file:
                json.dumps(f'{datetime.now()}\nОшибка: {resp_error}\n{errors[resp_error]}\n-------\n')
            result = 'Произошла непредвиденная ошибка! Пожалуйста, обратитесь к администратору или попробуйте позже.'
            return result