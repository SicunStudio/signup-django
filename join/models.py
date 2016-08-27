from django.db import models

# Create your models here.
class People(models.Model):
    cid = models.TextField(max_length=20)
    name = models.TextField(default=' ')
    sex = models.CharField(max_length=4, default='男')
    classname = models.TextField(default=' ', null=True)
    phone = models.CharField(max_length=13)
    qq = models.CharField(max_length=15, null=True)
    mail = models.TextField(null=True)

    depart1 = models.TextField(default=' ')
    depart2 = models.TextField(default=' ')
    adjustment = models.BooleanField(default=True)

    hobby = models.TextField(null=True)
    experience = models.TextField(null=True)
    judge = models.TextField(null=True)

    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
