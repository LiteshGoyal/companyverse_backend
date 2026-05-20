from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('tasks/', include('tasks.urls')),
    # path('auditlogs/', include('auditlogs.urls')),
    path('requirements/', include('requirements.urls')),
    path("ratings/", include("ratings.urls")),
    path(
        "auditlogs/",
        include("auditlogs.urls")
    ),
    path("notifications/", include("notifications.urls")),
    path(
        "dashboard/",
        include("dashboard.urls")
    ),
]
