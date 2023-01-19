from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def contact(request):
    if request.method=="POST":
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone']
        content= request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<1:
            messages.error(request,'Please fill the form correctly.')
        else:
            contact= Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,'Your message has been sent successfully.')
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query=request.GET['query']
    if len(query)>70:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)

    if len(allPosts) == 0:
            messages.warning(request,'No search result found. Please refine your query.')
    params = {'allPosts':allPosts, 'query': query}
    return render(request, 'home/search.html',params)

def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        check = request.POST['check']
        # Check for errorneous inputs
        if len(username)>20:
            messages.error(request,'Entered Username is too long')
            return redirect('home')
        if not username.isalnum():
            messages.error(request,'Username should only contain letters and numbers')
            return redirect('home')
        if password1!=password2:
            messages.error(request,'Entered Password Do not match')
            return redirect('home')
        # Create the user:
        myuser = User.objects.create_user(username,email,password1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Your Account has been created successfully. Now you can Login to your account.")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername,password =loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')