from django.db import models
import pendulum
from .gf import Round, Wall

# Create your models here.


class Paymount(models.Model):

    FOOD = "FOOD"
    DRESS = "DRESS"
    FOR_HOME = "FOR_HOME"
    AUTO = "AUTO"
    TRANSPORT = "TRANSPORT"
    H_SERVICE = "H_SERVICE"
    ENTERTAIMENT = "ENTERTAIMENT"
    PRESENT = "PRESENT"
    SERVICE = "SERVICE"
    CREDIT = "CREDIT"
    ACCUM = "ACCUM"
    OTHER = "OTHER"

    CATEGORY = [
        (FOOD, "Питание"),
        (DRESS, "Одежда/Обувь"),
        (FOR_HOME, "Для дома"),
        (AUTO, "Авто"),
        (TRANSPORT, "Транспорт"),
        (H_SERVICE, "ЖКХ/Связь"),
        (ENTERTAIMENT, "Развлечения"),
        (PRESENT, "Подарки"),
        (SERVICE, "Услуги"),
        (CREDIT, "Кредиты"),
        (ACCUM, "Накопления"),
        (OTHER, "Другое"),
    ]

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    datetime = models.DateTimeField(
        default=pendulum.now, verbose_name="Дата платежа"
    )
    # Решено отказаться от DecimalField,
    # чтобы избежать заморочек с проверками isdigit() - проверяет int
    amount = models.PositiveIntegerField(verbose_name="Сумма платежа")
    category = models.CharField(
        max_length=50, choices=CATEGORY, verbose_name="Категория"
    )


class User(models.Model):

    user_id = models.CharField(max_length=100, primary_key=True)
    # До определенного момента в развитии группы
    # принято решение не хранить личных данных кроме ID
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    last_active = models.DateTimeField(
        default=pendulum.now,
        blank=True,
        null=True,
        verbose_name="Последняя активность",
    )

    last_payment = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Последний платеж"
    )

    status = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="status"
    )

    def update_active(self):
        self.last_active = pendulum.now()
        self.save()

    def update_status(self, status=None):
        self.status = status
        self.save()

    def roll_back(self):
        query = Paymount.objects.latest("datetime")
        query.delete()

    def history_callback(self, period):

        query = None
        messages = []

        # Последние 20 платежей в одном сообщении
        if period == "h_last_20":
            query = Paymount.objects.filter(user=self).order_by("-datetime")[
                :20
            ]
            total_accum = sum([i.amount for i in query])
            if query:
                limit = query.count()
                message = "Последние {} расходов:\n".format(limit)
                message += "Всего на сумму {} руб.\n".format(total_accum)

                for i in query[:20]:
                    dt = pendulum.instance(i.datetime)
                    dt = dt.in_tz("Europe/Moscow")
                    message += "{} {} {} руб.\n".format(
                        dt.strftime("%d.%m %H:%M"),
                        i.get_category_display(),
                        i.amount,
                    )
            else:
                message = "У вас ещё нет сохраненных платежей"

            messages.append(message)

        # Возращает список платажей за последние 7 дней
        # в виде списка со вложенным текстовым сообщением,
        # если длинна выборки из db больше 30 записей
        # в список будет добавлено еще одно сообщение
        elif period == "h_week":
            dt = pendulum.now()
            end_week = dt.set(hour=23, minute=59, second=59)
            start_week = end_week.subtract(days=7)
            query = (
                Paymount.objects.filter(user=self)
                .filter(
                    datetime__range=(
                        start_week.add(hours=3),
                        end_week.add(hours=3),
                    )
                )
                .order_by("-datetime")
            )

            total_accum = sum([i.amount for i in query])
            message = "Расходы  c {} по {}\n".format(
                start_week.strftime("%d.%m"), end_week.strftime("%d.%m")
            )
            message += "Всего за неделю: {} руб.\n".format(total_accum)

            if query:
                if query.count() < 30:
                    for i in query:
                        dt = pendulum.instance(i.datetime)
                        dt = dt.in_tz("Europe/Moscow")
                        message += "{} {} {} руб.\n".format(
                            dt.strftime("%d.%m %H:%M"),
                            i.get_category_display(),
                            i.amount,
                        )
                    messages.append(message)

                else:
                    count = 0
                    for i in range(len(query) // 30 + 1):
                        chunk = query[count : count + 30]
                        count += 30
                        if chunk:
                            for every in chunk:
                                dt = pendulum.instance(every.datetime)
                                dt = dt.in_tz("Europe/Moscow")
                                message += "{} {} {} руб.\n".format(
                                    dt.strftime("%d.%m %H:%M"),
                                    every.get_category_display(),
                                    every.amount,
                                )
                        messages.append(message)
                        message = "продолжение...\n"

            else:
                message = "Нет платежей за выбранный период"
                messages.append(message)

        # Возращает список платажей за последний месяц
        # в виде списка со вложенным текстовым сообщением,
        # если длинна выборки из db больше 30 записей
        # в список будет добавлено еще одно сообщение
        elif period == "h_month":
            dt = pendulum.now()
            end_month = dt.set(hour=23, minute=59, second=59)
            start_month = end_month.subtract(months=1)
            query = (
                Paymount.objects.filter(user=self)
                .filter(
                    datetime__range=(
                        start_month.add(hours=3),
                        end_month.add(hours=3),
                    )
                )
                .order_by("-datetime")
            )
            total_accum = sum([i.amount for i in query])

            message = "Расходы  c {} по {}\n".format(
                start_month.strftime("%d.%m"), end_month.strftime("%d.%m")
            )
            message += "Всего за месяц: {} руб.\n".format(total_accum)

            if query:
                if query.count() < 30:
                    for i in query[:30]:
                        dt = pendulum.instance(i.datetime)
                        dt = dt.in_tz("Europe/Moscow")
                        message += "{} {} {} руб.\n".format(
                            dt.strftime("%d.%m %H:%M"),
                            i.get_category_display(),
                            i.amount,
                        )
                    messages.append(message)

                else:
                    count = 0
                    for i in range(len(query) // 30 + 1):
                        chunk = query[count : count + 30]
                        count += 30
                        if chunk:
                            for every in chunk:
                                dt = pendulum.instance(every.datetime)
                                dt = dt.in_tz("Europe/Moscow")
                                message += "{} {} {} руб.\n".format(
                                    dt.strftime("%d.%m %H:%M"),
                                    every.get_category_display(),
                                    every.amount,
                                )
                        messages.append(message)
                        message = "продолжение...\n"
            else:
                message = "Нет платежей за выбранный период"
                messages.append(message)

        return messages

    def statistics_callback(self, period):
        # !все данные возращаемые в разделе statistics, отличные от "full",
        # являются завершенным временным отрезком
        # т.е. предыдущая неделя или месяц
        query = Paymount.objects.filter(user=self)

        w = Wall(period, query)
        r = Round(period, query)
        w_gr = w.run()
        r_gr = r.run()

        return [w_gr, r_gr]
