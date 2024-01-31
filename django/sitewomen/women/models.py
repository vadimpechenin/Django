from django.db import models

# Create your models here.
class Women(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField(blank=True) #можно оставлять пустым
    time_create = models.DateTimeField(auto_now_add=True) #автоматически заполняется поле в момент появления записи
    time_update = models.DateTimeField(auto_now=True) #при изменении записи меняется поле
    is_published = models.BooleanField(default = True)

    def __str__(self):
        return self.title

