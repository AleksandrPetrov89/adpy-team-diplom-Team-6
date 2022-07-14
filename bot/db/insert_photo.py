from db.create_table import TableDb


#
class Photo:
    """

    """

    # Функция инициализации класса Photo
    def __init__(self, data_base, user):
        self.data_base = data_base
        self.user = user

    # Функция поиска спецсимвола % в ссылках и замена на %%, в противном случае данные не записываются в таблицы БД.
    def search_link_symbol(self, bot_user_user_id, user_id, photo_link, photo_id):
        """
        :return: new_photo_link
        """
        dict_photo = {
            bot_user_user_id: [user_id, photo_link, photo_id]
        }

        new_photo_link = ''
        new_dict_photo = {}

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
            # Проверка наличия пользователей в таблице user_data.
            req_check_user_bot = f'SELECT user_id FROM user_data WHERE user_id={key};'
            is_exist_user_bot = connect.execute(req_check_user_bot).fetchall()
            if is_exist_user_bot == []:
                connect.execute(f'INSERT INTO user_data(user_id) VALUES({key});')
            req_check_elect_user = f'SELECT user_id FROM user_data WHERE user_id={value[0]};'
            is_exist_elect_user = connect.execute(req_check_elect_user).fetchall()
            if is_exist_elect_user == []:
                connect.execute(f'INSERT INTO user_data(user_id) VALUES({value[0]});')
            # Внесение данных о пользователях в таблицу photo_list.
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
    def in_likeslist_table(self, bot_user_user_id, user_id, photo_link, photo_id):
        """
        Функция внесения в БД данных о фотографиях, на которые поставили "лайк": ID пользователя, который поставил лайк,
        а также ID фотографии, которая понравилась.
        :return: insert_status
        """
        id_list = []
        check_insert_list = []
        dict_photo = {
            bot_user_user_id: [user_id, photo_link, photo_id]
        }
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
                    # Проверка внесения данных о лайкнутых фото в таблицу likes_list базы данных.
                    req_check_ll_insert = f'SELECT bot_user_user_id FROM likes_list WHERE ' \
                                          f'bot_user_user_id={key} AND photo_list_id={id_value};'
                    list_check_ll_insert = connect.execute(req_check_ll_insert).fetchall()
                    check_insert_list.append(list_check_ll_insert)
        if check_insert_list == []:
            insert_status = False
        return insert_status


# if __name__ == '__main__':
    # Photo.search_link_symbol(Photo('db_dating', 'user_dating'))
    # Photo.in_photolist_table(Photo('db_dating', 'user_dating'))
    # Photo.in_likeslist_table(Photo('db_dating', 'user_dating'))
