from datetime import date
from tortoise.models import Model
from tortoise import fields

class Duty(Model):
    # таблица дежурных сотрудников
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=40)
    phone = fields.CharField(max_length=12)

    timetable : fields.ReverseRelation["DutyTimetable"]


class DutyTimetable(Model):
    # расписание дежурных сотрудников
    date = fields.DateField()
    staff = fields.ForeignKeyField("models.Tournament", related_name="timetable")
    

class WashTimetable(Model):
    # расписание постирочной комнаты
    date = fields.DateField()
    time = fields.TimeField()
    room = fields.CharField(max_length=3, null=True)


class KitchenTimetable(Model):
    # расписание дежурств
    date = fields.DateField()
    stair = fields.CharField(max_length=1)
    room = fields.CharField(max_length=3)


class Groups(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=15)
    markers = fields.JSONField()


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=15)
    markers = fields.JSONField()
