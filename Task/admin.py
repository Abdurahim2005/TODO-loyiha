from django.contrib import admin
from Task import models as models
from .models import Task, Category
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "created_at", "updated_at", "user")
    list_filter = ("status", "deadline")
    ordering = ("-updated_at",)
    search_fields = ("title",)
    list_editable = ("status", "priority")
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name",)
