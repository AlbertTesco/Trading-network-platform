from django.contrib import admin

from user.models import User


# Register your models here.
@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
