from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from db.сategories import Categories
from tortoise import run_async
from run_tortoise import run_t

from handler import expen


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await expen.create_user(int(update.message.from_user.id))
    await update.message.reply_text("Это бот для учета финансов\n\n Добавить расход: 250 такси\n "
                                    "Статистика за сегодня /today\n За текуший месяц /month\n"
                                    "Последний внесенные расходы /last \n Катеегории трат /categories")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Добавить расход: 250 такси\n "
                                    "Статистика за сегодня /today\n За текуший месяц /month\n"
                                    "Последний внесенные расходы /last \n Катеегории трат /categories")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = int(update.message.from_user.id)
    expense = await expen.add_expen(update.message.text, user_id)

    if isinstance(expense, Expenses):
        answer_message = (
            f"Добавлены траты:\n{expense.amount} руб на {expense.category_name}.")
        await update.message.reply_text(answer_message)
    elif isinstance(expense, Message):
        answer_massage = expense.category_text
        await update.message.reply_text(answer_massage)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = int(update.message.from_user.id)
    answer_message = await expen.get_today_statistic(user_id)

    await update.message.reply_text(answer_message)


async def all_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # костыль потому что в __init__ нельзя вызвать async
    force = Categories()
    await force.init()

    categories = force.get_all_category()
    answer_message = "Категории трат:\n\n" + (
        "\n".join([i.name + ": (" + ", ".join(i.aliases) + " )" for i in categories]))
    await update.message.reply_text(answer_message)


async def month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = int(update.message.from_user.id)
    answer_message = await expen.get_month_statistic(user_id)

    await update.message.reply_text(answer_message)


async def last(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = int(update.message.from_user.id)
    last_expenses = await expen.last_expenses(user_id)

    if last_expenses == []:
        await update.message.reply_text("Сегодня еще не было расходов")
    else:
        last_expenses_rows = [f"{expense.amount} руб на {expense.category_name}" \
                              f" для удаления нажмите /del{expense.id}\n" for expense in last_expenses]

        answer_message = f"Последние сохраненные траты:\n\n" + "\n".join(last_expenses_rows)
        await update.message.reply_text(answer_message)


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    index = int(update.message.text[4:])
    user_id = int(update.message.from_user.id)
    await expen.delete(index, user_id)
    answer_message = "Удалилась"
    await update.message.reply_text(answer_message)


def main() -> None:
    bot = Application.builder().token("TOKEN").build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("help", help))

    bot.add_handler(CommandHandler("categories", all_categories))
    bot.add_handler(CommandHandler("today", today))
    bot.add_handler(CommandHandler("month", month))
    bot.add_handler(CommandHandler("last", last))

    bot.add_handler(MessageHandler(filters.COMMAND, delete))
    bot.add_handler(MessageHandler(filters.TEXT, add))

    bot.run_polling()


if __name__ == '__main__':
    run_async(run_t.setup_db())
    main()
