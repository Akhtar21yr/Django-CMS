from django.urls import path
from . import views

urlpatterns = [
    path('sign-up',views.UserSignupView.as_view()),
    path('sign-in',views.UserLoginView.as_view())
]