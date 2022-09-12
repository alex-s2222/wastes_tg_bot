from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(unique=True)
    daily_limit = fields.IntField()


class Category(Model):
    codename = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=40)
    is_basic_expense = fields.BooleanField()
    aliases = fields.CharField(max_length=255)


class Expense(Model):
    id = fields.IntField(pk=True)
    #  user_expense = fields.ForeignKeyField("models.User")
    price = fields.IntField()
    created = fields.DateField()
    category = fields.CharField(max_length=255)


