from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    # path('posts/', views.posts, name='posts'),
    #authentication
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    #show users
    path('showusers/', views.showusers, name='show-users'),
]