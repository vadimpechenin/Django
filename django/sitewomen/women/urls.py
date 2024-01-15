from django.urls import path, register_converter
from . import views
from . import converters


#Регистрация конвертеров
register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', views.index), #http://127.0.0.1:8000/
    path('cats/<int:cat_id>/', views.categories), #http://127.0.0.1:8000/cats/N/ Порядок важен!!
    # если slug поставить вперед, до до int никогда не доберемся! Сначала более частные конвертеры, потом более общие
    path('cats/<slug:cat_slug>/', views.categories_by_slug), #http://127.0.0.1:8000/cats/asgad/
    path('archive/<year4:year>/', views.archive), #http://127.0.0.1:8000/archive/2023/
]