from django.contrib import admin
from .models import Group, Discussion, Comment
# Register your models here.

admin.site.register(Group)
admin.site.register(Discussion)
admin.site.register(Comment)

