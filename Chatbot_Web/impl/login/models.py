from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)
    pwd = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        db_table='user'
        verbose_name='用户表'
        verbose_name_plural='用户表'
        ordering=['name']