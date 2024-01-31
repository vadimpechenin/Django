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

