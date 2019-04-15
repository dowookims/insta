from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

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
    

def signup(request):
    if request.method =="POST":
        # User Signup
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:index')
        
    else:
        # Put userinfo
        form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
        

def people(request, username):
    # 사용자에 대한 정보를 넣을 예정.
    # 하나는 settings.AUTH_USER_MODEL =  django.conf
    # 둘째는 get_user_model() = django.contrib.auth
    # 셋째는 User = django.contrib.auth.models
    # 장고의 관례의 따라 3번은 존재하나 안쓰는게 좋고 둘중에 하나를 써야 하는데
    # 강사님의 경우 1은 모델을 정의할 때, 2는 뷰를 만들 때 사용한다.
    # lastest 인 get_user_model을 자주 쓸 생각을 하자 ㅇㅇ..
    people = get_object_or_404(get_user_model(), username=username)
    return  render(request, 'accounts/people.html', {'people': people})