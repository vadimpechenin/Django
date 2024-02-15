from django.contrib import admin

from women.models import Women, Category


@admin.register(Women)  #аналог admin.site.register(Women, WomenAdmin)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat') # поля для отображения в таблице
    list_display_links = ('id', 'title',) # какие поля позволяют перейти к описанию объекта
    ordering = ['-time_create', 'title'] #сортировка по полям
    list_editable = ('is_published',) #Кортеж полей для изменения
    list_per_page = 5 #Максимальное количество записей для отображения


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


#admin.site.register(Women, WomenAdmin)

