from db.create_table import TableDb


#
class Photo:
    """

    """

    # Функция инициализации класса Photo
    def __init__(self, data_base, user):
        self.data_base = data_base
        self.user = user

    # Функция получения фото в виде словаря.
    def get_photo(self, bot_user_user_id=123456789, user_id=987654321,
                  photo_link='https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos555666777',
                  photo_id=111111111):
        """
        Функция get_photo принимает на вход 4 параметра. bot_user_user_id - это id пользователя, который общается с
        ботом и выбирает кандидатов. user_id - это id пользователя, которого выбрали, ссылка на фото и id фото которого
        передаются в функцию, как 3-й и 4-й параметры.
        :return: dict_photo
        """
        dict_photo = {
            bot_user_user_id: [user_id, photo_link, photo_id]
        }
        return dict_photo

    # Функция поиска спецсимвола % в ссылках и замена на %%, в противном случае данные не записываются в таблицы БД.
    def search_link_symbol(self):
        """
        :return: new_photo_link
        """
        new_photo_link = ''
        new_dict_photo = {}
        photo_obj = Photo(self.data_base, self.user)
        dict_photo = photo_obj.get_photo()
        for key, value in dict_photo.items():
            link = value[1]
            for symbol in link:
                if symbol == '%':
                    new_symbol = symbol.replace('%', '%%')
                    new_photo_link += new_symbol
                else:
                    new_photo_link += symbol
            new_dict_photo[key] = [value[0], new_photo_link, value[2]]
        return new_dict_photo

    # Функция заносит данные по фотографиям в таблицу photo_list.
    def in_photolist_table(self):
        """
        Функция внесения в БД данных о фотографиях: ссылка, ID фотографии, ID пользователя. Если такие данные уже есть
         в таблице, то ничего не заносится. Возвращается результат выполнения insert_status. Если запись сделана, то
         True, если нет, то False.
        :return: insert_status
        """
        dict_obj = Photo(self.data_base, self.user)
        dict_photo = dict_obj.search_link_symbol()
        table_db_obj = TableDb(self.data_base, self.user)
        connect = table_db_obj.db_connect()
        insert_status = True
        for key, value in dict_photo.items():
            req_sql = f"INSERT INTO photo_list(photo_link, photo_id, user_data_user_id) VALUES('{value[1]}'," \
                      f" {value[2]}, {value[0]});"
            req_check_sql = f'SELECT user_data_user_id, photo_id FROM photo_list' \
                            f' WHERE user_data_user_id={value[0]} AND photo_id={value[2]};'
            is_exist = connect.execute(req_check_sql).fetchall()
            if is_exist != []:
                insert_status = False
            else:
                connect.execute(req_sql)
        return insert_status

    # Функция заносит данные по "лайкнутым" фотографиям в таблицу likes_list.
    def in_likeslist_table(self):
        """
        Функция внесения в БД данных о фотографиях, на которые поставили "лайк": ID пользователя, который поставил лайк,
        а также ID фотографии, которая понравилась.
        :return: insert_status
        """
        id_list = []
        dict_obj = Photo(self.data_base, self.user)
        dict_photo = dict_obj.get_photo()
        table_db_obj = TableDb(self.data_base, self.user)
        connect = table_db_obj.db_connect()
        insert_status = True
        for key, value in dict_photo.items():
            req_search_id = f'SELECT id FROM photo_list WHERE photo_id={value[2]};'
            list_photo_list_id = connect.execute(req_search_id).fetchall()
            for item in list_photo_list_id:
                for id_value in item:
                    id_list.append(id_value)
                    req_sql = f"INSERT INTO likes_list(bot_user_user_id, photo_list_id) VALUES({key}, {id_value});"
                    connect.execute(req_sql)
        return insert_status


if __name__ == '__main__':
    # Photo.search_link_symbol(Photo('db_dating', 'user_dating'))
    # Photo.in_photolist_table(Photo('db_dating', 'user_dating'))
    Photo.in_likeslist_table(Photo('db_dating', 'user_dating'))
