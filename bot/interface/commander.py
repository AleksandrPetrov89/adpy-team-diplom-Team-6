import os


class Commander:

    def __init__(self):

        self.mode = "default"
        self.search_options = {"Пол": None, "Мин. возраст": None, "Макс. возраст": None, "Счетчик": 0}
        # Для запоминания ответов пользователя
        self.last_ans = None
        self.result = None
        self.path = os.path.join("bot", "interface", "keyboards", "default.json")

    def input(self, msg):
        """
        Функция принимающая сообщения пользователя
        :param msg: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """
        next_contender = "Следующий/ая"
        favorites = "Добавить в избранное"
        black_list = "Добавить в черный список"
        favorites_list = "Список избранных"
        continue_searching = "Продолжить поиск"
        remove = "Удалить из избранного"
        start = "Начать поиск"
        photo_1, photo_2, photo_3 = "Фото 1", "Фото 2", "Фото 3"
        like = "Поставить лайк"
        revoke_like = "Убрать лайк"

        self.last_ans = msg

        if self.mode == "default":
            if start in msg:
                self.mode = "search"
                answer = "search"
                self.path = os.path.join("bot", "interface", "keyboards", "search.json")
                result = [answer, self.path]
                return result
            else:
                answer = "Привет!\nДля того чтобы начать поиск партнера нажмите 'Начать поиск'. Удачи!"
                result = [answer, self.path]
                return result

        if self.mode == "favorites":

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

        if self.mode == "search":

            if next_contender in msg:
                answer = next_contender
                result = [answer, self.path]
                self.result = result
                return result

            if favorites in msg:
                answer = favorites
                result = [answer, self.path]
                return result

            if black_list in msg:
                answer = black_list
                result = [answer, self.path]
                return result

            if favorites_list in msg:
                self.mode = "favorites"
                answer = favorites_list
                self.path = os.path.join("bot", "interface", "keyboards", "favorites.json")
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

        if self.mode == "photo":

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
