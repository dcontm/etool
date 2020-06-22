from django.contrib import admin
from . models import User, Paymount

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id']


class PaymountAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'datetime']


admin.site.register(User, UserAdmin)
admin.site.register(Paymount, PaymountAdmin)
