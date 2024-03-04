from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from women.models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'maried':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Women)  #аналог admin.site.register(Women, WomenAdmin)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband','tags'] #Отображаемые поля для редактирования
    #exclude = ['tags', 'is_published'] #поля, которые не будут отображаться
    readonly_fields = ['post_photo'] #нередактируемые поля
    prepopulated_fields = {"slug": ("title", )} #генерация поля автоматически
    #filter_horizontal = ["tags"]
    filter_vertical = ["tags"]
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat') # поля для отображения в таблице
    list_display_links = ('title',) # какие поля позволяют перейти к описанию объекта
    ordering = ['-time_create', 'title'] #сортировка по полям
    list_editable = ('is_published',) #Кортеж полей для изменения
    list_per_page = 5 #Максимальное количество записей для отображения
    actions=['set_published','set_draft'] #Список задаваемых действий
    search_fields = ['title__startswith','cat__name'] #Дополнительная панель поиск
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] #поля, по которым будем делать фильтрацию
    save_on_top = True

    @admin.display(description="Изображение", ordering="content")
    def post_photo(self, women: Women):
        #Метод для возвращения пути к фото, его отображения
        if women.photo:
            return mark_safe(f"<img src=' {women.photo.url}' width=50>")
        else:
            return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count= queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Стять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации!", messages.WARNING) #WARNING формирует значек


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


#admin.site.register(Women, WomenAdmin)

