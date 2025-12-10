from rest_framework import routers
from core import views
from django.urls import path,include


urlpatterns = [
              path('user/',views.CustomUserApi.as_view()),
              path('LoginUserView/',views.UserLoginView.as_view()),
              path("events/",views.EventApi.as_view()),

             
]