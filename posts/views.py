from django.shortcuts import render, redirect, get_object_or_404
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
        return render(request, 'posts/create.html', {'form':form })

def update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        # 실제 DB에 수정 반영
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        # page redirect
        form = PostForm(instance=post)
        return render(request, 'posts/create.html', {'form': form })

@require_safe
def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('posts:index')