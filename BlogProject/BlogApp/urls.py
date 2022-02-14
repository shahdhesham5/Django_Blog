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
    path('likepost/<post_id>', views.likepost, name='likepost'),
    path('dislikepost/<post_id>', views.dislikepost, name='dislikepost'),
    #show category posts
    path('enter-category/<cat_id>', views.enterCat, name='enter-category'),
    path('subscribe/<cat_id>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<cat_id>/', views.unsubscribe, name='unsubscribe'),
    #crud on categories
    path('categories/', views.categories, name='categories'),
    path('add-cat/', views.addCat, name='add-cat'),
    path('edit-cat/<cat_id>', views.editCat, name='edit-cat'),
    path('delete-cat/<cat_id>', views.delectCat, name='delete-cat'),
    #crud on tags
    path('tags/', views.tags, name='tags'),
    path('addtag/', views.addtag, name='addtag'),
    path('deltag/<tag_id>', views.deltag, name='deltag'),
    path('edit-tag/<tag_id>', views.editTag, name='edit-tag'),
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
    #crud on Forbidden words
    path('Fwords/', views.fwords, name='Fwords'),
    path('add-Fwords/', views.addFword, name='add-fword'),
    path('del-Fword/<fword_id>', views.delFword, name='del-Fword'),
    #search for tags and post titles 
    path('search/', views.search, name='search'),



    
]