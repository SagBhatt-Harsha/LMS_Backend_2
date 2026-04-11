from django.urls import path
from .views import *

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/me/', MeView.as_view()),

    path('users/', UserListCreateView.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateDeleteView.as_view()),
]