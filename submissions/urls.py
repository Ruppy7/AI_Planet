from django.urls import path
from . import views

urlpatterns = [
    path('login', views.userLogin, name="login"),
    path('signup', views.signup, name='signup'),
    path('test', views.test_token),
    path('logout', views.logoutUser, name='logout'),
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('hackathons', views.HackathonListCreateView.as_view(), name='hacklist')
]