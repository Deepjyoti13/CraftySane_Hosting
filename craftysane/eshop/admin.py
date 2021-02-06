from django.contrib import admin
from .models import *
# Register your models here.

class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']
    
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip', 'phone')
    list_filter = ['status']
    search_fields = ['name']

admin.site.register(Setting, SettingtAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
