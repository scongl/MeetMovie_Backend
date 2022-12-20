from django.contrib import admin
from .models import Review, Rating, Reply


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Review, ReviewAdmin)
admin.site.register(Rating, ReviewAdmin)
admin.site.register(Reply, ReviewAdmin)
