from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Job, Location

# Register your models here.
admin.site.register(Job, MarkdownxModelAdmin)
admin.site.register(Location)