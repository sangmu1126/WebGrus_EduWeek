from webboard.models import Post, Comment
from django.core.paginator import Paginator
from webboard.forms import PostForm, CommentForm, UpdatePostForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404


def list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)  # 한 페이지에 5개씩 표시

    page = request.GET.get('page')  # query params에서 page 데이터를 가져옴
    items = paginator.get_page(page)  # 해당 페이지의 아이템으로 필터링

    context = {
        'posts': items
    }
    return render(request, 'webboard/list.html', context)


def detail(request, id):
    if id is not None:
        item = get_object_or_404(Post, pk=id)
        reviews = Comment.objects.filter(post=item).all()
        return render(request, 'webboard/detail.html', {'item': item, 'reviews': reviews})

    return HttpResponseRedirect('/list/')



def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)  # request의 POST 데이터들을 바로 PostForm에 담을 수 있습니다.
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return HttpResponseRedirect('/list/')  # 리스트 화면으로 이동합니다.
    form = PostForm()
    return render(request, 'webboard/create.html', {'form': form})


def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        item = get_object_or_404(Post, pk=request.POST.get('id'))
        password = request.POST.get("password", "")
        form = UpdatePostForm(request.POST, instance=item)  # NOTE: instance 인자(수정대상) 지정
        if form.is_valid() and password == item.password:  # 비밀번호 검증 추가
            item = form.save()
    elif 'id' in request.GET:
        item = get_object_or_404(Post, pk=request.GET.get('id'))
        form = PostForm(instance=item)
        form.password = ''  # password 데이터를 비웁니다.
        return render(request, 'webboard/update.html', {'form': form})

    return HttpResponseRedirect('/list/')  # 리스트 화면으로 이동합니다.


def delete(request, id):
    item = get_object_or_404(Post, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password'):
            item.delete()
            return redirect('list')  # 리스트 화면으로 이동합니다.

        return redirect('post-detail', id=id)  # 비밀번호가 입력되지 않으면 상세페이지로 되돌아감

    return render(request, 'webboard/delete.html', {'item': item})


def comment_create(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)  #
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return redirect('post-detail', id=post_id)  # 전화면으로 이동합니다.

    item = get_object_or_404(Post, pk=post_id)
    form = CommentForm(initial={'post': item})
    return render(request, 'webboard/comment_create.html', {'form': form, 'item':item})


def comment_delete(request, post_id, comment_id):
    item = get_object_or_404(Comment, pk=comment_id)
    item.delete()

    return redirect('post-detail', id=post_id)  # 전 화면으로 이동합니다.

