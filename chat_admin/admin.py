from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from chat_admin import models
from chat_admin.models import DishInfo


# admin.site.register(models.UserInfo)
# admin.site.register(models.TestData)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'u_name', 'u_type', 'u_content', 'u_price', 'u_rating')


admin.site.register(DishInfo, DishAdmin)
