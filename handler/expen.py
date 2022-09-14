import datetime
import re
from typing import NamedTuple, List, Optional

import pytz

from db.models import Expense, User
from db.сategories import Categories


class Message(NamedTuple):
    amount: Optional[int]
    category_text: str


class Expenses(NamedTuple):
    id: Optional[int]
    amount: int
    category_name: str


# добавляем рассходы
async def add_expen(message: str, user_id: int) -> Expenses | Message:
    parse_message = _parse_message(message)
    if parse_message.amount == None:
        return Message(amount=None, category_text=parse_message.category_text)

    force = Categories()
    await force.init()
    # получили класс с категорией
    category = force.get_category(category_name=parse_message.category_text)
    await Expense.create(price=parse_message.amount, category=category.codename,
                         created=_get_now_format(), user_expense=user[0])
    return Expenses(id=None, amount=parse_message.amount, category_name=category.name)


# получаем стативстику за день
async def get_today_statistic(user_id: int) -> str:
    user = await User.filter(user_id=user_id)
    today_list = await Expense.filter(created=_get_now_format(), user_expense=user[0]).values_list("price", flat=True)

    if today_list == []:
        return "Сегодня еще не было никаких расходов"

    result_all = 0
    for i in today_list:
        result_all += i

    return f"Расходы сегодня:\nВсего - {result_all}"


# получаем стастику за день
async def get_month_statistic(user_id: int) -> str:
    # now = _get_now_datetime()
    # first_day_of_month = f"{now.year:04d}-{now.month:02d}"
    fist_day = datetime.datetime.today().replace(day=1)

    user = await User.filter(user_id=user_id)

    month_list = await Expense.filter(created__gte=fist_day, user_expense=user[0]).values_list("price", flat=True)
    # month_list = await Expense.filter(created__startswith=first_day_of_month).values_list("price", flat=True)

    if month_list == []:
        return "За этот месяц еще не было расходов"

    result_all = 0
    for i in month_list:
        result_all += i
    return f"Расходы за месяц:\nВсего: - {result_all}"


# получаем последние рассходы
async def last_expenses(user_id: int) -> List[Expenses]:
    user = await User.filter(user_id=user_id)
    rows = await Expense.filter(created=_get_now_format(), user_expense=user[0]).values("category", "price", "id")
    rows = rows[-3:]

    last_exp = [Expenses(id=row["id"], amount=row["price"], category_name=row["category"]) for row in rows]
    return last_exp


async def create_user(user_id: int):
    await User.create(user_id=user_id, daily_limit=500)


# удаляем рассход
async def delete(index: int, user_id) -> None:
    user = await User.filter(user_id=user_id)
    await Expense.filter(id=index, user_expense=user[0]).delete()

#
def _parse_message(message: str) -> Message:
    message_result = re.match(r"([\d ]+) (.*)", message)

    if not message_result or not message_result.group(0) \
            or not message_result.group(1) or not message_result.group(2):
        return Message(amount=None,
                       category_text="Не могу понять сообщение. Напишите в формате, например: \n1500 метро")

    amount = int(message_result.group(1))
    category_text = message_result.group(2).lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_format() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now



if __name__ == '__main__':
    _get_now_format()
