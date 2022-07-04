from config import vk_app_token
import requests



class VKApiRequests:
    URL = 'https://api.vk.com/method/'

    def __init__(self, vk_user_screen_name):
        self.user_token = None
        self.vk_user_id = None
        self.first_name = None
        self.second_name = None
        self.birthday = None
        self.sex = None
        self.city = None
        self.groups = None
        self._get_init_user_info(vk_user_screen_name)

    def _get_init_user_info(self, screen_name):
        METHOD = 'users.get'
        params = {
            'user_ids': screen_name,
            'fields': 'bdate, sex, city',
            'access_token': vk_app_token,
            'v': '5.131'
        }
        user_info = requests.get(VKApiRequests.URL + METHOD, params=params).json()
        self.vk_user_id = user_info['response'][0]['id']
        self.first_name = user_info['response'][0]['first_name']
        self.second_name = user_info['response'][0]['last_name']
        if len(user_info['response'][0]['bdate'].split('.')) < 3:
            #вызов функции бота для запроса года рождения
            self.birthday = f"{user_info['response'][0]['bdate']}.{#результат ранее вызванной функции}"
        else:
            self.birthday = user_info['response'][0]['bdate']
        self.sex = user_info['response'][0]['sex']
        self.city = user_info['response'][0]['city']['id']

    def search_compare_users(self):
        METHOD = 'users.search'
