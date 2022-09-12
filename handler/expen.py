import datetime
import re
from typing import NamedTuple, List, Optional

import pytz

from db.models import Expense
from db.сategories import Categories
from handler import exceptioms


class Message(NamedTuple):
    amount: int
    category_text: str


class Expenses(NamedTuple):
    id: Optional[int]
    amount: int
    category_name: str


async def add_expen(message: str):
    parse_message = _parse_message(message)
    force = Categories()
    await force.init()
    # получили класс с категорией
    category = force.get_category(category_name=parse_message.category_text)

    await Expense.create(price=parse_message.amount, category=category.codename, created=_get_now_format())
    return Expenses(id=None, amount=parse_message.amount, category_name=category.name)


async def get_today_statistic() -> str:
    today_list = await Expense.all().filter(created=_get_now_format()).values_list("price", flat=True)

    if today_list == []:
        return "Сегодня еще не было никаких расходов"

    result_all = 0
    for i in today_list:
        result_all += i
    return f"Расходы сегодня:\nВсего - {result_all}"


async def get_month_statistic() -> str:
    now = _get_now_datetime()
    first_day_of_month = f"{now.year:04d}-{now.month:02d}"

    # не очень нравится __startwith не забыть спроситьь можно ли сделать >=
    month_list = await Expense.all().filter(created__startswith=first_day_of_month).values_list("price", flat=True)

    if month_list == []:
        return "За этот месяц еще не было расходов"

    result_all = 0
    for i in month_list:
        result_all += i
    return f"Расходы за месяц:\nВсего: - {result_all}"


async def last_expenses() -> List[Expenses]:
    rows = await Expense.all().filter(created=_get_now_format()).values("category", "price", "id")
    rows = rows[-3:]

    last_exp = [Expenses(id=row["id"], amount=row["price"], category_name=row["category"]) for row in rows]
    return last_exp


async def delete(index: int) -> None:
    await Expense.filter(id=index).delete()


def _parse_message(message: str) -> Message:
    message_result = re.match(r"([\d ]+) (.*)", message)

    if not message_result or not message_result.group(0) \
            or not message_result.group(1) or not message_result.group(2):
        raise exceptioms.NotCorrectMessage(
            "Не могу понять сообщение. Напишите в формате, например: \n1500 метро")

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
