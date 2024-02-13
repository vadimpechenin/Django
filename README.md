# Уроки по Django
Коды из ютуб плейлиста Сергея Балакирева "Добрый, добрый Django".

## Стэк технологий
python 3.8.8
Django 4.2.1
ipython 8.12.3
django-extensions 3.2.3

## Полезные ссылки
https://docs.djangoproject.com/en/4.2/topics/http/urls/
https://proproprogs.ru/django4


## Команды для начала:
>>>django-admin #список команд
>>>django-admin startproject имясайта #создание проекта

>>>имясайта>python manage.py runserver #запуск сервера

по адресу http://127.0.0.1:8000/ находится фронтэнд

>>>имясайта>python manage.py runserver 4000 #поменять порт

>>>имясайта>python manage.py startapp названиеприложения #создание нового приложения
После создания нового приложения появится каталог в каталоге приложений. В основном приложении в файле settings.py необходимо 
добавить созданное приложение в список INSTALLED_APPS "названиеприложения.apps.НазваниеКлассаВApps"

## Сбор всех статических файлов из проектов в единый
>>>python manage.py collectstatic

## Создание файлов миграций
>>>python manage.py makemigrations

## Выполнение запросов к бд
### Создание запроса
>>>python manage.py sqlmigrate women 0001 // 0001_initial нужен только номер
### собсвтенно выполнение запросов к бд
>>>python manage.py migrate

## Переход в командную оболочку django
>>>python manage.py shell
###Выход из БД
>>>CTRL+Z или exit для IPython
### Создание объекта-модели и ее запись в БД
>>>from <имясайта>.models import <Название_класса_модели>
>>>w1 = Women(title = 'Name', content = 'Content')
>>>w1.save()
## Посмотреть запросы
>>>from django.db import connection
>>>connection.queries

## Работа в оболочке django-extension
>>>python manage.py shell_plus --print-sql
>>>Women.objects.create(title='Ума Турман', content='Биография Умы Турман')  //Сразу создать и записать
>>>Women.objects.all() //Выбарать все записи
>>>w = Women.objects.all()[0] //Прочитать первую запись
>>>ws= Women.objects.filter(title='Энн Хэтуей') //Отобрать запись по полю
>>>ws= Women.objects.filter(pk__gt=2) //__gt - аналог >, pk==id
>>>ws= Women.objects.filter(title__contains='ли') //__contains, включает фрагмент
>>>ws= Women.objects.filter(pk__in=[2,5,11,12])  //Отбор записей, где встречается хотя бы один элемент из списка
>>>ws= Women.objects.filter(pk__in=[2,5,11,12], is_published=1) // через , - аналогично and в sql-запросе
>>>Women.objects.exclude(pk=2) //Выбирает все записи, за исключением указаного - аналог NOT
>>>Women.objects.get(pk=2) // метод get возвращает строго одну запись, не список

>>>Women.objects.order_by("title") // сортировка по title, ORDER BY
>>>Women.objects.filter(pk__lte=4).order_by("title") //  WHERE "women_women"."id" <= 4 ORDER BY "women_women"."title" ASC
>>>Women.objects.order_by("-title") // сортировка по возрастанию,  ORDER BY "women_women"."title" DESC
//Изменение записей в БД
>>>wu = Women.objects.get(pk=2)
>>>wu.title = 'Марго Робби'
>>>wu.save()
//Изменение всех записей таблицы
>>>Women.objects.update(поле_для_изменения=новое_значение)
>>> Women.objects.filter(pk__lte=4).update(is_published=1) // обновили первые 4 записи при помощи filter, срезы использовать нельзя
//Удаление записей
>>>wd = Women.objects.filter(pk__gte=5) //отобрали записи
>>>wd.delete() // собственно удаление. Можно в одну строчку с предыдущим


## Создание связанных таблиц
1. models.CASCADE - при удалении записи из первичной модели (Category) происходит удаление всех записей из вторичной модели (Women)
2. models.PROTECT - запрещает удаление записи из первичной модели, если она используется во вторичной
3. models.SET_NULL - при удалении записи первичной модели устанавливает занчение foreign key в NULL у соответствующих записей вторичной модели
4. models.SET_DEFAULT - то же самое, что и SET_NULL, только вместо значения NULL устанавливает значение по умолчанию, которое должно быть определено через класс ForeignKey
5. models.DO_NOTHING - удаление записи в первичной модели не вызывает никаких действий у вторичных моделей

## Связь многие к одному
>>>Women.objects.filter(cat__slug="aktrisy") //обращение к полю связанной таблицы через поле ForeignKey текущей таблицы, двойное подчеркивание
>>>Category.objects.filter(posts__title__contains="ли").distinct()
/* 
SELECT DISTINCT "women_category"."id",
       "women_category"."name",
       "women_category"."slug"
  FROM "women_category"
 INNER JOIN "women_women"
    ON ("women_category"."id" = "women_women"."cat_id")
 WHERE "women_women"."title" LIKE '%ли%' ESCAPE '\'
 LIMIT 21
 */

## Q-классы
// Позволяет делать логическое OR и не только
>>>Women.objects.filter(pk__lt=5, cat_id=2) // По умолчанию только AND 
/*
 FROM "women_women"
 WHERE ("women_women"."cat_id" = 2 AND "women_women"."id" < 5)
*/
>>>Women.objects.filter(Q(pk__lt=5) | Q(cat_id=2))
/*
 FROM "women_women"
 WHERE ("women_women"."id" < 5 OR "women_women"."cat_id" = 2)
*/
>>>Women.objects.filter(Q(pk__lt=5) & Q(cat_id=2)) //Теперь AND

>>>Women.objects.filter(~Q(pk__lt=5) | Q(cat_id=2)) //Теперь есть NOT и OR

>>>Women.objects.filter(Q(pk__in=[1, 2, 5]) | Q(cat_id=2), title__icontains="ра")
/*
 WHERE (("women_women"."id" IN (1, 2, 5) OR "women_women"."cat_id" = 2) AND "women_women"."title" LIKE '%ра%' ESCAPE '\')
*/

## F, Value и метод annotate()
// F представляет значение поля модели, преобразованное значение поля модели или аннотированный столбец.
// Он позволяет ссылаться на значения полей модели и выполнять операции с базой данных, 
// используя их без необходимости извлекать их из базы данных в память Python.
>>>from django.db.models import F

>>>Women.objects.filter(pk__gt=F("cat_id"))
/*
 WHERE "women_women"."id" > ("women_women"."cat_id")
 */
>>>Husband.objects.update(m_count=F("m_count")+1)
/*
UPDATE "women_husband"
SET "m_count" = ("women_husband"."m_count" + 1)
*/

// Метод annotate позволяет создавать новые, дополнительные вычисляемые поля
>>> from django.db.models import Value

>>>lst = Husband.objects.all().annotate(is_married=Value(True))
>>>for i, x in enumerate(lst):
...:     if i==0:
...:         print(list(x.__dict__)[1:])
...:     print(list(x.__dict__.values())[1:])
...:

/*
SELECT "women_husband"."id",
       "women_husband"."name",
       "women_husband"."age",
       "women_husband"."m_count",
       1 AS "is_married"
  FROM "women_husband"
  
['id', 'name', 'age', 'm_count', 'is_married']
[1, 'Брэд Питт', 30, 3, True]
*/
>>>lst = Husband.objects.all().annotate(is_married=F("m_count")*3)

>>>for i, x in enumerate(lst):
...:     if i==0:
...:         print(list(x.__dict__)[1:])
...:     print(list(x.__dict__.values())[1:])
...:
/*
SELECT "women_husband"."id",
       "women_husband"."name",
       "women_husband"."age",
       "women_husband"."m_count",
       ("women_husband"."m_count" * 3) AS "is_married"
  FROM "women_husband"

Execution time: 0.000000s [Database: default]
['id', 'name', 'age', 'm_count', 'is_married']
[1, 'Брэд Питт', 30, 3, 9]
*/

>>>lst = Husband.objects.all().annotate(work_age=F("age")-20)
/*
SELECT "women_husband"."id",
       "women_husband"."name",
       "women_husband"."age",
       "women_husband"."m_count",
       ("women_husband"."age" - 20) AS "work_age"
  FROM "women_husband"

Execution time: 0.000000s [Database: default]
['id', 'name', 'age', 'm_count', 'work_age']
[1, 'Брэд Питт', 30, 3, 10]
*/


