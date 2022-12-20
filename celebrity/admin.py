from django.contrib import admin
from .models import Celebrity, CelebrityImage


# Register your models here.
class CelebrityAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Celebrity, CelebrityAdmin)
admin.site.register(CelebrityImage, CelebrityAdmin)
