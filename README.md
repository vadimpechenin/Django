# Уроки по Django
Коды из ютуб плейлиста Сергея Балакирева "Добрый, добрый Django".

## Стэк технологий
python 3.8.8
Django 4.2.1

##Полезные ссылки
https://docs.djangoproject.com/en/4.2/topics/http/urls/
https://proproprogs.ru/django4


##Команды для начала:
django-admin #список команд
django-admin startproject имясайта #создание проекта

имясайта>python manage.py runserver #запуск сервера

по адресу http://127.0.0.1:8000/ находится фронтэнд

имясайта>python manage.py runserver 4000 #поменять порт

имясайта>python manage.py startapp названиеприложения #создание нового приложения
После создания нового приложения появится каталог в каталоге приложений. В основном приложении в файле settings.py необходимо 
добавить созданное приложение в список INSTALLED_APPS "названиеприложения.apps.НазваниеКлассаВApps"

##Сбор всех статических файлов из проектов в единый
python manage.py collectstatic