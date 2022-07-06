from config import vk_app_token
import requests
import os
import json
import re
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
                self.viewed_users_id = self.user_info['viewed_users_id']
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
        self.viewed_users_id = []
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
            city_id = self._get_city_id(city_name)
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

    def give_me_candidates(self):
        if self.match_users:
            return self.match_users
        else:
            self._get_candidates()
            return self.match_users

    def save_session(self, candidate_id):
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
        METHOD = 'users.search'
        params = {
            'offset': self.offset,
            'count': 1000,
            'fields': 'bdate, music, interests, books',
            'city': self.city_id,
            'country': 1,
            'sex': self.partner_sex,
            'has_photo': 1,
            'access_token': self.user_token,
            'v': '5.131'
        }
        match_users_raw = requests.get(VKApiRequests.URL + METHOD, params=params).json()
        for users in match_users_raw['response']['items']:
            m_user_id = users.values()['id']
            m_first_name = users.values()['first_name']
            m_last_name = users.values()['last_name']
            m_age = 0
            if len(users.values()['bdate'].split('.')) == 3:
                m_birth_year = users.values()['bdate'][-1:-4]
                m_age = int(m_birth_year) - int(date.today()[:4])
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
                continue
            elif self.age - 10 <= m_age <= self.age - 1 or self.age + 1 <= m_age <= self.age + 10:
                if m_interests:
                    cont_trigger = 0
                    for inter in m_interests:
                        if re.match(inter, self.interests, flags=0):
                            self.match_users[m_user_id] = match_users_dict
                            cont_trigger = 1
                    if cont_trigger == 1:
                        continue
                elif m_books:
                    cont_trigger = 0
                    for book in m_books:
                        if re.match(book, self.books, flags=0):
                            self.match_users[m_user_id] = match_users_dict
                            cont_trigger = 1
                    if cont_trigger == 1:
                        continue
                elif m_music:
                    cont_trigger = 0
                    for music in m_music:
                        if re.match(music, self.music, flags=0):
                            self.match_users[m_user_id] = match_users_dict
                            cont_trigger = 1
                    if cont_trigger == 1:
                        continue
                elif m_groups:
                    for group in m_groups:
                        if re.match(group, self.groups, flags=0):
                            self.match_users[m_user_id] = match_users_dict
        self.offset += 999

    def _get_photo_links(self, owner_id):
        METHOD = 'photos.get'
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
        photo_info_profile = requests.get(VKApiRequests.URL + METHOD, params=params_profile).json()
        photo_info_with = requests.get(VKApiRequests.URL + METHOD, params=params_with).json()
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

    def smash_like(self):
        pass
