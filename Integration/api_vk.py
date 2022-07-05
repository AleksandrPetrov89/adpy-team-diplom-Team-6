from config import vk_app_token
import requests
import os
import json
from datetime import date


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
        else:
            self._get_init_user_info()

    #Сбор данных из профиля и распределение по атрибутам
    def _get_init_user_info(self):
        METHOD = 'users.get'
        params = {
            'user_ids': self.user_id,
            'fields': 'bdate, sex, city, music, interests, books',
            'access_token': self.user_token,
            'v': '5.131'
        }
        user_info = requests.get(VKApiRequests.URL + METHOD, params=params).json()
        self.first_name = user_info['response'][0]['first_name']
        self.second_name = user_info['response'][0]['last_name']
        self.sex = user_info['response'][0]['sex']
        if len(user_info['response'][0]['bdate'].split('.')) == 3:
            birth_year = user_info['response'][0]['bdate'][-1:-4]
        else:
            # вызов функции бота для запроса года рождения
            birth_year = give_me_birth_year()
        self.age = int(birth_year) - int(date.today()[:4])
        if user_info['response'][0]['city']['id'] == '' or user_info['response'][0]['city']['id'] is None:
            a # Вызов функции бота для запроса города поиска
            city_name = give_me_city()
            a # Определение id города по имени
            city_id = _get_city_id(city_name)
        else:
            city_id = user_info['response'][0]['city']['id']
        self.city_id = city_id
        if user_info['response'][0]['interests'] is None or user_info['response'][0]['interests'] == '':
            interests = None
        else:
            interests = user_info['response'][0]['interests']
        self.interests = interests
        if user_info['response'][0]['music'] is None or user_info['response'][0]['music'] == '':
            music = None
        else:
            music = user_info['response'][0]['music']
        self.music = music
        if user_info['response'][0]['books'] is None or user_info['response'][0]['books'] == '':
            books = None
        else:
            books = user_info['response'][0]['books']
        self.books = books
        self.groups = self._get_user_groups(self.user_id)
        self.offset = 0
        if self.sex == 1:
            self.partner_sex = self.sex + 1
        elif self.sex == 2:
            self.partner_sex = self.sex - 1

    def _get_city_id(self, name):
        METHOD = 'database.getCities'
        params = {
            'country_id': 1,
            'q': name,
            'count': 1,
            'access_token': self.user_token,
            'v': '5.131'
        }
        result = requests.get(VKApiRequests.URL + METHOD, params=params).json()['response']['items']['id']
        return result

    def _get_user_groups(self, id_):
        METHOD = 'groups.get'
        params = {
            'user_id': id_,
            'count': 1000,
            'access_token': self.user_token,
            'v': '5.131'
        }
        result = requests.get(VKApiRequests.URL + METHOD, params=params).json()['response']['items']
        return result

    # Собираем список подходящих кандидатов
    def get_match_users(self):
        METHOD = 'users.search'
        params = {
            'offset': self.offset,
            'count': 1000,
            'fields': 'music, interests, books',
            'city': self.city_id,
            'country': 1,
            'sex': self.partner_sex,
            'age_from': self.age - 2,
            'age_to': self.age + 2,
            'has_photo': 1,
            'access_token': self.user_token,
            'v': '5.131'
        }
        match_users_raw = requests.get(VKApiRequests.URL + METHOD, params=params).json()
        for users in match_users_raw['response']['items']:
            m_user_id = users.values()['id']
            m_first_name = users.values()['first_name']
            m_last_name = users.values()['last_name']
            m_interests = users.values()['interests']
            m_books = users.values()['books']
            m_music = users.values()['music']
            m_groups = self._get_user_groups(m_user_id)
            m_photo_links =
            match_users_dict = {
                'first_name': m_first_name,
                'last_name': m_last_name,
                'interests': m_interests,
                'books': m_books,
                'music': m_music,
                'groups': m_groups
            }
            self.match_users[m_user_id] = match_users_dict
        self.offset += 999

    def _get_photo_links(self):
        METHOD = ''
