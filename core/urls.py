from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/templates/', include('templates_app.urls')),
    path('api/v1/calendar/', include('calendar_app.urls')),
]
