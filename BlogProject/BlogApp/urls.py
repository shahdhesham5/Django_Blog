from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    #posts
    path('posts/', views.posts, name='posts'),
    path('addpost/', views.addpost, name='addpost'),
    path('delete-post/<post_id>', views.deletepost, name='delete-post'),
    #category
    path('enter-category/<cat_id>', views.enterCat, name='enter-category'),
    #authentication
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('manageblog/', views.manageBlog, name='manageblog'),
    #crud on users
    path('blockuser/<user_id>', views.blockUser, name='blockuser'),
    path('unblockuser/<user_id>', views.unblockUser, name='unblockuser'),
    path('showusers/', views.showUsers, name='showusers'),
    path('makadmin/<user_id>', views.makeadmin, name='makeadmin'),
    #crud on categories
    path('categories/', views.categories, name='categories'),
    path('add-cat/', views.addCat, name='add-cat'),
    path('delete-cat/<cat_id>', views.delectCat, name='delete-cat'),
    
]