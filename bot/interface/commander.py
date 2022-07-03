class Commander:

    # Команды

    def __init__(self):

        self.last_command = None
        self.search_options = {"Пол": None, "Мин. возраст": None, "Макс. возраст": None, "Счетчик": 1}
        # Для запоминания ответов пользователя
        self.last_ans = None

    def input(self, msg):
        """
        Функция принимающая сообщения пользователя
        :param msg: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """
        next_contender = "Следующий/ая"
        search_options = "Параметры поиска"
        favorites = "Добавить в избранное"
        black_list = "Добавить в черный список"

        self.last_ans = msg

        if self.last_command == search_options:
            if self.search_options["Пол"] is None:
                self.search_options["Пол"] = msg
                return "Введите минимальный возраст партнера: "
            if self.search_options["Мин. возраст"] is None:
                self.search_options["Мин. возраст"] = msg
                return "Введите максимальный возраст партнера: "
            if self.search_options["Макс. возраст"] is None:
                self.search_options["Макс. возраст"] = msg
                self.last_command = None
                return "Параметры поиска установлены!"

        # next
        if next_contender in msg:
            return next_contender

        # search options
        if search_options in msg:
            self.search_options = {"Пол": None, "Мин. возраст": None, "Макс. возраст": None, "Счетчик": 1}
            self.last_command = search_options
            return "Кого ищем: мужчину или женщину(м/ж): "

        # favorites
        if favorites in msg:
            return favorites

        # black list
        if black_list in msg:
            return black_list

        return "Команда не распознана!"
