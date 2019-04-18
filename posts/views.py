from django.shortcuts import render, redirect, get_object_or_404
from . forms import PostForm, CommentForm
from . models import Post, Comment
from django.views.decorators.http import require_safe
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q

# Create your views here.

@login_required
def index(request):
    # Show all posts
      # 뭔가
    posts = Post.objects.filter(Q(user__in=request.user.followings.all()) | Q(user=request.user)).order_by('-id')
    print(posts.query)
    form = CommentForm()
    return render(request, 'posts/index.html', {'posts': posts, 'form': form})


@login_required
def create(request):
    if request.method == "POST":
        # written post apply on DB
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
        
    else: #GET
        # Show Post writing form
        form = PostForm()
        actions = 'create'
        return render(request, 'posts/create.html', {'form':form })

def update(request, id):
    post = get_object_or_404(Post, pk=id)
    
    if post.user != request.user:
        return redirect('posts:index')
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
    if post.user != request.user:
        return redirect('posts:index')    
    post.delete()
    return redirect('posts:index')

@login_required
def like(request, id):
    # 1. like를 추가할 포스트를 가져옴
    post = get_object_or_404(Post, id=id)
    # 2. if user already push like buttons, remove like else add like
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:index')


@login_required
@require_http_methods(["POST"])
def comment_create(request, id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        post = Post.objects.get(pk=id)
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect('posts:index')


@login_required
def comment_delete(request, id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('posts:index')
    comment.delete()
    return redirect('posts:index')