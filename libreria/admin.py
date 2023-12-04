from django.contrib import admin
from .models import CustomUser
from libreria.models import Post

admin.site.register(CustomUser)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')



