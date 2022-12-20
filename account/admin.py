from django.contrib import admin
from .models import UserInfo


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'nickname', 'avatar', 'prefer_genres', 'like_movies',
              'like_celebrities', 'introduction')

    list_per_page = 20

    search_fields = ('username', )
    list_display = ('username', 'nickname', 'avatar', 'introduction')


# Register your models here.
admin.site.register(UserInfo, UserAdmin)
admin.site.site_header = '觅影后台管理'
