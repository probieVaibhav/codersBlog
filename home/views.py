from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# for messages
from django.contrib import messages
# Create your views here.
# home function
def home(request):
    # filter posts according to views
    post = Post.objects.filter(views__gte = 5)
    return render(request, 'home/home.html', {'posts': post})

def about(request):
    # return HttpResponse('This is about....')
    return render(request, 'home/about.html')

def contact(request):
    # return HttpResponse('This is contact....')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        msg = request.POST['msg']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(msg)<5:
            messages.error(request, 'Please fill the form correctly...')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=msg)
            contact.save()
            messages.success(request, 'Your issue has been sent successfully...')
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['search']
    if len(query) > 1:
        if len(query) > 70:  
            search_post = Post.objects.none()
        else:
            search_post_title = Post.objects.filter(title__icontains=query)
            search_post_content = Post.objects.filter(content__icontains=query)
            search_post_author = Post.objects.filter(author__icontains=query)
            search_post = search_post_title.union(search_post_content, search_post_author)
        if search_post.count() == 0:
            messages.warning(request, 'No search results found. Please take a look on your query')
        return render(request, 'home/search.html', {'post': search_post, 'query': query})
    else:
        messages.error(request, 'Enter something, you want to explore')
        return redirect('/')
    # return HttpResponse('This is search')

# handle sign up functinality
def signup(request):
    if request.method == 'POST':
        username = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['c_pass']
        # check for errorneous inputs
        # username should under 4 - 8 characters
        if len(username) > 8 and len(username) < 4:
            messages.error(request, 'Username must be in between 4 to 8 characters')
            return redirect('/')
        # username must be and alphanumeric text
        if not username.isalnum():
            messages.error(request, 'Username must contain only numbers and characters')
            return redirect('/')
        # password and confirm password must be matched
        if pass1 != pass2:
            messages.error(request, 'Password and confirm password must match each other')
            return redirect('/')
        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "your Coder's Blog account has been created")
        return redirect('/')
    else:
        return HttpResponse('404 - Not Found')

# handle login functionality
def handlelogin(request):
    if request.method == 'POST':
        loginuser = request.POST['login_user']
        loginpass = request.POST['login_pass']
        # use authentication function to authenticate user
        user = authenticate(username=loginuser, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('/')
        else:
            messages.error(redirect, 'Invalid Credentials, please try agai')
            return redirect('/')

    return HttpResponse('404 - Not Found')

# handle logout functionality
def handlelogout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('/')
    # return HttpResponse('logout')