from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name= "register_user_view"),
    path('me/', views.MeView.as_view(), name= "user_me_view"),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path(
        "update-profile/",
        views.UpdateProfileView.as_view(),
        name="update_profile_view"
    ),
]
