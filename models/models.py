from tortoise.models import Model
from tortoise import fields


class Vacancy(Model):
    id = fields.IntField(pk=True)
    site = fields.CharField(max_length=20)
    site_id = fields.IntField()
    title = fields.CharField(max_length=255)
    company = fields.CharField(max_length=50)
    desc = fields.TextField()
    city = fields.CharField(max_length=50)
    salary = fields.CharField(max_length=50, null=True)
    link = fields.TextField()

    def __str__(self):
        return f"{self.title}\n{self.link}"
