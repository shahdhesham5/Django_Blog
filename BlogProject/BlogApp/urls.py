from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('posts/', views.posts, name='posts'),
    path('categories/', views.categories, name='categories'),
    path('add-cat/', views.addCat, name='add-cat'),
    path('delete-cat/<cat_id>', views.delectCat, name='delete-cat'),
    #authentication
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('manageblog/', views.manageBlog, name='manageblog'),
    #show users
    path('showusers/', views.showUsers, name='showusers'),
    path('makadmin/<user_id>', views.makeadmin, name='makeadmin'),

]