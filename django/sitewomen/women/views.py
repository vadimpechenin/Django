from django.http import HttpResponse, HttpResponseNotFound#, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify #импорт фильтров для страницы

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 1, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 1, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True}
]
# Шаблоны по документации https://docs.djangoproject.com/en/4.2/ref/templates
def index(request): #HttpRequest
    #t = render_to_string('women/index.html') #чтобы не подхватывались иные index.html из других прилоений,
                                             # помещаем в подкаталог women
    #return HttpResponse(t)
    data = {'title': 'главная, страница?',
            'menu': menu,
            'posts': data_db,
            }
    return render(request, 'women/index.html', context = data)

def about(request):
    data = {'title': 'О сайте'}
    return render(request, 'women/about.html', data)

def categories(request, cat_id: int):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}<p>")


def categories_by_slug(request, cat_slug):
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}<p>")


def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('music', )) #можно и кортеж, и список
        #return redirect('/', permanent=True) - перенаправление на главную страницу с кодом 301
        #return redirect(index) # перенаправление на главную страницу с кодом 302 (временная)
        return redirect(uri) #лучшая практика перенаправления, имя машрута
        #Вместо redirect
        #return HttpResponseRedirect(uri) #302
        #return HttpResponsePermanentRedirect(uri)  # 301
        #Просто обработка ошибки
        #raise Http404

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}<p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
