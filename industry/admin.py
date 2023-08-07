from django.contrib import admin
from .models import Industry, IndustryPhoto


admin.site.register(IndustryPhoto)


@admin.register(Industry)
class IndustryModelAdmin(admin.ModelAdmin):
    list_display = ['industry_name', 'district', 'local_body']