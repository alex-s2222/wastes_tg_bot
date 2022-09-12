from typing import List, NamedTuple, Dict
from db.models import Category


class Temporary_category(NamedTuple):
    codename: str
    name: str
    is_basic_expense: bool
    aliases: List[str]


class Categories:
    _categories: List[Temporary_category]

    async def init(self):
        self._categories = await self._load_category()

    # загружаем категории из базы данных категории
    async def _load_category(self) -> List[Temporary_category]:
        categories = await Category.all().values()
        print(categories)
        categories = self._fill_aliases(categories)
        return categories

    # создаем List[классов] из строк базы данных
    def _fill_aliases(self, categories: List[Dict]) -> List[Temporary_category]:
        result_categories = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            result_categories.append(Temporary_category(
                codename=category["codename"],
                name=category["name"],
                is_basic_expense=category["is_basic_expense"],
                aliases=aliases
            ))
        return result_categories

    def get_all_category(self):
        return self._categories

    # выбрали класс с нужной категорией
    def get_category(self, category_name: str) -> Temporary_category:
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category

        print(finded)
        return finded