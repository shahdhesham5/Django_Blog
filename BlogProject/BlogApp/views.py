from multiprocessing import context
from tokenize import group
from django.http import HttpResponse
from django.shortcuts import render,redirect
from BlogApp.decorators import unauthenticated_user,allowed_users, admin_only
from BlogApp.models import Category
from .forms import CreateUserForm,CategoryForm  #the modified UserCreationForm
#authentication
from django.contrib.auth.forms import UserCreationForm #replaced by CreateUserForm 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User #User model to access users and admins

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
            group = Group.objects.get(name='normaluser')
            user.groups.add(group)
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
        #if the user exists and the password matches direct them to home
        if user is not None:
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
    context ={'users' : users}
    return render(request,'BlogApp/showusers.html', context)


#home
def home(request):
    all_categories = Category.objects.all()
    context = {'all_categories':all_categories}
    return render(request, 'BlogApp/home.html',context)

#Post details
def post(request,post_id):

    return render(request, 'BlogApp/post.html')
    
#posts
@login_required(login_url='login')
def posts(request):
    return render(request, 'BlogApp/posts.html')

#manageblog
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manageBlog(request):
    return render(request,'BlogApp/manageblog.html')

#show categories
def categories(request):
    all_categories = Category.objects.all()
    context = {'all_categories':all_categories}
    return render (request,'BlogApp/categories.html', context)
<<<<<<< HEAD
=======


#add category
def addCat(request):
    if request.method == 'POST': #if submited, check the inputs, validate form, then save
        form = CategoryForm(request.POST)
        all_categories = Category.objects.all()
        if request.POST in all_categories:
            return HttpResponse("exists")
        else:
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
>>>>>>> c412737e6ea25e813494d9e1b7f467cc49ebfd89
