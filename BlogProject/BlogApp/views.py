from django.http import HttpResponse
from django.shortcuts import render,redirect
from BlogApp.decorators import unauthenticated_user,allowed_users, admin_only
from BlogApp.models import Category, Post , Comment, Fwords, Tag
from .forms import CommentForm, CreateUserForm,CategoryForm, FwordsForm,PostForm ,  TagForm#the modified UserCreationForm
#authentication
from django.contrib.auth.forms import UserCreationForm #replaced by CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User #User model to access users and admins

 
#authentications
#registration
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #assign the user to a group on creation
            # group = Group.objects.get(name='normaluser')
            # user.groups.add(group)
            messages.success(request, "Account created successfully for "+username)
            return redirect ('login')
    context = {'form':form}
    return render(request, 'BlogApp/register.html', context)

#login
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        #gather the username and the password entered on the login form
        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticate the data entered by the user
        user = authenticate(request, username=username, password=password)
        #if the user exists
        if user is not None:
            #check if blocked
            if user.groups.filter(name='blockedusers'):
                return HttpResponse("blocked")
            #if not blocked
            login(request, user)
            return redirect('home')
        #if not, show this flash message
        else:
            messages.info(request, 'Username or Password is incorrect')
    #displaying the loging form
    context ={}
    return render(request, 'BlogApp/login.html', context)

#logout
#redirect to home-page after logout, as an AnonymousUser
def logoutuser(request):
    logout(request)
    return redirect('home')


# Create your views here.
#show admins and users
@login_required(login_url='login')
@admin_only
def showUsers(request):
    users = User.objects.all()
    blocked_users = User.objects.filter(groups__name="blockedusers")
    context ={'users' : users, 'blocked_users':blocked_users}
    return render(request,'BlogApp/showusers.html', context)

#delete user
def deleteUser(request, user_id):
    user = User.objects.get(id = user_id)
    user.delete()
    return redirect('showusers')
#makeadmin 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def makeadmin(request, user_id):
    user=User.objects.get(id= user_id)
    my_group=Group.objects.get(name="admin")
    my_group.user_set.add(user)
    user.is_staff = True
    user.is_superuser = True
    #if the user was blocked before, they will be unblocked
    group = Group.objects.get(name='blockedusers')
    user.groups.remove(group)
    user.save()
    return redirect('showusers')



#block user
def blockUser(request,user_id):
    user = User.objects.get(id = user_id)
    my_group = Group.objects.get(name = "blockedusers")
    my_group.user_set.add(user)
    return redirect ('showusers')

#unblock user
def unblockUser(request, user_id):
    user = User.objects.get(id = user_id)
    group = Group.objects.get(name = "blockedusers")
    user.groups.remove(group)
    return redirect ('showusers')

#home
def home(request):
    all_categories = Category.objects.all()
    context = {'all_categories':all_categories}
    return render(request, 'BlogApp/home.html',context)

#Post details
def post(request,post_id):
    post = Post.objects.get(id = post_id)
    #geting total likes
    totallikes = post.total_likes()
    totaldislikes = post.total_dislikes()
    is_like = False
    for like in post.likes.all():
        if like == request.user:  #if user has already likes this post
            is_like = True
            break
    
    is_dislike = False   #checks whether user disliked this post or not
    for dislike in post.dislikes.all():
        if dislike == request.user:  #if user is already disliked this post
            is_dislike = True
            break
    # if adding comment
    if request.method == "POST":
        form = CommentForm(request.POST , request.FILES)
        if form.is_valid():
            comment = form.save(commit=False) # to insert the ForeignKey of post and user before saving comment
            comment.user = request.user
            comment.post = post
            comment.save()
    # show comments again after adding comment
    comments = Comment.objects.filter(post = post_id)
    form = CommentForm()
    tags = Tag.objects.filter(tags__id=post_id )
    context = {'post': post, 'comments': comments, 'form': form ,'totallikes':totallikes,'totaldislikes':totaldislikes,'is_like':is_like,'is_dislike':is_dislike, 'tags':tags, 'form': form} 
    return render(request, 'BlogApp/post.html', context)

# Post likes
@login_required(login_url='login')
def likepost(request, post_id):
    post = Post.objects.get(id=post_id)

    is_dislike = False   #checks whether user disliked this post or not
    for dislike in post.dislikes.all():
        if dislike == request.user:  #if user is already disliked this post
            is_dislike = True
            break
    if is_dislike:   #if user is already disliked this post, will undo it 
            post.dislikes.remove(request.user)
         
    is_like = False
    for like in post.likes.all():
        if like == request.user:  #if user has already likes this post
            is_like = True
            break
    if not is_like:
        post.likes.add(request.user) #if user didn't like post yet, will add like
    
    if is_like:
        post.likes.remove(request.user) #if user has already likes this post, will undo it
    return redirect('post',post_id=post_id)

# Post dislikes
@login_required(login_url='login')
def dislikepost(request, post_id):
    post = Post.objects.get(id=post_id)
    
    is_like = False
    for like in post.likes.all():
        if like == request.user:
            is_like = True
            break
    if is_like:
            post.likes.remove(request.user)
            
    is_dislike = False
    for dislike in post.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break
    if not is_dislike:
        post.dislikes.add(request.user)
    
    if is_dislike:
        post.dislikes.remove(request.user)

    dislikesnum = post.total_dislikes()
    if dislikesnum >= 10:
        post.delete()

    return redirect('post',post_id=post_id)

# delet comment from spcefic post
def deletecomment(request,post_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comment.delete()
    return redirect('post',post_id=post_id) # redirct to post view with this parameter

#manageblog
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def manageBlog(request):
    return render(request,'BlogApp/manageblog.html')

#subscribe to a category
def subscribe(request, cat_id):
    category = Category.objects.get(id = cat_id)


#enter category
def enterCat(request, cat_id):
    category = Category.objects.get(id = cat_id)
    category_posts = Post.objects.filter(category_id=cat_id)
    context ={'category': category, 'category_posts':category_posts}
    return render (request, 'BlogApp/enterCategory.html', context)

#show categories
def categories(request):
    all_categories = Category.objects.all()
    context = {'all_categories':all_categories}
    return render (request,'BlogApp/categories.html', context)


#add category
@allowed_users(allowed_roles=['admin'])
def addCat(request):
    if request.method == 'POST': #if submited, check the inputs, validate form, then save
        input = request.POST.get("category") #getting the category the customer trying to add
        try:
            x = Category.objects.get(category=input) #if category already exists
            messages.info(request, 'Category already exists')
            return redirect('add-cat')
        except:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('categories')

    else:
        form = CategoryForm()
        context = {'form': form}
        return render (request, 'BlogApp/addcat.html', context)


#delete category
def delectCat(request, cat_id):
    category = Category.objects.get(id=cat_id)
    category.delete()
    return redirect('categories')





#show posts
def posts(request):
    all_posts = Post.objects.all()
    context = {'all_posts':all_posts}
    return render (request,'BlogApp/posts.html', context)


#addpost
def addpost(request):
    if request.method == 'POST': #if submited, check the inputs, validate form, then save
        form = PostForm(request.POST , request.FILES)
        form2 = TagForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.tag.clear()
            post.save()
            postTags= form.cleaned_data['tag']
            for tag in postTags:
                tag_item = Tag.objects.get(tag_item= tag)
                post.save()
                post.tag.add(tag)
            if form2.is_valid():
                tagsArray = form2.cleaned_data['tag_item']
                tags = tagsArray.split(",")
                for tag in tags:
                    tag_item = Tag.objects.create(tag_item= tag)
                    tag_item.save()
                    post.save()
                    post.tag.add(tag_item)
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
        form2 = TagForm()
        context = {'form': form, 'form2': form2}
        return render (request, 'BlogApp/addpost.html', context)


#delete post
def deletepost(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('posts')

#update post
@login_required(login_url='login')
def updatepost(request,post_id):
    postSelected = Post.objects.get(id = post_id)
    if request.method ==  'POST' :
        form = PostForm(request.POST ,request.FILES ,instance = postSelected)
        form2 = TagForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.tag.clear()
            post.save()
            postTags= form.cleaned_data['tag']
            for tag in postTags:
                tag_item = Tag.objects.get(tag_item= tag)
                post.save()
                post.tag.add(tag)

            if form2.is_valid():
                tagsArray = form2.cleaned_data['tag_item']
                tags = tagsArray.split(",")
                for tag in tags:
                    tag_item = Tag.objects.create(tag_item= tag)
                    tag_item.save()
                    post.save()
                    post.tag.add(tag_item)
            post.save()
            return redirect('post', post_id=post_id)
    else:
        form = PostForm(instance = postSelected)
        form2 = TagForm()
        context = {'form': form, 'form2': form2}
        return render(request,"BlogApp/updatepost.html",context)



#searchforPosts
# @login_required(login_url='login')
# def searchforposts(request):
#     keyword = request.GET.get("keyword")
#     if keyword:
#         Posts = Posts.objects.filter(title__contains = keyword)
#         return render(request,"posts.html",{"Posts":Posts})

#     Posts = Posts.objects.all()
#     return render(request, 'BlogApp/posts.html',{"Posts":Posts})


#enter category
def enterCat(request, cat_id):
    category = Category.objects.get(id = cat_id)
    category_posts = Post.objects.filter(category_id=cat_id)
    context ={'category': category, 'category_posts':category_posts}
    return render (request, 'BlogApp/enterCategory.html', context)

#show categories
@allowed_users(allowed_roles=['admin'])
def fwords(request):
    all_fwords = Fwords.objects.all()
    context = {'all_fwords':all_fwords}
    return render (request,'BlogApp/Fwords.html', context)


#add Forbbiden Wordss
@allowed_users(allowed_roles=['admin'])
def addFword(request):
    if request.method == 'POST': #if submited, check the inputs, validate form, then save
        input = request.POST.get("fword") #getting the category the customer trying to add
        try:    
            x = Fwords.objects.get(fword=input) #if category already exists
            messages.info(request, 'it is already exists')
            return redirect('addfword')
        except:
            form = FwordsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('Fwords')
                
    else:
        form = FwordsForm()
        context = {'form': form}
        return render (request, 'BlogApp/add-fword.html', context)


#delete category
def delFword(request, fword_id):
    fword = Fwords.objects.get(id=fword_id)
    fword.delete()
    return redirect('Fwords')
    
