from django.shortcuts import render, redirect
from . forms import PostForm
from . models import Post

# Create your views here.


def create(request):
    if request.method == "POST":
        # written post apply on DB
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:create')
        else:
            pass
        
    else: #GET
        # Show Post writing form
        form = PostForm()
        return render(request, 'posts/create.html', {'form':form})