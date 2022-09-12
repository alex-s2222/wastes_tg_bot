from tortoise import Tortoise
from db.models import Category
from db.сategories import Categories

async def setup_db():
    await Tortoise.init(db_url="sqlite://test.db", modules={"models": ["db.models"]})
    # await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["db.models"]})
    await Tortoise.generate_schemas()

    a = {1: ("product", "подукты", True, "еда"),
             2: ("dinner", "обед", False, "ланч, мак, kfc, столовая, поел "),
             3: ("transport", "общ. транспорт", True, "метро, автобус"),
             4: ("taxi", "покатушки", False, "такси"),
             5: ("mobile", "мобильная связь", True, "тел, моб, телефон"),
             6: ("subscriptions", "подписки", False, "подписка"),
             7: ("smoke", "курение", False, "сиги, сигареты, парилка"),
             8: ("other", "прочее", False, "")
             }

    for i in a:
        await Category.create(codename=a[i][0], name=a[i][1], is_basic_expense=a[i][2], aliases=a[i][3])

