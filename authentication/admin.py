from django.contrib import admin
from .models import Account
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'phone', 'date_creation')  # Columns to show in the list
    search_fields = ('login', 'email')  # Searchable fields
    list_filter = ('date_creation',)  # Filter options

admin.site.register(Account)