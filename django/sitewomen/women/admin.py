from django.contrib import admin, messages
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
    list_display = ('title', 'time_create', 'is_published', 'cat','brief_info') # поля для отображения в таблице
    list_display_links = ('title',) # какие поля позволяют перейти к описанию объекта
    ordering = ['-time_create', 'title'] #сортировка по полям
    list_editable = ('is_published',) #Кортеж полей для изменения
    list_per_page = 5 #Максимальное количество записей для отображения
    actions=['set_published','set_draft'] #Список задаваемых действий
    search_fields = ['title__startswith','cat__name'] #Дополнительная панель поиск
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] #поля, по которым будем делать фильтрацию

    @admin.display(description="Краткое описание", ordering="content")
    def brief_info(self, women: Women):
        #Метод для пользовательского поля, которого нет в БД
        return f"Описание {len(women.content)} символов."

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

