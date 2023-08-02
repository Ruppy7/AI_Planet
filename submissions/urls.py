from django.urls import path
from . import views

urlpatterns = [
    path('login', views.userLogin, name="login"),
    path('signup', views.signup, name='signup'),
    path('test', views.test_token),
    path('logout', views.logoutUser, name='logout'),
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('hackathons', views.HackathonListCreateView.as_view(), name='hacklist'),
    path('hackathons/<int:pk>', views.HackathonDetailView.as_view(), name='singlehk'),
    path('hkregister', views.HackathonRegistrationView.as_view(), name='hkregister'),
    path('hackathons/<int:pk>/submit', views.SubmissionView.as_view(), name='hksubmit'),
]