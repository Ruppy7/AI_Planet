from django.urls import path
from . import views

urlpatterns = [
    path('login', views.userLogin, name="login"),
    path('signup', views.signup),
    path('test', views.test_token),
    path('logout', views.logout),
    path('', views.index, name="index"),
    path('home', views.home, name="home")
]