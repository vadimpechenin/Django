from django.http import HttpResponse, HttpResponseNotFound#, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify #импорт фильтров для страницы
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

# Шаблоны по документации https://docs.djangoproject.com/en/4.2/ref/templates
# def index(request): #HttpRequest
#     #t = render_to_string('women/index.html') #чтобы не подхватывались иные index.html из других прилоений,
#                                              # помещаем в подкаталог women
#     #return HttpResponse(t)
#     # posts = Women.objects.filter(is_published=1)
#     posts = Women.published.all().select_related('cat')  # Выбрали все опубликованные статьи, "Жадная загрузка" связанных категорий
#
#     data = {'title': 'главная, страница?',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected': 0,
#             }
#     return render(request, 'women/index.html', context = data)

class WomenHome(ListView):
    #model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'


    def get_context_data(self,  *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Women.published.all().select_related('cat')

# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #Файл через функцию сохраняется в папке
            #handle_uploaded_file(form.cleaned_data["file"])
            #Файл сохраняется в БД
            fp = UploadFiles(file = form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()
    data = {'title': 'О сайте',
            'menu': menu,
            'form': form}
    return render(request, 'women/about.html', data)


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'women/post.html', data)

class ShowPost(DetailView):
    #model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #Сохранение в БД
#             #print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, "Ошибка добавления поста")
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'women/addpage.html', data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }

        return render(request, 'women/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }

        return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug = cat_slug)
#     posts = Women.published.filter(cat_id = category.pk).select_related('cat')
#
#     data = {'title': f'Рубрика: {category.name}',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected': category.pk,
#             }
#     return render(request, 'women/index.html', context = data)


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False #при пустом списке будет генерироваться исключение 404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

# def show_tag_post_list(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug = tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#             'title': f'Тег: {tag.tag}',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected': None,
#             }
#     return render(request, 'women/index.html', context = data)


class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False #при пустом списке будет генерироваться исключение 404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
