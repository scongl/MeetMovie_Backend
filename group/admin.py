from django.contrib import admin
from .models import Group, Discussion, Comment
# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Group, GroupAdmin)
admin.site.register(Discussion, GroupAdmin)
admin.site.register(Comment, GroupAdmin)

