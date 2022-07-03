from interface import config
from interface.server import Server


if __name__ == "__main__":
    dating = Server(api_token=config.vk_api_token, group_id=config.vk_group_id)
    dating.start()
