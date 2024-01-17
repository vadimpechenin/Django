from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request): #HttpRequest
    return HttpResponse("Страница приложения women.")


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
