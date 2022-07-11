import os
import re
import json

from interface import commander_config
from Integration.api_vk import VKApiRequests


class Commander:

    def __init__(self, vk_id, user_name):

        self.id = vk_id
        self.user_name = user_name
        path_file = os.path.join("interface", "options", f"options_{self.id}.txt")
        if os.path.exists(path_file):
            self.reading_parameters()
            if self.token is not None:
                self.bot_user = VKApiRequests(self.id, self.token)
        else:
            self.token = None
            self.bot_user = None
            self.mode = "default"
            self.last_ans = None
            self.result = None
            self.path = os.path.join("interface", "keyboards", "default.json")

    def input(self, msg):
        """
        Функция принимающая сообщения пользователя
        :param msg: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """

        if self.mode == "default":
            return self.processing_mode_default(msg)

        if self.mode == "token":
            return self.processing_mode_token(msg)

        if self.mode == "favorites":
            return self.processing_mode_favorites(msg)

        if self.mode == "blacklist":
            return self.processing_mode_blacklist(msg)

        if self.mode == "search":
            return self.processing_mode_search(msg)

        if self.mode == "photo":
            return self.processing_mode_photo(msg)

        if self.mode == "age":
            return self.processing_mode_age(msg)

        if self.mode == "city":
            return self.processing_mode_city(msg)

    def processing_mode_token(self, msg):

        request_token = commander_config.request_token
        pattern = "access_token=([^&]*)"
        if re.search(pattern, msg):
            self.token = re.search(pattern, msg).group(1)
            self.bot_user = VKApiRequests(self.id, self.token)
            return self.age_city_check()
        else:
            answer = f"Ошибка! Попробуйте еще раз!\n\n" + request_token
            result = [answer, self.path]
            self.saving_parameters()
            return result

    def processing_mode_default(self, msg):
        start = commander_config.start
        request_token = commander_config.request_token
        if start in msg:
            self.mode = "token"
            answer = request_token
            self.path = os.path.join("interface", "keyboards", "none.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result
        else:
            answer = f"Привет, {self.user_name}!\n" \
                     f"Для того чтобы начать поиск партнера нажмите 'Начать поиск'. Удачи, {self.user_name}!"
            result = [answer, self.path]
            self.saving_parameters()
            return result

    def processing_mode_favorites(self, msg):

        next_contender = commander_config.next_contender
        remove = commander_config.remove
        continue_searching = commander_config.continue_searching

        if next_contender in msg:
            answer = next_contender
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if remove in msg:
            answer = remove
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("interface", "keyboards", "search.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
            self.saving_parameters()
            return result

    def processing_mode_blacklist(self, msg):
        next_contender = commander_config.next_contender
        remove_blacklist = commander_config.remove_blacklist
        continue_searching = commander_config.continue_searching

        if next_contender in msg:
            answer = next_contender
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if remove_blacklist in msg:
            answer = remove_blacklist
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("interface", "keyboards", "search.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
            self.saving_parameters()
            return result

    def processing_mode_search(self, msg):

        next_contender = commander_config.next_contender
        favorites = commander_config.favorites
        add_blacklist = commander_config.add_blacklist
        favorites_list = commander_config.favorites_list
        blacklist = commander_config.blacklist
        photo_1 = commander_config.photo_1
        photo_2 = commander_config.photo_2
        photo_3 = commander_config.photo_3

        if next_contender in msg:
            answer = next_contender
            result = [answer, self.path]
            self.result = result
            self.saving_parameters()
            return result

        if favorites in msg:
            answer = favorites
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if add_blacklist in msg:
            answer = add_blacklist
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if favorites_list in msg:
            self.mode = "favorites"
            answer = favorites_list
            self.path = os.path.join("interface", "keyboards", "favorites.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if blacklist in msg:
            self.mode = "blacklist"
            answer = blacklist
            self.path = os.path.join("interface", "keyboards", "blacklist.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if photo_1 in msg:
            self.mode = "photo"
            answer = photo_1
            self.path = os.path.join("interface", "keyboards", "photo.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if photo_2 in msg:
            self.mode = "photo"
            answer = photo_2
            self.path = os.path.join("interface", "keyboards", "photo.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if photo_3 in msg:
            self.mode = "photo"
            answer = photo_3
            self.path = os.path.join("interface", "keyboards", "photo.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
            self.saving_parameters()
            return result

    def processing_mode_photo(self, msg):

        like = commander_config.like
        revoke_like = commander_config.revoke_like
        continue_searching = commander_config.continue_searching

        if like in msg:
            answer = like
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if revoke_like in msg:
            answer = revoke_like
            result = [answer, self.path]
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("interface", "keyboards", "search.json")
            result = [answer, self.path]
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
            self.saving_parameters()
            return result

    def age_city_check(self):
        if self.bot_user.is_city_age_exists() == 0:
            self.mode = "search"
            self.path = os.path.join("interface", "keyboards", "search.json")

            answer = "Все данные полученны"
            result = [answer, self.path]
            self.saving_parameters()
            return result
        if self.bot_user.is_city_age_exists() == 1 or self.bot_user.is_city_age_exists() == 2:
            self.mode = "age"
            self.path = os.path.join("interface", "keyboards", "none.json")
            answer = f"{self.user_name}, пришлите Ваш возраст, в виде числа, в ответном сообщении."
            result = [answer, self.path]
            self.saving_parameters()
            return result
        elif self.bot_user.is_city_age_exists() == 3:
            self.mode = "city"
            self.path = os.path.join("interface", "keyboards", "none.json")
            answer = f"{self.user_name}, укажите название города, в котором Вы проживаете, в ответном сообщении."
            result = [answer, self.path]
            self.saving_parameters()
            return result

    def processing_mode_age(self, msg):
        pattern_age = "[1-9][0-9]{0,2}"
        if re.search(pattern_age, msg):
            age = re.search(pattern_age, msg).group(0)
            if 0 < int(age) < 150:
                self.bot_user.give_me_city_age(age=age)
        return self.age_city_check()

    def processing_mode_city(self, msg):
        pattern_city = "[А-Я][а-я]+-*[А-Я]*[а-я]*[0-9]*"
        if re.search(pattern_city, msg):
            city = re.search(pattern_city, msg).group(0)
            self.bot_user.give_me_city_age(city_name=city)
        return self.age_city_check()

    def saving_parameters(self):
        path_options = os.path.join("interface", "options")
        if os.path.exists(path_options) is False:
            os.mkdir(path_options)
        path_file = os.path.join(path_options, f"options_{self.id}.txt")
        dict_options = {
            "self.token": self.token,
            "self.mode": self.mode,
            "self.last_ans": self.last_ans,
            "self.result": self.result,
            "self.path": self.path
        }
        with open(path_file, 'w', encoding='utf-8') as file:
            json.dump(dict_options, file)

    def reading_parameters(self):
        path_file = os.path.join("interface", "options", f"options_{self.id}.txt")
        with open(path_file, 'r', encoding='utf-8') as file:
            dict_options = json.load(file)
            self.token = dict_options["self.token"]
            self.mode = dict_options["self.mode"]
            self.last_ans = dict_options["self.last_ans"]
            self.result = dict_options["self.result"]
            self.path = dict_options["self.path"]
