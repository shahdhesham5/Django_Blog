from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    #posts
    path('posts/', views.posts, name='posts'),
    path('post/<post_id>', views.post, name='post'),
    path('delcomment/<post_id>/<comment_id>', views.deletecomment, name='delete-comment'),
    path('addpost/', views.addpost, name='addpost'),
    path('deletepost/<post_id>', views.deletepost, name='deletepost'),
    path('updatepost/<post_id>', views.updatepost, name='updatepost'),
    #show category posts
    path('enter-category/<cat_id>', views.enterCat, name='enter-category'),
    #crud on categories
    path('categories/', views.categories, name='categories'),
    path('add-cat/', views.addCat, name='add-cat'),
    path('delete-cat/<cat_id>', views.delectCat, name='delete-cat'),
    path('subscribe/<cat_id>', views.subscribe, name='subscribe'),
    #authentication
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('manageblog/', views.manageBlog, name='manageblog'),
    #crud on users
    path('deleteuser/<user_id>', views.deleteUser, name='deleteuser'),
    path('blockuser/<user_id>', views.blockUser, name='blockuser'),
    path('unblockuser/<user_id>', views.unblockUser, name='unblockuser'),
    path('showusers/', views.showUsers, name='showusers'),
    path('makadmin/<user_id>', views.makeadmin, name='makeadmin'),
    
]