from django.urls import path

from .views import (
    MyNotificationsView,
    MarkNotificationReadView
)

urlpatterns = [

    path(
        "my/",
        MyNotificationsView.as_view(),
        name="my_notifications_view"
    ),

    path(
        "<uuid:pk>/read/",
        MarkNotificationReadView.as_view(),
        name="mark_notification_read_view"
    ),
]