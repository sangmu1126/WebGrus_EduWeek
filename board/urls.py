from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('webboard.urls')),
    path('admin/', admin.site.urls),
]
