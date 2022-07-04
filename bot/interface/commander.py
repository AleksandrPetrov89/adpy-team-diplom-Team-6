import os


class Commander:

    # Команды

    def __init__(self):

        self.mode = "default"
        self.search_options = {"Пол": None, "Мин. возраст": None, "Макс. возраст": None, "Счетчик": 0}
        # Для запоминания ответов пользователя
        self.last_ans = None
        self.path = os.path.join("bot", "interface", "keyboards", "default.json")

    def input(self, msg):
        """
        Функция принимающая сообщения пользователя
        :param msg: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """
        next_contender = "Следующий/ая"
        search_options = "Изменить параметры поиска"
        favorites = "Добавить в избранное"
        black_list = "Добавить в черный список"
        favorites_list = "Список избранных"
        start = "Начать поиск"

        self.last_ans = msg

        if self.mode == "default":
            if start in msg:
                self.mode = "options"
                answer = "Введите параметры поиска.\nКого ищем: мужчину или женщину(м/ж): "
                self.path = os.path.join("bot", "interface", "keyboards", "options.json")
                result = [answer, self.path]
                return result
            else:
                answer = "Привет!\nДля того чтобы начать поиск партнера нажмите 'Начать поиск'. Удачи!"
                result = [answer, self.path]
                return result

        if self.mode == "favorites":
            pass

        if self.mode == "options":
            if self.search_options["Пол"] is None:
                self.search_options["Пол"] = msg
                answer = "Введите минимальный возраст партнера: "
                result = [answer, self.path]
                return result
            if self.search_options["Мин. возраст"] is None:
                self.search_options["Мин. возраст"] = msg
                answer = "Введите максимальный возраст партнера: "
                result = [answer, self.path]
                return result
            if self.search_options["Макс. возраст"] is None:
                self.search_options["Макс. возраст"] = msg
                self.mode = "search"
                self.path = os.path.join("bot", "interface", "keyboards", "search.json")
                answer = "Параметры поиска установлены!"
                result = [answer, self.path]
                return result

        if self.mode == "search":

            if next_contender in msg:
                answer = next_contender
                result = [answer, self.path]
                return result

            if search_options in msg:
                self.search_options = {"Пол": None, "Мин. возраст": None, "Макс. возраст": None, "Счетчик": 0}
                self.mode = "options"
                answer = "Введите параметры поиска.\nКого ищем: мужчину или женщину(м/ж): "
                self.path = os.path.join("bot", "interface", "keyboards", "options.json")
                result = [answer, self.path]
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
                answer = favorites_list
                result = [answer, self.path]
                return result

            else:
                answer = "Команда не распознана!"
                result = [answer, self.path]
                return result
