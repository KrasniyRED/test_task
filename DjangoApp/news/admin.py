from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import News
from .models import EmailTask

@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    list_filter = ('publication_date', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'publication_date'
    summernote_fields = ('content',)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [field for field in fields if field != 'preview_image']

@admin.register(EmailTask)
class EmailTaskAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipients", "send_at")
    search_fields = ("subject", "recipients")
    list_filter = ("send_at",)
