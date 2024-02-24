from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse

def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

class PublishedManager(models.Manager):
    # Пользовательский менеджер для моделей
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

class Women(models.Model):
    # Модель
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'


    title = models.CharField(max_length = 255, verbose_name = "Заголовок")
    #slug = models.SlugField(max_length=255, blank=True, db_index=True, default='') #При создании миграции хитрость, потом поле сделали уникальным
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = "Slug",                           validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    content = models.TextField(blank=True, verbose_name = "Текст статьи") #можно оставлять пустым
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = "Время создания") #автоматически заполняется поле в момент появления записи
    time_update = models.DateTimeField(auto_now=True, verbose_name = "Время изменения") #при изменении записи меняется поле
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default = Status.DRAFT, verbose_name = "Статус")
    #cat = models.ForeignKey('Category', models.PROTECT, null=True) #хитрость, когда нужно создать categories, а записи в Women уже есть
    cat = models.ForeignKey('Category', on_delete = models.PROTECT, related_name='posts', verbose_name = "Категории") #Category как строка, т.к. класс определен ниже
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name = "Теги")
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='woman', verbose_name = "Муж")

    # Менеджер по умолчанию
    objects = models.Manager()
    # новый менеджер
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        #Специальный вложенный класс для создания методов работы с объектами
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     #Автоматическая генерация slug при создании новой записи
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length = 100, db_index=True, verbose_name = "Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = "Slug")

    class Meta:
        #Специальный вложенный класс для создания методов работы с объектами
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name