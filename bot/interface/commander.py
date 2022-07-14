import os
import re
import json

from interface import commander_config
from Integration.api_vk import VKApiRequests
from db.insert_data import DataIn
from db.send_data import Parcel
from db.delete_data import Disposal


class Commander:

    def __init__(self, vk_id, user_name):

        self.id = vk_id
        self.user_name = user_name
        path_file = os.path.join("interface", "options", f"options_{self.id}.txt")
        if os.path.exists(path_file):
            self.reading_parameters()
            if self.token is not None:
                self.obj_vk_api_requests = VKApiRequests(self.id, self.token)
        else:
            self.token = None
            self.obj_vk_api_requests = None
            self.mode = "default"
            self.path = os.path.join("interface", "keyboards", "default.json")
            self.candidate = {}
            self.list_elected = []
            self.elected_id = None
            self.list_blacklist = []
            self.blacklist_id = None
            self.counter = 0

    def input(self, msg):
        """
        Функция принимающая сообщения пользователя
        :param msg: Сообщение от пользователя
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

        if self.mode == "photo_1" or self.mode == "photo_2" or self.mode == "photo_3":
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
            self.obj_vk_api_requests = VKApiRequests(self.id, self.token)
            return self.age_city_check()
        else:
            answer = f"Ошибка! Попробуйте еще раз!\n\n" + request_token
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

    def processing_mode_default(self, msg):
        start = commander_config.start
        request_token = commander_config.request_token
        if start in msg:
            self.mode = "token"
            answer = request_token
            self.path = os.path.join("interface", "keyboards", "none.json")
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result
        else:
            answer = f"Привет, {self.user_name}!\n" \
                     f"Для того чтобы начать поиск партнера нажмите 'Начать поиск'. Удачи, {self.user_name}!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

    def processing_mode_favorites(self, msg):

        next_contender = commander_config.next_contender
        remove = commander_config.remove
        continue_searching = commander_config.continue_searching

        if next_contender in msg:
            if self.list_elected == []:
                answer = f"{self.user_name}, это невозможно! Ваш список избранных кандидатов пуст!"
                self.elected_id = None
            else:
                if self.counter == (len(self.list_elected) - 1):
                    answer = f"{self.user_name}, больше избранных кандидатов нет!"
                else:
                    self.counter += 1
                    self.elected_id = self.list_elected[self.counter]
                    answer = f"https://vk.com/id{self.elected_id}"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if remove in msg:
            db = Disposal('db_dating', 'user_dating')
            db.del_id_electlist(user_id=self.id, del_user_id=self.elected_id)
            answer = f"Пользователь https://vk.com/id{self.elected_id} удален из списка избранных кандидатов!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            self.path = os.path.join("interface", "keyboards", "search.json")
            answer = self.candidate_data_output()
            result = {"message": answer["message"], "path": self.path, "attachment": answer["attachment"]}
            self.counter = 0
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

    def processing_mode_blacklist(self, msg):
        next_contender = commander_config.next_contender
        remove_blacklist = commander_config.remove_blacklist
        continue_searching = commander_config.continue_searching

        if next_contender in msg:
            if self.list_blacklist == []:
                answer = f"{self.user_name}, это невозможно! Ваш черный список пуст!"
                self.blacklist_id = None
            else:
                if self.counter == (len(self.list_blacklist) - 1):
                    answer = f"{self.user_name}, больше в черном списке никого нет!"
                else:
                    self.counter += 1
                    self.blacklist_id = self.list_blacklist[self.counter]
                    answer = f"https://vk.com/id{self.blacklist_id}"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if remove_blacklist in msg:
            db = Disposal('db_dating', 'user_dating')
            db.del_id_blacklist(user_id=self.id, del_user_id=self.blacklist_id)
            answer = f"Пользователь https://vk.com/id{self.blacklist_id} удален из черного списка!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            self.path = os.path.join("interface", "keyboards", "search.json")
            answer = self.candidate_data_output()
            result = {"message": answer["message"], "path": self.path, "attachment": answer["attachment"]}
            self.counter = 0
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = {"message": answer, "path": self.path, "attachment": None}
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
            self.obtaining_candidate()
            answer = self.candidate_data_output()
            result = {"message": answer["message"], "path": self.path, "attachment": answer["attachment"]}
            self.saving_parameters()
            return result

        if favorites in msg:
            db = DataIn("Script_Insert_SQL_table_data.sql", 'db_dating', 'user_dating')
            db.in_elected_table(user_bot=self.id, elected_user=self.candidate["id"])
            answer = f"{self.candidate['first_name']} {self.candidate['last_name']} внесен/а в список избранного"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if add_blacklist in msg:
            db = DataIn("Script_Insert_SQL_table_data.sql", 'db_dating', 'user_dating')
            db.in_blacklist_table(user_bot=self.id, blacklist_user=self.candidate["id"])
            answer = f"{self.candidate['first_name']} {self.candidate['last_name']} внесен/а в чёрный список " \
                     f"и больше не будет отображаться при поиске кандидатов!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if favorites_list in msg:
            db = Parcel('db_dating', 'user_dating')
            self.list_elected = db.elected_list_output(user_id=self.id)
            if self.list_elected == []:
                answer = f"{self.user_name}, Ваш список избранных кандидатов пуст!"
                self.elected_id = None
            else:
                self.counter = 0
                self.elected_id = self.list_elected[self.counter]
                answer = f"{self.user_name}, Ваш список избранных кандидатов:\n" \
                         f"https://vk.com/id{self.elected_id}"
                self.path = os.path.join("interface", "keyboards", "favorites.json")
                self.mode = "favorites"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if blacklist in msg:
            db = Parcel('db_dating', 'user_dating')
            self.list_blacklist = db.black_list_output(user_id=self.id)
            if self.list_blacklist == []:
                answer = f"{self.user_name}, Ваш черный список пуст!"
                self.blacklist_id = None
            else:
                self.counter = 0
                self.blacklist_id = self.list_blacklist[self.counter]
                answer = f"{self.user_name}, Ваш черный список:\n" \
                         f"https://vk.com/id{self.blacklist_id}"
                self.path = os.path.join("interface", "keyboards", "blacklist.json")
                self.mode = "blacklist"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if photo_1 in msg:
            result = self.choose_photo(photo="photo_1")
            return result

        if photo_2 in msg:
            result = self.choose_photo(photo="photo_2")
            return result

        if photo_3 in msg:
            result = self.choose_photo(photo="photo_3")
            return result

        else:
            answer = "Команда не распознана!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

    def processing_mode_photo(self, msg):

        like = commander_config.like
        revoke_like = commander_config.revoke_like
        continue_searching = commander_config.continue_searching

        if like in msg:
            photo_id = None
            if self.mode == "photo_1":
                photo_id = self.candidate['photo_1']['id_photo']
            elif self.mode == "photo_2":
                photo_id = self.candidate['photo_2']['id_photo']
            elif self.mode == "photo_3":
                photo_id = self.candidate['photo_3']['id_photo']
            if photo_id:
                answer = self.obj_vk_api_requests.smash_like(candidate_id=self.candidate['id'], photo_id=photo_id)
            else:
                answer = "Неизвестная ошибка: режим photo, команда: Поставить лайк"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if revoke_like in msg:
            photo_id = None
            if self.mode == "photo_1":
                photo_id = self.candidate['photo_1']['id_photo']
            elif self.mode == "photo_2":
                photo_id = self.candidate['photo_2']['id_photo']
            elif self.mode == "photo_3":
                photo_id = self.candidate['photo_3']['id_photo']
            if photo_id:
                answer = self.obj_vk_api_requests.delete_like(candidate_id=self.candidate['id'], photo_id=photo_id)
            else:
                answer = "Неизвестная ошибка: режим photo, команда: Убрать лайк"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            self.path = os.path.join("interface", "keyboards", "search.json")
            answer = self.candidate_data_output()
            result = {"message": answer["message"], "path": self.path, "attachment": answer["attachment"]}
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

    def age_city_check(self):
        if self.obj_vk_api_requests.is_city_age_exists() == 0:
            self.mode = "search"
            self.path = os.path.join("interface", "keyboards", "search.json")
            self.obtaining_candidate()
            answer = self.candidate_data_output()
            result = {"message": answer["message"], "path": self.path, "attachment": answer["attachment"]}
            self.saving_parameters()
            return result
        if self.obj_vk_api_requests.is_city_age_exists() == 1 or self.obj_vk_api_requests.is_city_age_exists() == 2:
            self.mode = "age"
            self.path = os.path.join("interface", "keyboards", "none.json")
            answer = f"{self.user_name}, пришлите Ваш возраст, в виде числа, в ответном сообщении."
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result
        elif self.obj_vk_api_requests.is_city_age_exists() == 3:
            self.mode = "city"
            self.path = os.path.join("interface", "keyboards", "none.json")
            answer = f"{self.user_name}, укажите название города, в котором Вы проживаете, в ответном сообщении."
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

    def processing_mode_age(self, msg):
        pattern_age = "[1-9][0-9]{0,2}"
        if re.search(pattern_age, msg):
            age = re.search(pattern_age, msg).group(0)
            if 0 < int(age) < 150:
                self.obj_vk_api_requests.give_me_city_age(age=age)
        return self.age_city_check()

    def processing_mode_city(self, msg):
        pattern_city = "[А-Я][а-я]+-*[А-Я]*[а-я]*[0-9]*"
        if re.search(pattern_city, msg):
            city = re.search(pattern_city, msg).group(0)
            self.obj_vk_api_requests.give_me_city_age(city_name=city)
        return self.age_city_check()

    def saving_parameters(self):
        path_options = os.path.join("interface", "options")
        if os.path.exists(path_options) is False:
            os.mkdir(path_options)
        path_file = os.path.join(path_options, f"options_{self.id}.txt")
        dict_options = {
            "self.token": self.token,
            "self.mode": self.mode,
            "self.path": self.path,
            "self.candidate": self.candidate,
            "self.list_elected": self.list_elected,
            "self.elected_id": self.elected_id,
            "self.counter": self.counter,
            "self.list_blacklist": self.list_blacklist,
            "self.blacklist_id": self.blacklist_id
        }
        with open(path_file, 'w', encoding='utf-8') as file:
            json.dump(dict_options, file)

    def reading_parameters(self):
        path_file = os.path.join("interface", "options", f"options_{self.id}.txt")
        with open(path_file, 'r', encoding='utf-8') as file:
            dict_options = json.load(file)
            self.token = dict_options["self.token"]
            self.mode = dict_options["self.mode"]
            self.path = dict_options["self.path"]
            self.candidate = dict_options["self.candidate"]
            self.list_elected = dict_options["self.list_elected"]
            self.elected_id = dict_options["self.elected_id"]
            self.counter = dict_options["self.counter"]
            self.list_blacklist = dict_options["self.list_blacklist"]
            self.blacklist_id = dict_options["self.blacklist_id"]

    def obtaining_candidate(self):
        dict_candidates = self.obj_vk_api_requests.give_me_candidates()
        dict_photo = dict_candidates[list(dict_candidates.keys())[0]]["photo_links"]
        dict_candidate = {
            "id": list(dict_candidates.keys())[0],
            "first_name": dict_candidates[list(dict_candidates.keys())[0]]["first_name"],
            "last_name": dict_candidates[list(dict_candidates.keys())[0]]["last_name"],
            "link_to_profile": f"https://vk.com/id{list(dict_candidates.keys())[0]}"
        }
        for count, photo_key in enumerate(dict_photo):
            dict_candidate[f"photo_{count + 1}"] = {
                "id_photo": photo_key,
                "link_photo": dict_photo[photo_key]
            }
        self.candidate = dict_candidate
        self.obj_vk_api_requests.save_session(self.candidate["id"])

    def candidate_data_output(self):
        message = f"{self.candidate['first_name']} {self.candidate['last_name']}\n{self.candidate['link_to_profile']}"
        owner_id = self.candidate['id']
        if self.candidate.get("photo_3"):
            photo_id_1 = self.candidate['photo_1']['id_photo']
            photo_id_2 = self.candidate['photo_2']['id_photo']
            photo_id_3 = self.candidate['photo_3']['id_photo']
            attachment = f"photo{owner_id}_{photo_id_1},photo{owner_id}_{photo_id_2},photo{owner_id}_{photo_id_3}"
            return {"message": message, "attachment": attachment}
        elif self.candidate.get("photo_2"):
            photo_id_1 = self.candidate['photo_1']['id_photo']
            photo_id_2 = self.candidate['photo_2']['id_photo']
            attachment = f"photo{owner_id}_{photo_id_1},photo{owner_id}_{photo_id_2}"
            message += "\nЕсть только две фотографии:"
            return {"message": message, "attachment": attachment}
        elif self.candidate.get("photo_1"):
            photo_id_1 = self.candidate['photo_1']['id_photo']
            attachment = f"photo{owner_id}_{photo_id_1}"
            message += "\nЕсть только одна фотография:"
            return {"message": message, "attachment": attachment}
        else:
            message += "\nФотографий нет!"
            return {"message": message, "attachment": None}

    def choose_photo(self, photo):
        if self.candidate.get(photo):
            self.mode = photo
            answer = "Выбранная фотография:\n"
            photo_id = self.candidate[photo]['id_photo']
            attachment = f"photo{self.candidate['id']}_{photo_id}"
            self.path = os.path.join("interface", "keyboards", "photo.json")
            result = {"message": answer, "path": self.path, "attachment": attachment}
        else:
            answer = f"У {self.candidate['first_name']} {self.candidate['last_name']} нет такой фотографии!"
            result = {"message": answer, "path": self.path, "attachment": None}
        self.saving_parameters()
        return result
