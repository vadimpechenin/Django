from django.db import models
from django.urls import reverse


# Create your models here.
class Women(models.Model):
    title = models.CharField(max_length = 255)
    #slug = models.SlugField(max_length=255, blank=True, db_index=True, default='') #При создании миграции хитрость, потом поле сделали уникальным
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True) #можно оставлять пустым
    time_create = models.DateTimeField(auto_now_add=True) #автоматически заполняется поле в момент появления записи
    time_update = models.DateTimeField(auto_now=True) #при изменении записи меняется поле
    is_published = models.BooleanField(default = True)

    def __str__(self):
        return self.title

    class Meta:
        #Специальный вложенный класс для создания методов работы с объектами
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

