from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import forms
from .forms import EmployeeCreationForm
from .models import *

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee'
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]



class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_description', 'photo')
    list_display_links = ('user', 'job_description')
    search_fields = ('user', 'job_description')
    list_filter = ('user', 'job_description', 'user__is_staff')
    list_per_page = 25



admin.site.register(Employee, EmployeeAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(pickupPoint)
admin.site.register(news_item)
admin.site.register(about_company)
admin.site.register(faq)
admin.site.register(vacancy)
admin.site.register(review)
admin.site.register(promocode)
admin.site.register(productType)
admin.site.register(product)
admin.site.register(order)
admin.site.register(orderProduct)
admin.site.register(manufacturer)



# Register your models here.
