from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from . forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from . models import Profile

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
        
    else:
        form = AuthenticationForm()
        return render(request, "accounts/login.html", {'form': form})

def logout(request):
    auth_logout(request)
    return redirect("posts:index")
    

def signup(request):
    if request.method =="POST":
        # User Signup
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:index')
        
    else:
        # Put userinfo
        form = CustomUserCreationForm()
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
    profile = Profile.objects.get(user_id=people.id)
    context = {
        "people": people,
        "profile": profile
    }
    return  render(request, 'accounts/people.html', context)
    
# 회원 정보 변경 action
# 편집 & 반영
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(instance=request.user, data = request.POST)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
        return redirect('people', user.username)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 1. instance에 넣어줄 정보가 있는 User가 있고, 없는 User도 있다.
        # 밑에 있는 친구는 튜플을 반환하는데 profile 객체가 있으면 profile을, 
        # 없으면 만들어야 하므로 created가 되어야 한다.
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)
        # password_change_form = PasswordChangeForm(request.user)
        context = {
            'user_change_form': user_change_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/update.html', context)
        

@login_required
@require_http_methods(['GET', 'POST'])
def delete(request):
    if request.method =="POST":
        request.user.delete()
        return redirect('posts:index')
    return render(request, 'accounts/delete.html')


@login_required
@require_http_methods(['GET', 'POST'])
def password(request):
    if request.method == "POST":
        pw_change_form = PasswordChangeForm(request.user, request.POST)
        if pw_change_form.is_valid():
            user = pw_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', user.username)
        else:
            pw_change_form = PasswordChangeForm(request.user)
            return render(request, 'accounts/password.html', {"pw_change_form":pw_change_form})
    else:
        pw_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password.html', {"pw_change_form":pw_change_form})

@login_required
def follow(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    
    # 만약 현재 유저가 해당 유저를 이미 팔로우 하고 있었으면
    # => 팔로우를 취소
    # 아니면
    # => 팔로우를 함.
    if request.user in person.follows.all():
        person.follows.remove(request.user)
    else:
        person.follows.add(request.user)
    return redirect("people", person.username)
    