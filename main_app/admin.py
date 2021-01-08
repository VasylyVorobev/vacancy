from django.contrib import admin
from .models import Vacancy, Specialty, Company, Resume, Application


@admin.register(Vacancy)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Specialty)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'code']


@admin.register(Company)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Resume)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class CategoryAdmin(admin.ModelAdmin):
    pass
