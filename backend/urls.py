
from django.contrib import admin
from django.urls import path, include
from base.api.views import Register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.api.urls')),
    path('register/', Register.as_view(), name='register'),
]