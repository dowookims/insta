from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def login(request):
    if request.method =="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # next = 정의 되어 있으면, 해당 하는 url로 리다이렉트
            # 정의되어 있지 않으면 posts의 index로 리다이렉트
            # 로그인 되어 있지 않을시 로그인으로 이동 한 후 로그인 이후에 추가적인 행동을 하게 리다이렉팅 하는 경우가 많다
            return redirect(request.GET.get('next') or 'posts:index')
        
    else:
        form = AuthenticationForm()
        return render(request, "accounts/login.html", {'form': form})

def logout(request):
    auth_logout(request)
    return redirect("posts:index")