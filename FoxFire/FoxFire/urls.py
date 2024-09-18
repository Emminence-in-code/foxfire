from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("api.urls")),
    path("recovery/", include("forgot_password.urls")),
    path("notifications/", include("notifications_and_messages.urls")),
    path("admin/", admin.site.urls),
]
