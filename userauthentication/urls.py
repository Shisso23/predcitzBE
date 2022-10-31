from django.urls import path
from .views import Register, Login, CurrentUser

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('user', CurrentUser.as_view())
]
