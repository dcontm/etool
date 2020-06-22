import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pendulum
import uuid
from collections import OrderedDict
import numpy as np


class Round:
    def __init__(self, period, query, title="", message="", status=True):
        self.period = period
        self.query = query
        self.title = title
        self.message = message
        self.status = status

    def get_period(self):
        # определяемся с временными границами
        # в зависимости от запрашиваемого периода
        date = pendulum.now(tz="UTC")
        start_period = date
        end_period = date

        if self.period == "s_week":
            # берем ближайщий понедельник и откатываемся на 7 дней =
            # понедельник прошедшей недели
            # если diff == 7 следовательно сегодня уже понедельник.
            if (date - date.previous(pendulum.MONDAY)).days < 7:
                start_period = date.previous(pendulum.MONDAY).subtract(days=7)
            else:
                start_period = date.previous(pendulum.MONDAY)
            end_period = start_period.end_of("week")

            self.message = (
                "Диаграмма деления платежей по категориям"
                "за прошедшую неделю "
                "с {} по {}"
            ).format(start_period.format("DD.MM"), end_period.format("DD.MM"))

        elif self.period == "s_month":
            prev_month = date.subtract(months=1)
            start_period = prev_month.start_of("month")
            end_period = prev_month.end_of("month")
            self.message = "Диаграмма деления платежей \
            по категориям за {}".format(
                prev_month.format("MMMM")
            )

        elif self.period == "s_full":
            if self.query:
                start_period = pendulum.instance(self.query[0].datetime)
                end_period = date
                self.message = "Диаграмма деления платежей по категориям \
                начиная с {}.".format(
                    start_period.format("DD.MM.YYYY")
                )
            else:
                self.status = False

        # проверяем был ли 1 платеж совершен ранее конца запрашиваемого периода
        # если нет устанавливаем статус в False и прекращаем расчеты
        if not self.query or self.query[0].datetime > end_period:
            self.status = False

        if self.query:
            self.title = (
                "Круговая диаграмма платежей по категориям \n"
                "за период c {} по {}"
            ).format(start_period.format("DD.MM"), end_period.format("DD.MM"))

        return (start_period, end_period)

    def get_data_values(self):
        period = self.get_period()

        if self.status:
            # фильтруем запрос относительно границ периода
            query = self.query.filter(datetime__range=period).order_by(
                "datetime"
            )
            data_dict = OrderedDict()

            # сортируем в упорядоченный словарь исходя из категории платежа
            # сохраняя размер платежа в список
            for i in query:
                if i.get_category_display() in data_dict:
                    data_dict[i.get_category_display()].append(i.amount)
                else:
                    data_dict[i.get_category_display()] = [i.amount]

            for i in data_dict:
                # суммируем значения для каждого ключа
                data_dict[i] = sum(data_dict[i])
            return [data_dict.keys(), data_dict.values()]

        else:
            return None

    def run(self):
        data = self.get_data_values()
        # если данные получены отрисовываем диаграмму
        if data:
            cmap = plt.get_cmap("Set3")
            colors = cmap(np.arange(12))

            fig, ax = plt.subplots()

            ax.pie(
                data[1],
                labels=data[0],
                colors=colors,
                autopct="%1.2f%%",
                radius=1,
                pctdistance=0.8,
                wedgeprops=dict(width=0.6, edgecolor="w"),
            )

            ax.set_title("{}".format(self.title), color="#999999")

            filename = (
                "/home/dcoxtm/project/media/grafics/" "round-{}-{}"
            ).format(self.period, uuid.uuid4())
            fig.savefig(filename)

            return {"filename": filename, "message": self.message}

        else:
            self.message = (
                "Ваш первый платеж произошел,"
                "позднее конца запрашиваемого периода."
            )

            return {"message": self.message}


class Wall:
    def __init__(self, period, query, title="", message="", status=True):
        self.period = period
        self.query = query
        self.title = title
        self.message = message
        self.status = status

    def get_period(self):
        # определяемся с временными границами
        # в зависимости от запрашиваемого периода
        date = pendulum.now(tz="UTC")
        start_period = date
        end_period = date

        if self.period == "s_week":
            # берем ближайщий понедельник и откатываемся на 7 дней =
            # понедельник прошедшей недели
            # если diff == 7 следовательно сегодня уже понедельник.
            if (date - date.previous(pendulum.MONDAY)).days < 7:
                start_period = date.previous(pendulum.MONDAY).subtract(days=7)
            else:
                start_period = date.previous(pendulum.MONDAY)
            end_period = start_period.end_of("week")

            self.message = (
                "Диаграмма величины платежей "
                "за прошедшую неделю "
                "с {} по {}"
            ).format(start_period.format("DD.MM"), end_period.format("DD.MM"))

        elif self.period == "s_month":
            prev_month = date.subtract(months=1)
            start_period = prev_month.start_of("month")
            end_period = prev_month.end_of("month")
            self.message = "Диаграмма величины платежей за {}".format(
                prev_month.format("MMMM")
            )

        elif self.period == "s_full":
            if self.query:
                start_period = pendulum.instance(self.query[0].datetime)
                end_period = date
                if (start_period - end_period).days > 62:
                    # ограничим максимальный период 2-мя месяцами
                    start_period = end_period.subtract(month=2)

                self.message = (
                    "Диаграмма величины платежей начиная с {}\n "
                    "!Внимание данные не позднее 2-х месячной"
                    " давности."
                ).format(start_period.format("DD.MM.YYYY"))
            else:
                self.status = False

        # проверяем был ли 1 платеж совершен ранее конца запрашиваемого периода
        # если нет устанавливаем статус в False и прекращаем расчеты
        if not self.query or self.query[0].datetime > end_period:
            self.status = False

        # это запишем в заголовке диаграммы
        if self.query:
            self.title = "Столбчатая диаграмма платежей\n \
            за период c {} по {}".format(
                start_period.format("DD.MM"), end_period.format("DD.MM")
            )

        return (start_period, end_period)

    def get_data_values(self):
        period = self.get_period()

        if self.status:
            # фильтруем запрос относительно границ периода
            query = self.query.filter(datetime__range=period).order_by(
                "datetime"
            )

            # определяем параметры для оси x исходя от запрашиваемого периода
            if self.period == "s_week":
                x_data = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            if self.period == "s_month":
                x_data = [i.format("DD.MM") for i in (period[1] - period[0])]
            if self.period == "s_full":
                x_data = [
                    i.format("DD.MM")
                    for i in (period[1].add(days=1) - period[0])
                ]
            # так как данные для x отличаются
            # заранее определим 'контейнеры' для фасовки
            if self.period == "s_week":
                y_data = [[] for i in range(7 + 1)]

                for i in query:  # распределяем запросы по дате
                    day = pendulum.instance(i.datetime)
                    day_of_week = day.day_of_week
                    y_data[day_of_week].append(i.amount)

                y_data = [sum(i) for i in y_data][1:]

            # для двух оставшихся фасуем с в упорядоченный словарь сопостовляя
            # данные c оси x c датой сохранения платежа
            else:
                y_data = OrderedDict.fromkeys(x_data, None)

                for i in query:  # распределяем запросы по дате
                    day = pendulum.instance(i.datetime)
                    day = day.format("DD.MM")
                    if y_data[day] != None:
                        y_data[day].append(i.amount)
                    else:
                        y_data[day] = [i.amount]

                # суммируем размер платаежа для каждого из ключей
                y_data = [sum(i) if i != None else 0 for i in y_data.values()]

                # для месяца избавляемся от излишней информативности
                # (не отображаем месяц в диаграмме)
                if self.period == "s_month":
                    x_data = [i.format("DD") for i in (period[1] - period[0])]

            return (x_data, y_data)

        else:
            return None

    def run(self):

        data = self.get_data_values()
        # если данные получены отрисовываем диаграмму
        if data:

            fig, ax = plt.subplots()
            plt.bar(data[0], data[1], color="purple")

            if len(data[0]) > 31:
                ax.xaxis.set_major_locator(MultipleLocator(3))
                ax.xaxis.set_minor_locator(MultipleLocator(1))
                ax.tick_params(labelsize=5)
            else:
                ax.tick_params(labelsize=6)

            ax.grid(True)

            ax.set_title("{}".format(self.title), color="#999999")
            ax.set_xlabel("Дата", color="#999999")
            ax.set_ylabel("Размер платежа", color="#999999")

            fig.tight_layout()

            filename = (
                "/home/dcoxtm/project/media/" "grafics/wall-{}-{}"
            ).format(self.period, uuid.uuid4())

            fig.savefig(filename)

            return {"filename": filename, "message": self.message}

        else:
            self.message = (
                "Ваш первый платеж произошел,"
                "позднее конца запрашиваемого периода."
            )
            return {"message": self.message}
