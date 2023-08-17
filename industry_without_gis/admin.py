from django.contrib import admin

from .models import IndustryWithoutGis


@admin.register(IndustryWithoutGis)
class IndustryWithoutGisModelAdmin(admin.ModelAdmin):
    list_display = ['industry_name', 'male', 'female', 'yearly_capacity']