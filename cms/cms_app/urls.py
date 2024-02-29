from django.urls import path
from . import views

urlpatterns = [
    path('sign-up',views.UserSignupView.as_view()),
    path('sign-in',views.UserLoginView.as_view()),
    path('logout',views.UserLogoutView.as_view()),
    path('content',views.ContentItemView.as_view()),
    path('content/<int:pk>',views.ContentItemView.as_view()),
]