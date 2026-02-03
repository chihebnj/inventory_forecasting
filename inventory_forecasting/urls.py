from django.contrib import admin
from django.db import router
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
]
