from django.urls import path,include
from .views import RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # REGISTER
    path('register/', RegisterView.as_view()),

    # LOGIN (JWT)
    path('login/', TokenObtainPairView.as_view()),

    # REFRESH TOKEN
    path('refresh/', TokenRefreshView.as_view()),

    # PROFILE
    path('profile/', ProfileView.as_view()),
]