import vk_api
from . import keys
import os

LOGIN = keys.login
PASSWORD = keys.password
ALBUM_ID = 268084247
GROUP_ID = 188016300


def delivery_graphics(filenames):
    # 1-Логинимся как пользователь в вк
    # 2-Загружаем список файлов на сервере вк
    # 3-При успешной загружке удаляем графики на нашем сервере
    # 4-Формируем список ссылок на загруженные файлы из json,
    # полученном на 2 шагe

    vk_session = vk_api.VkApi(LOGIN, PASSWORD)  # 1

    try:
        vk_session.auth(token_only=True)

    except vk_api.AuthError as error_msg:
        print(error_msg)

    upload = vk_api.VkUpload(vk_session)
    grafics = [i + ".png" for i in filenames]
    uploaded = upload.photo(grafics, album_id=ALBUM_ID, group_id=GROUP_ID)  # 2

    uploaded_url = [
        "photo{}_{}".format(
            uploaded[uploaded.index(i)]["owner_id"],
            uploaded[uploaded.index(i)]["id"],
        )
        for i in uploaded
    ]  # 4

    if uploaded_url:
        for i in grafics:
            os.remove(i)  # 3

    return uploaded_url


def clean_album(file):
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)

    try:
        vk_session.auth(token_only=True)

    except vk_api.AuthError as error_msg:
        print(error_msg)

    vk = vk_session.get_api()

    try:
        vk.photos.delete(owner_id=-GROUP_ID, photo_id=file)

    except:
        pass
