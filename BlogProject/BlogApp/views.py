from multiprocessing import context
from pickle import TRUE
from django import forms
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.test import tag
from BlogApp.decorators import unauthenticated_user,allowed_users, admin_only
from BlogApp.models import Category, Message, Post , Comment, Fwords, Tag, Subscribers
from .forms import CommentForm, CreateUserForm,CategoryForm, FwordsForm, MessageForm,PostForm , TagForm#the modified UserCreationForm
from django.core.paginator import Paginator
#authentication
from django.contrib.auth.forms import UserCreationForm #replaced by CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User #User model to access users and admins
#send email
from django.core.mail import send_mail
import re 

 
#authentications
#registration
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        email=request.POST.get('email')
        if email == "":
            messages.info(request, "Email is required")
        else:
            try:
                x=User.objects.get(email=email)
                messages.info(request, "Email is already registered")
                context = {'form':form}
                return render(request, 'BlogApp/register.html', context)
               
            except:    
                pass
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
                form = MessageForm()
                context = {'user': user, 'form':form }
                return render(request, 'BlogApp/blockedMessage.html' , context)
            else:
                if user is not None:
                    login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                else:
                    # return redirect(request.META.get('HTTP_REFERER'), history = -2)  #to stay in the same page after logging in
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
    # return redirect(request.META.get('HTTP_REFERER'))  #to stay in the same page after logging out
    
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
@login_required(login_url='login')
@admin_only
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
    email= user.email
    #send email confirming the block
    send_mail(
    'Congratulations!',
    f'Congratulations {user.username}, your account has been promoted! welcome on board!',
    'djangoblog2022@gmail.com',
    [f'{email}'],
    fail_silently=False,
)
    #if the user was blocked before, they will be unblocked
    try:
        group = Group.objects.get(name='blockedusers')
        user.groups.remove(group)
    except:
        pass
    user.save()
    return redirect('showusers')



#block user
@login_required(login_url='login')
@admin_only
def blockUser(request,user_id):
    user = User.objects.get(id = user_id)
    my_group = Group.objects.get(name = "blockedusers")
    my_group.user_set.add(user)
    email= user.email
    #send email confirming the block
    send_mail(
    'Account disabled!',
    f'Hello {user.username} your account has been disabled please contact your admin',
    'djangoblog2022@gmail.com',
    [f'{email}'],
    fail_silently=False,
)
    return redirect ('showusers')

#unblock user
@login_required(login_url='login')
@admin_only
def unblockUser(request, user_id):
    user = User.objects.get(id = user_id)
    group = Group.objects.get(name = "blockedusers")
    user.groups.remove(group)
    email= user.email
    #send email confirming the block
    send_mail(
    'Account unblocked!',
    f'Hello {user.username} your account has been unblocked, welcome back!',
    'djangoblog2022@gmail.com',
    [f'{email}'],
    fail_silently=False,
)
    return redirect ('showusers')

#home
def home(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            user = User.objects.get(id= request.POST.get("user"))
            message.user = user
            message.save()
            messages.info(request, 'Your message has been sent!')
            context = {'confirmation': True , 'user':user}
            return render(request, 'BlogApp/blockedMessage.html',context)
    all_categories = Category.objects.all()
    tags = Tag.objects.all()
    all_posts = Post.objects.all()
    # paginator for pagination
    paginator = Paginator(all_posts,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if not request.user.is_anonymous:
        all_subscribers = Subscribers.objects.filter(subscriber=request.user).values_list('category_id', flat=True)
        context = {'all_categories':all_categories, 'all_subscribers':all_subscribers,'tags':tags, 'page_obj':page_obj}
    else:
        context = {'all_categories':all_categories,'tags':tags, 'page_obj':page_obj }
    return render(request, 'BlogApp/home.html',context)



#Post details
def post(request,post_id):
    post = Post.objects.get(id = post_id)
    # comment = Comment.objects.get(id=comment_id)
    #geting total likes and dislikes for posts
    totallikes = post.total_likes()
    totaldislikes = post.total_dislikes()
    # if adding comment
    if request.method == "POST":
        form = CommentForm(request.POST , request.FILES)
        if form.is_valid():
            comment = form.save(commit=False) # to insert the ForeignKey of post and user before saving comment
            entered_comment= form.cleaned_data['comment_info'] #grapping the comment the user entered
            forbidden_words=list (Fwords.objects.values_list('fword', flat=True)) 
            #looping to remove any forbidden words
            for i in forbidden_words:
                # entered_comment = entered_comment.replace(i, len(i) * "*")
                entered_comment = re.sub(i, len(i)*"*" ,entered_comment, flags=re.IGNORECASE)
            comment.comment_info =  entered_comment #comment after filtration
            comment.user = request.user
            comment.post = post
            comment.save()
    # show comments again after adding comment
    comments = Comment.objects.filter(post = post_id)
    form = CommentForm()
    tags = Tag.objects.filter(tags__id=post_id )
    context = {'post': post, 'comments': comments, 'form': form ,'totallikes':totallikes,'totaldislikes':totaldislikes,'tags':tags, 'form': form} 
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

# Comment likes
@login_required(login_url='login')
def likecomment(request,post_id,comment_id):
    comment = Comment.objects.get(id=comment_id)

    is_dislike = False   #checks whether user disliked this comment or not
    for dislike in comment.dislikes.all():
        if dislike == request.user:  #if user is already disliked this comment
            is_dislike = True
            break
    if is_dislike:   #if user is already disliked this post, will undo it 
            comment.dislikes.remove(request.user)
         
    is_like = False
    for like in comment.likes.all():
        if like == request.user:  #if user has already likes this comment
            is_like = True
            break
    if not is_like:
        comment.likes.add(request.user) #if user didn't like comment yet, will add like
    
    if is_like:
        comment.likes.remove(request.user) #if user has already likes this comment, will undo it
    return redirect('post',post_id=post_id)

# Comments dislikes
@login_required(login_url='login')
def dislikecomment(request,post_id,comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    is_like = False
    for like in comment.likes.all():
        if like == request.user:
            is_like = True
            break
    if is_like:
            comment.likes.remove(request.user)
            
    is_dislike = False
    for dislike in comment.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break
    if not is_dislike:
        comment.dislikes.add(request.user)
    
    if is_dislike:
        comment.dislikes.remove(request.user)

    dislikesnum = comment.total_dislikes()
    if dislikesnum >= 10:
        comment.delete()

    return redirect('post',post_id=post_id)

#Reply to comments
@login_required(login_url='login')
def commentreply(request,post_id, comment_id):
    post = Post.objects.get(id=post_id)
    parent_comment = Comment.objects.get(id = comment_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.post = post
        new_comment.parent = parent_comment
        new_comment.save()
    return redirect('post',post_id=post_id)

# delete comment from spcefic post
@login_required(login_url='login')
def deletecomment(request,post_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comment.delete()
    return redirect('post',post_id=post_id)



#manageblog
@login_required(login_url='login')
@admin_only
# @allowed_users(allowed_roles=['admin'])
def manageBlog(request):
    return render(request,'BlogApp/manageblog.html')


#show categories on sidebar
@login_required(login_url='login')
@admin_only
def categories(request):
    all_categories = Category.objects.all()
    context = {'all_categories':all_categories}
    return render (request,'BlogApp/categories.html', context)

#subscribe to a category
@login_required(login_url='login')
def subscribe(request, cat_id):
    category = Category.objects.get(id = cat_id)
    subscriber = Subscribers.objects.create(category=category,subscriber=request.user)
    email = request.user.email
    #send email confirming subscription
    send_mail(
    'Subscription Successful!',
    f'Hello {request.user} Thank you for subscribing to {category}, welcome on board',
    'djangoblog2022@gmail.com',
    [f'{email}'],
    fail_silently=False,
)
    return redirect ('home')

#Unsubscribe to a category
@login_required(login_url='login')
def unsubscribe(request, cat_id):
    category = Category.objects.get(id = cat_id)
    subscriber = Subscribers.objects.get(category=category,subscriber=request.user)
    subscriber.delete()
    return redirect ('home')


#enter category
def enterCat(request, cat_id):
    category = Category.objects.get(id = cat_id)
    category_posts = Post.objects.filter(category_id=cat_id)
    context ={'category': category, 'all_posts':category_posts}
    return render (request, 'BlogApp/posts.html', context)

#tags on homepage
def tag(request, tag_id):
    tag_name = Tag.objects.get(id = tag_id)
    posts = Post.objects.filter(tag=tag_id).all()
    context ={'all_posts':posts, 'tag': tag_name}
    return render (request, 'BlogApp/posts.html', context)

#add category
@login_required(login_url='login')
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delectCat(request, cat_id):
    category = Category.objects.get(id=cat_id)
    category.delete()
    return redirect('categories')

#edit category
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editCat(request, cat_id):
    category =  Category.objects.get(id=cat_id)
    categories_list = list(Category.objects.values_list('category', flat=True))
    form = CategoryForm(instance=category)
    context = {'form': form, 'edit':True}
    if request.method == 'POST':
        #check if category already exists
        input = request.POST.get("category")
        if input in categories_list:
            messages.info (request, 'Category already exists')
            return render (request, 'BlogApp/addcat.html', context)        #if not found
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid:
            form.save()
            return redirect('categories')
    else:
        return render (request, 'BlogApp/addcat.html', context)

#show tags for admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def tags(request):
    all_tags = Tag.objects.all()
    context = {'all_tags':all_tags}
    return render (request,'BlogApp/showtags.html', context)

#addtag
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addtag(request):
    if request.method == 'POST':
        input = request.POST.get("tag_item")
        try:
            x = Tag.objects.get(tag_item=input) #if tag already exists
            messages.info(request, 'Tag already exists')
            return redirect('addtag')
        except:
            form = TagForm(request.POST)
            if form.is_valid():
                tag=form.save(commit=False)
                tag.tag_item = input.replace('#','')
                tag.save()
                return redirect('tags')
    else:
        form = TagForm()
        context = {'form':form}
        return render (request, 'BlogApp/addtag.html', context)
    
#delete tag by admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deltag(request,tag_id):
    tag = Tag.objects.get(id=tag_id)
    tag.delete()
    return redirect ('tags')



#edit tag by admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editTag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    form = TagForm(instance=tag)
    tags_list = list(Tag.objects.values_list('tag_item', flat=True))
    context = {'form': form, 'edit':True}
    if request.method == 'POST':
        input = request.POST.get('tag_item')
        if input in tags_list:
            messages.info (request, 'Tag already exists')      
            return render (request, 'BlogApp/addtag.html', context)  
        form = TagForm(request.POST, instance=tag)
        if form.is_valid:
            tag=form.save(commit=False)
            tag.tag_item = input.replace('#','')
            tag.save()
            return redirect('tags')
    else:
        return render (request, 'BlogApp/addtag.html', context)


# show posts
def posts(request):
    all_posts = Post.objects.all()
    context = {'all_posts':all_posts}
    return render (request,'BlogApp/posts.html', context)

#show the user their posts only
@login_required(login_url='login')
def yourPosts(request, user_id):
    user_posts = Post.objects.filter(user_id=request.user.id)
    context = {'all_posts':user_posts}
    return render (request,'BlogApp/posts.html', context)

#addpost
@login_required(login_url='login')
def addpost(request):
    if request.method == 'POST': #if submited, check the inputs, validate form, then save
        form = PostForm(request.POST , request.FILES)
        form2 = TagForm(request.POST)
        if form.is_valid():
            #1
            post = form.save(commit=False)
            forbidden_words=list (Fwords.objects.values_list('fword', flat=True))
            entered_title= form.cleaned_data['title'] #grapping the title the user entered
            #looping to remove any forbidden words
            for i in forbidden_words:
                entered_title = re.sub(i, len(i)*"*" ,entered_title, flags=re.IGNORECASE)
            post.title =  entered_title #title after filtration
            #2
            entered_content= form.cleaned_data['content'] #grapping the comment the user entered
            #looping to remove any forbidden words
            for i in forbidden_words:
                entered_content = re.sub(i, len(i)*"*" ,entered_content, flags=re.IGNORECASE)
            post.content =  entered_content #content after filtration
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
            return redirect('home')
    else:
        form = PostForm()
        form2 = TagForm()
        forbidden_words=list (Fwords.objects.values_list('fword', flat=True))
        fwords = ','.join(forbidden_words)
        new = True
        context = {'form': form, 'form2': form2, 'fwords':fwords, 'new': new}
        return render (request, 'BlogApp/addpost.html', context)


#delete post
@login_required(login_url='login')
def deletepost(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('home')


#update post
@login_required(login_url='login')
def updatepost(request,post_id):
    postSelected = Post.objects.get(id = post_id)
    if request.method ==  'POST' :
        form = PostForm(request.POST ,request.FILES ,instance = postSelected)
        form2 = TagForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #1
            forbidden_words=list (Fwords.objects.values_list('fword', flat=True))
            entered_title= form.cleaned_data['title'] #grapping the title the user entered
            #looping to remove any forbidden words
            for i in forbidden_words:
                entered_title = re.sub(i, len(i)*"*" ,entered_title, flags=re.IGNORECASE)
            post.title =  entered_title #title after filtration
            #2
            entered_content= form.cleaned_data['content'] #grapping the comment the user entered
            #looping to remove any forbidden words
            for i in forbidden_words:
                entered_content = re.sub(i, len(i)*"*" ,entered_content, flags=re.IGNORECASE)
            post.content =  entered_content #content after filtration
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
        forbidden_words=list (Fwords.objects.values_list('fword', flat=True))
        fwords = ','.join(forbidden_words)
        context = {'form': form, 'form2': form2, 'fwords':fwords, 'edit': True}
        return render(request,"BlogApp/addpost.html",context)



#show Forbidden words
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def fwords(request):
    all_fwords = Fwords.objects.all()
    context = {'all_fwords':all_fwords}
    return render (request,'BlogApp/Fwords.html', context)


#add Forbbiden Words
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addFword(request):
    if request.method == 'POST': #if submited, check the inputs, validate form, then save
        input = request.POST.get("fword") #getting the word the customer trying to add
        try:    
            x = Fwords.objects.get(fword=input) #if  already exists
            messages.info(request, 'it is already exists')
            return redirect('add-fword')
        except:
            form = FwordsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('Fwords')
    else:
        form = FwordsForm()
        context = {'form': form}
        return render (request, 'BlogApp/add-fword.html', context)

#edit Forbidden Words 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editFwords(request, fword_id):
    # grapping the word that want 
    fword= Fwords.objects.get(id=fword_id) 
    word = list(Fwords.objects.values_list('fword', flat=True))
    form = FwordsForm(instance=fword)
    context = {'form': form , 'edit': True}
    if request.method == 'POST':
        form = FwordsForm(request.POST, instance=fword)
        x = request.POST.get('fword')
        if x in  word :
            messages.info(request, 'it is already exists')
            return render(request, 'BlogApp/add-fword.html', context)
        else:
            form = FwordsForm(request.POST, instance=fword)
            form.is_valid()
            form.save()
            return redirect('Fwords')
    else:
        return render(request, 'BlogApp/add-fword.html', context)

#forbidden words
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delFword(request, fword_id):
    fword = Fwords.objects.get(id=fword_id)
    fword.delete()
    return redirect('Fwords')


#search function
def search(request):
    searchResults = Post.objects.none()
    if request.method == "POST":
        selected = request.POST.get("selected")
        posts = Post.objects.all()
        tags = Tag.objects.all()
        if not selected:
            context = {'noResult': True, 'searchValue': selected}
            return render(request,  'BlogApp/search.html', context)
        for tag in tags:
            if selected.lower() in tag.tag_item.lower():
                sel = Post.objects.filter(tag=tag)
                searchResults = searchResults | sel
        for post in posts:
            if selected.lower() in post.title.lower():
                sel = Post.objects.filter(title=post.title)
                searchResults = searchResults | sel
        if not searchResults:
            context = {'noResult': True, 'searchValue': selected}
        else:
            context = {'posts': searchResults, 'searchValue': selected}
        return render(request,  'BlogApp/search.html', context)
    else:
        context = {'noResult': True}
        return render(request,  'BlogApp/search.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def userMessage(request):
    all_messages = Message.objects.all()
    context = {'all_messages':all_messages}
    return render (request,'BlogApp/messages.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delMsg(request, msg_id):
        msg = Message.objects.get(id=msg_id)
        msg.delete()
        return redirect('messages')

# def error_404(request, exception):
#     data = {'name': 'ThePythonDjango.com'}
#     return render(request, 'BlogApp/NotFound.hml')