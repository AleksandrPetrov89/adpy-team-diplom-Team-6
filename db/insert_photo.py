import sqlalchemy
from create_table import TableDb

#
class Photo:
    """

    """
    # Функция инициализации класса Photo
    def __init__(self, data_base, user):
        self.data_base = data_base
        self.user = user


    # Функция получения фото в виде словаря.
    def get_photo(self, user_id=987654321, photo_link='https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos555666777', photo_id=457239018):
        """
        :return: dict_photo
        """
        dict_photo = {
                    user_id : [photo_link, photo_id ]
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
            link = value[0]
            for symbol in link:
                if symbol == '%':
                    new_symbol = symbol.replace('%', '%%')
                    new_photo_link += new_symbol
                else:
                    new_photo_link += symbol
            new_dict_photo[key] = [new_photo_link, value[1]]
        return new_dict_photo

    # Функция заносит данные по фотографиям в таблицу photo_list.
    def in_photolist_table(self):
        """
        Функция внесения в БД данных о фотографиях: ссылка, ID фотографии, ID пользователя.
        :return: insert_photo_result
        """
        dict_obj = Photo(self.data_base, self.user)
        dict_photo = dict_obj.search_link_symbol()
        TableDb_obj = TableDb(self.data_base, self.user)
        connect = TableDb_obj.db_connect()
        for key, value in dict_photo.items():
            req_sql = f"INSERT INTO photo_list(photo_link, photo_id, user_data_user_id) VALUES('{value[0]}'," \
                      f" {value[1]}, {key});"
            insert_photo_result = connect.execute(req_sql)
        return insert_photo_result

    # Функция получения фото c "лайком" в виде словаря.
    def get_likes_photo(self, user_id=123456789, photo_id=5):
        """
        :return: dict_likes_photo
        """
        dict_likes_photo = {
                    user_id : photo_id
        }
        return dict_likes_photo

    # Функция заносит данные по "лайкнутым" фотографиям в таблицу likes_list.
    def in_likeslist_table(self):
        """
        Функция внесения в БД данных о фотографиях, на которые поставили "лайк": ID фотографии, ID пользователя.
        :return: insert_photo_result
        """
        dict_obj = Photo(self.data_base, self.user)
        dict_photo = dict_obj.get_likes_photo()
        TableDb_obj = TableDb(self.data_base, self.user)
        connect = TableDb_obj.db_connect()
        for key, value in dict_photo.items():
            req_sql = f"INSERT INTO likes_list(user_data_id, photo_list_id) VALUES({key}, {value});"
            insert_photo_result = connect.execute(req_sql)
        return insert_photo_result

if __name__ == '__main__':
    # Photo.search_link_symbol(Photo('db_dating', 'user_dating'))
    # Photo.in_photolist_table(Photo('db_dating', 'user_dating'))
    Photo.in_likeslist_table(Photo('db_dating', 'user_dating'))
