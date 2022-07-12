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
            self.path = os.path.join("interface", "keyboards", "default.json")
            self.candidate = {}

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
            answer = next_contender
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if remove in msg:
            answer = remove
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("interface", "keyboards", "search.json")
            result = {"message": answer, "path": self.path, "attachment": None}
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
            answer = next_contender
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if remove_blacklist in msg:
            answer = remove_blacklist
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("interface", "keyboards", "search.json")
            result = {"message": answer, "path": self.path, "attachment": None}
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
            answer = favorites
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if add_blacklist in msg:
            answer = add_blacklist
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if favorites_list in msg:
            self.mode = "favorites"
            answer = favorites_list
            self.path = os.path.join("interface", "keyboards", "favorites.json")
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if blacklist in msg:
            self.mode = "blacklist"
            answer = blacklist
            self.path = os.path.join("interface", "keyboards", "blacklist.json")
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if photo_1 in msg:
            self.mode = "photo"
            answer = photo_1
            self.path = os.path.join("interface", "keyboards", "photo.json")
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if photo_2 in msg:
            self.mode = "photo"
            answer = photo_2
            self.path = os.path.join("interface", "keyboards", "photo.json")
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if photo_3 in msg:
            self.mode = "photo"
            answer = photo_3
            self.path = os.path.join("interface", "keyboards", "photo.json")
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
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
            answer = like
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if revoke_like in msg:
            answer = revoke_like
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        if continue_searching in msg:
            self.mode = "search"
            answer = continue_searching
            self.path = os.path.join("interface", "keyboards", "search.json")
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

        else:
            answer = "Команда не распознана!"
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result

    def age_city_check(self):
        if self.bot_user.is_city_age_exists() == 0:
            self.mode = "search"
            self.path = os.path.join("interface", "keyboards", "search.json")
            self.obtaining_candidate()
            answer = self.candidate_data_output()
            result = {"message": answer["message"], "path": self.path, "attachment": answer["attachment"]}
            self.saving_parameters()
            return result
        if self.bot_user.is_city_age_exists() == 1 or self.bot_user.is_city_age_exists() == 2:
            self.mode = "age"
            self.path = os.path.join("interface", "keyboards", "none.json")
            answer = f"{self.user_name}, пришлите Ваш возраст, в виде числа, в ответном сообщении."
            result = {"message": answer, "path": self.path, "attachment": None}
            self.saving_parameters()
            return result
        elif self.bot_user.is_city_age_exists() == 3:
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
            "self.path": self.path,
            "self.candidate": self.candidate
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

    def obtaining_candidate(self):
        dict_candidates = self.bot_user.give_me_candidates()
        dict_candidate = {
            "id": list(dict_candidates.keys())[0],
            "first_name": dict_candidates[list(dict_candidates.keys())[0]]["first_name"],
            "last_name": dict_candidates[list(dict_candidates.keys())[0]]["last_name"],
            "link_to_profile": f"https://vk.com/id{list(dict_candidates.keys())[0]}",
            "photo_1": {"id_photo": list(dict_candidates[list(dict_candidates.keys())[0]]["photo_links"].keys())[0],
                        "link_photo": dict_candidates[list(dict_candidates.keys())[0]]["photo_links"]
                        [list(dict_candidates[list(dict_candidates.keys())[0]]["photo_links"].keys())[0]]},
            "photo_2": {"id_photo": list(dict_candidates[list(dict_candidates.keys())[0]]["photo_links"].keys())[1],
                        "link_photo": dict_candidates[list(dict_candidates.keys())[0]]["photo_links"]
                        [list(dict_candidates[list(dict_candidates.keys())[0]]["photo_links"].keys())[1]]},
            "photo_3": {"id_photo": list(dict_candidates[list(dict_candidates.keys())[0]]["photo_links"].keys())[2],
                        "link_photo": dict_candidates[list(dict_candidates.keys())[0]]["photo_links"]
                        [list(dict_candidates[list(dict_candidates.keys())[0]]["photo_links"].keys())[2]]}
        }
        self.candidate = dict_candidate
        self.bot_user.save_session(self.candidate["id"])

    def candidate_data_output(self):
        message = f"{self.candidate['first_name']} {self.candidate['last_name']}\n{self.candidate['link_to_profile']}"
        owner_id = self.candidate['id']
        photo_id_1 = self.candidate['photo_1']['id_photo']
        photo_id_2 = self.candidate['photo_2']['id_photo']
        photo_id_3 = self.candidate['photo_3']['id_photo']
        attachment = f"photo{owner_id}_{photo_id_1},photo{owner_id}_{photo_id_2},photo{owner_id}_{photo_id_3}"
        return {"message": message, "attachment": attachment}
