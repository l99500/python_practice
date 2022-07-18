import datetime

"""
适配器模式：
让两个既有的对象进行合作，唯一的目的就是执行翻译的任务。
"""


class AgeCalculator:
    def __init__(self, birthday):
        self.year, self.month, self.day = (
            int(x) for x in birthday.split('-')
        )

    def calculate_age(self, date):
        year, month, day = (int(x) for x in date.split('-'))
        age = year - self.year
        if (month, day) < (self.month, self.day):
            age -= 1
        return age


class DateAgeAdapter:
    def _str_date(self, date):
        return date.strftime("%Y-%m-%d")

    def __init__(self, birthday):
        birthday = self._str_date(birthday)
        self.calculator = AgeCalculator(birthday)

    def get_age(self, date):
        date = self._str_date(date)
        return self.calculator.calculate_age(date)


class AgeableDate(datetime.date):
    def split(self, char):
        return self.year, self.month, self.day


if __name__ == "__main__":
    bd = AgeableDate(1975, 6, 14)
    print(bd)
    today = AgeableDate.today()
    print(today)
    a = AgeCalculator(bd)
    print(a.calculate_age(today))