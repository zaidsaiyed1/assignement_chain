from rest_framework import routers
from core import views
from django.urls import path,include


urlpatterns = [
              path('user/',views.CustomUserApi.as_view()),
              path('LoginUserView/',views.UserLoginView.as_view()),
              path("events/",views.EventApi.as_view()),
              path("events/<int:eid>/",views.EventApi.as_view()),
              path("events/<int:eid>/rsvp/",views.RSVPApi.as_view()),
              path("events/<int:eid>/rsvp/<int:rid>/",views.RSVPApi.as_view()),
              
             
]