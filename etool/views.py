import vk_api
from rest_framework.views import APIView
from . models import User, Paymount
from . import keyboards
from . import keys
from . import vk_upload
from . helps import help_message
from vk_api.utils import get_random_id
import json
from django.http import HttpResponse


def router(payload=None, user_id=None, vk=None):
    # в зависимости от нажатй клавиши меню
    # передаем запрос соответсвующей функции
    payload = json.loads(payload)
    user = User.objects.get(user_id=user_id)

    if "next" in payload:
        next = payload["next"]
        vk.messages.send(peer_id=str(user_id),
                         random_id=get_random_id(),
                         keyboard=getattr(keyboards, next)(),
                         message='Выберите действие')

    elif "action" in payload:
        action = payload["action"]
        inc = payload["inc"]

        if action == "spending":
            vk.messages.send(peer_id=str(user_id),
                             random_id=get_random_id(),
                             keyboard=keyboards.nav_menu(back="category_menu"),
                             message='Введите сумму платежа')
            user.update_status(inc)

        elif action == "complete":
            vk.messages.send(peer_id=str(user_id),
                             random_id=get_random_id(),
                             keyboard=keyboards.general_menu(),
                             message='Успешно сохранено.')

        elif action == "roll_back":
            user.roll_back()
            vk.messages.send(peer_id=str(user_id),
                             random_id=get_random_id(),
                             keyboard=keyboards.general_menu(),
                             message='Успешно отменено.')

        elif action == "history":
            messages = user.history_callback(inc)
            for every in messages:
                vk.messages.send(peer_id=str(user_id),
                                 random_id=get_random_id(),
                                 keyboard=keyboards.nav_menu(back="history_menu"),
                                 message=every)

        elif action == "statistics":
            files = user.statistics_callback(inc)

            for file in files:
                if 'filename' in files[0]:
                    upload = vk_upload.delivery_graphics([file['filename']])
                    vk.messages.send(peer_id=str(user_id),
                                     random_id=get_random_id(),
                                     keyboard=keyboards.nav_menu(back="statistics_menu"),
                                     attachment = upload,
                                     message='{}'.format(file['message']))
                else:
                    vk.messages.send(peer_id=str(user_id),
                                     random_id=get_random_id(),
                                     keyboard=keyboards.nav_menu(back="statistics_menu"),
                                     message='{}'.format(file['message']))
                    break

        elif action == "help":
            vk.messages.send(peer_id=str(user_id),
                             random_id=get_random_id(),
                             keyboard=keyboards.nav_menu(back="general_menu"),
                             message=help_message)


class EntryPointView(APIView):
    def post(self, request, format=None):
        # обработка входящего пост запроса
        data = request.data

        if data['type'] == 'confirmation':
            # внутренняя проверка вк
            return HttpResponse(keys.confirmation_token)

        elif data['type'] == 'message_new':
            # обработка входящего сообщения
            vk_session = vk_api.VkApi(token=keys.token)
            vk = vk_session.get_api()
            user_message = data['object']['text']
            user_id = data['object']['from_id']
            user = None

            try:
                user = User.objects.get(user_id=user_id)
            except:
                pass

            if user_message == "Начать":
                if user:
                    vk.messages.send(peer_id=str(user_id),
                                     random_id=get_random_id(),
                                     keyboard=keyboards.general_menu(),
                                     message='Выберите действие')
                else:
                    User.objects.create(user_id=user_id)
                    vk.messages.send(peer_id=str(user_id),
                                     random_id=get_random_id(),
                                     keyboard=keyboards.general_menu(),
                                     message=('Спасибо за регистрацию.'
                                              'Выберите действие'))

            elif 'payload' in data['object']:
                router(payload=data['object']['payload'],
                       user_id=user_id, vk=vk)

            elif user_message.isdigit():
                if user:
                    if user.status:
                        paymount = Paymount.objects.create(user=user,
                                                           amount=int(user_message),
                                                           category=user.status)
                        user.update_active()
                        vk.messages.send(peer_id=str(user_id),
                                         random_id=get_random_id(),
                                         keyboard=keyboards.complete_menu(),
                                         message='Категория платежа {},сумма {} руб.'.format(paymount.get_category_display(),
                                                                                             user_message))
                        user.status = None
                        user.save()
                    else:
                        vk.messages.send(peer_id=str(user_id),
                                         random_id=get_random_id(),
                                         keyboard=keyboards.general_menu(),
                                         message=('Вы не выбрали '
                                                  'назначение платежа'))
                else:
                    vk.messages.send(peer_id=str(user_id),
                                     random_id=get_random_id(),
                                     message=('Вы не зарегистрированы.'
                                              'Нажмите/напишите "Начать"'))

            else:
                if user:
                    vk.messages.send(peer_id=str(user_id),
                                     random_id=get_random_id(),
                                     keyboard=keyboards.general_menu(),
                                     message="Неверный ввод.Выберите действие")
                else:
                    vk.messages.send(peer_id=str(user_id),
                                     random_id=get_random_id(),
                                     message=('Вы не зарегистрированы. '
                                              'Нажмите/напишите "Начать"'))

        return HttpResponse('ok')
