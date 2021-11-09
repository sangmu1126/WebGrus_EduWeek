from django import forms
from webboard.models import Post, Comment
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'password']
        labels = {
            'title': _('제목'),
            'content': _('내용'),
            'password': _('게시물 비밀번호'),
        }
        help_texts = {
            'title': _('제목을 입력해주세요.'),
            'content': _('내용을 입력해주세요.'),
            'password': _('비밀번호를 입력해주세요.'),
        }
        error_messages = {
            'title': {
                'max_length': _("제목이 너무 깁니다. 30자 이하로 해주세요."),
            },
            'password': {
                'max_length': _("비밀번호가 너무 깁니다. 20자 이하로 해주세요."),
            },
        }


class UpdatePostForm(PostForm):
    class Meta:
        model = Post
        exclude = ['password']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'post']
        labels = {
            'comment': _('댓글'),
        }
        widgets = {
            'post': forms.HiddenInput(),
        }
        help_texts = {
            'comment': _('댓글을 입력하세요.'),
        }
