from django.contrib import admin
from django.urls import path, include
from libreria.api.router import router_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libreria.urls')),
    path('api/', include(router_post.urls)),
]
