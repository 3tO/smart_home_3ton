from django.contrib import admin
from .models import *

class ValuesAdmin(admin.ModelAdmin):
    list_display  = ['topic', 'value', 'date_pub']
    list_filter   = ['topic', 'date_pub']
    list_editable = ['value']

admin.site.register(Topic)
admin.site.register(Values, ValuesAdmin)
