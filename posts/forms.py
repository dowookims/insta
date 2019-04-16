from django import forms
from . models import Post, Comment

# Post라는 모델을 조작 할 수 있는 PostModelForm 정의
class PostForm(forms.ModelForm):
    # 1. 이 폼이 어떤 input field를 가지는지
    # 2. 해당 input field의 속성을 추가
    content = forms.CharField(widget = forms.Textarea(attrs={
        'placeholder': '오늘은 무엇을 하셨나요?'
    }), label='')
    
    class Meta:
        model = Post
        # fields = "__all__" # __all__ : 가지고 있는 모든 필드(지금은 content가 적으나 나중에는 모델)
        fields = ['content', 'image']
        

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': '댓글을 입력하세요.',
        'class': 'form-control d-inline col-10'
    }), label='')
    
    class Meta:
        model = Comment
        fields = ['content']
      