from django.shortcuts import render, redirect
from . forms import PostForm
from . models import Post
from django.views.decorators.http import require_safe

# Create your views here.

def index(request):
    # Show all posts
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

def create(request):
    if request.method == "POST":
        # written post apply on DB
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
        else:
            pass
        
    else: #GET
        # Show Post writing form
        form = PostForm()
        actions = 'create'
        return render(request, 'posts/create.html', {'form':form, 'actions':actions })

def update(request, id):
    post = Post.objects.get(pk=id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = PostForm(instance=post)
        actions = 'edit'
        return render(request, 'posts/create.html', {'form': form, 'actions' : actions})

@require_safe
def delete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect('posts:index')