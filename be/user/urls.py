from django.urls import path

from user.views import register_or_login


urlpatterns = [
    path('register',register_or_login)
]
