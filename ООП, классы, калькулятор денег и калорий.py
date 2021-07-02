import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = float(amount)
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        today = dt.date.today()
        today_amount = sum([
            record.amount
            for record in self.records
            if record.date == today
        ])
        return today_amount

    def get_week_stats(self):
        today = dt.date.today()
        one_week_ago_date = today - dt.timedelta(days=7)
        week_amount = float(sum([
            record.amount
            for record in self.records
            if one_week_ago_date <= record.date <= today]))
        return week_amount

    def get_today_remained(self):
        today_amount = self.get_today_stats()
        balance = round(self.limit - today_amount, 2)
        return balance


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):

        currencies = {
            'eur': ('Euro', CashCalculator.EURO_RATE),
            'usd': ('USD', CashCalculator.USD_RATE),
            'rub': ('руб', CashCalculator.RUB_RATE),
        }

        today_remained = self.get_today_remained()
        currency_name, currency_rate = currencies[currency]
        today_remained_currency = abs(round(today_remained / currency_rate, 2))

        if not today_remained:
            return 'Денег нет, держись'
        if today_remained > 0:
            return (f'На сегодня осталось {today_remained_currency} {currency_name}')
        else:
            return (f'Денег нет, держись: твой долг -'
                        f' {today_remained_currency} {currency_name}')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_remained = self.get_today_remained()

        if today_remained > 0:
            today_remained = int(today_remained)
            return (
                f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {today_remained} кКал')

        return 'Хватит есть!'


    # думаю else здесь не нужен, т.к. функция return автоматически завершает выполнение этого метода?
    #   т.е. либо мы выводим первый return и выходим, либо пробегаем дальше по методу и выходим
    #       через второй return
