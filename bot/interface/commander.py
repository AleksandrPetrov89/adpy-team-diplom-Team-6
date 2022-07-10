import os
import re

from interface import commander_config


class Commander:
    def __init__(self, vk_id, user_name):

        self.id = vk_id
        self.token = None
        self.user_name = user_name
        self.mode = "default"
        self.search_options = {"Пол": None, "Мин. возраст": None, "Макс. возраст": None, "Счетчик": 0}
        self.last_ans = None
        self.result = None
        self.path = os.path.join("bot", "interface", "keyboards", "default.json")

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

    def processing_mode_token(self, msg):

        request_token = commander_config.request_token

        pattern = "access_token=([^&]*)"
        if re.search(pattern, msg):
            self.token = re.search(pattern, msg).group(1)
            self.mode = "search"
            self.path = os.path.join("bot", "interface", "keyboards", "search.json")
            answer = self.token
            result = [answer, self.path]
            return result
        else:
            answer = f"Ошибка! Попробуйте еще раз!\n\n" + request_token
            result = [answer, self.path]
            return result

    def processing_mode_default(self, msg):
        start = commander_config.start
        request_token = commander_config.request_token
        if start in msg:
            self.mode = "token"
            answer = request_token
            self.path = os.path.join("bot", "interface", "keyboards", "none.json")
            result = [answer, self.path]
            return result
        else:
            answer = f"Привет, {self.user_name}!\n" \
                     f"Для того чтобы начать поиск партнера нажмите 'Начать поиск'. Удачи, {self.user_name}!"
            result = [answer, self.path]
            return result

    def processing_mode_favorites(self, msg):

        next_contender = commander_config.next_contender
        remove = commander_config.remove
        continue_searching = commander_config.continue_searching

        if next_contender in msg:
            answer = next_contender
            result = [answer, self.path]
            return result

        if remove in msg:
            answer = remove
            result = [answer, self.path]
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("bot", "interface", "keyboards", "search.json")
            result = [answer, self.path]
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
            return result

    def processing_mode_blacklist(self, msg):
        next_contender = commander_config.next_contender
        remove_blacklist = commander_config.remove_blacklist
        continue_searching = commander_config.continue_searching

        if next_contender in msg:
            answer = next_contender
            result = [answer, self.path]
            return result

        if remove_blacklist in msg:
            answer = remove_blacklist
            result = [answer, self.path]
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("bot", "interface", "keyboards", "search.json")
            result = [answer, self.path]
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
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
            return result

        if favorites in msg:
            answer = favorites
            result = [answer, self.path]
            return result

        if add_blacklist in msg:
            answer = add_blacklist
            result = [answer, self.path]
            return result

        if favorites_list in msg:
            self.mode = "favorites"
            answer = favorites_list
            self.path = os.path.join("bot", "interface", "keyboards", "favorites.json")
            result = [answer, self.path]
            return result

        if blacklist in msg:
            self.mode = "blacklist"
            answer = blacklist
            self.path = os.path.join("bot", "interface", "keyboards", "blacklist.json")
            result = [answer, self.path]
            return result

        if photo_1 in msg:
            self.mode = "photo"
            answer = photo_1
            self.path = os.path.join("bot", "interface", "keyboards", "photo.json")
            result = [answer, self.path]
            return result

        if photo_2 in msg:
            self.mode = "photo"
            answer = photo_2
            self.path = os.path.join("bot", "interface", "keyboards", "photo.json")
            result = [answer, self.path]
            return result

        if photo_3 in msg:
            self.mode = "photo"
            answer = photo_3
            self.path = os.path.join("bot", "interface", "keyboards", "photo.json")
            result = [answer, self.path]
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
            return result

    def processing_mode_photo(self, msg):

        like = commander_config.like
        revoke_like = commander_config.revoke_like
        continue_searching = commander_config.continue_searching

        if like in msg:
            answer = like
            result = [answer, self.path]
            return result

        if revoke_like in msg:
            answer = revoke_like
            result = [answer, self.path]
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("bot", "interface", "keyboards", "search.json")
            result = [answer, self.path]
            return result

        else:
            answer = "Команда не распознана!"
            result = [answer, self.path]
            return result
