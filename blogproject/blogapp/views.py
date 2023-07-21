from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Blog, Comment
from .forms import BlogForm, CommentForm, RegisterForm
from django.contrib import auth


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        try:
            User.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {'error': 'email is already taken!'})
        except User.DoesNotExist:
            User.objects.create_user(request.POST['username'], password=request.POST['password'],
                                     email=request.POST['email'])
            # auth.login(request, user)
            return redirect('login')
    else:
        return render(request, 'signup.html', {'error': 'password does not match!'})


def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('blog_list')
        else:
            return render(request, 'login.html', {'error': 'email or password is incorrect!'})
    else:
        return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('blog_list')

def blog_list(request):
    blogs = Blog.objects.order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    comments = blog.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', blog_id=blog_id)

    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})

@login_required(login_url='/login')
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})

@login_required(login_url='/login')
def update_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)

    if blog.author != request.user:
        return redirect('blog_list')

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', blog_id=blog_id)
    else:
        form = BlogForm(instance=blog)

    return render(request, 'update_blog.html', {'form': form, 'blog': blog})

@login_required(login_url='/login')
def delete_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    if blog.author == request.user:
        blog.delete()
        return redirect('blog_list')
    else:
        return redirect('blog_list')

def search_blog(request):
    query = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=query))
    return render(request, 'blog_list.html', {'blogs': blogs})


