from tracemalloc import get_object_traceback
from django.shortcuts import render, redirect, get_object_or_404
# logout
# from group_four.forms import
# login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BlogPostForm, ProfileForm
from .models import BlogPost, Blog_Comment, Profile
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
# def index(request):
#     return render(request,'blog.html')
# dang ki


def Register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Mật khẩu không phù hợp!")
            return redirect('/register')

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')
    return render(request, "registration.html")
# login(dang nhap)


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Đã đăng nhập thành công")
            return redirect("/")
        else:
            messages.error(request, "Thông tin không hợp lệ")
        return render(request, 'login.html')
    return render(request, "login.html")


@login_required
def special(request):
    return HttpResponse('Bạn đã đăng nhập!')


def Logout(request):
    logout(request)
    messages.success(request, "Đăng xuất thành công")
    return redirect('/login')


def user_login(request):
    if request.method != 'POST':
        return render(request, 'login.html', {})
    username = request.POST.get('username')
    password = request.POST.get('password')

    if user := authenticate(username=username, password=password):
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse('TÀI KHOẢN KHÔNG HOẠT ĐỘNG')
    else:
        print('Ai đó đã cố gắng đăng nhập và không thành công!!')
        print(f"Username: {username} and Password: {password}")
        return HttpResponse("Chi tiết đăng nhập không hợp lệ!")
# @login_required(login_url = '/login')
# def add_blogs(request):
#     if request.method=="POST":
#         form = BlogPostForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             blogpost = form.save(commit=False)
#             blogpost.author = request.user
#             blogpost.save()
#             return redirect("draft")
#     else:
#         form=BlogPostForm()
#     return render(request, "add_new_blog.html", {'form':form})


@login_required(login_url='/login')
def add_blogs(request):
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            # sau khi tao ra bai viet mac dinh la draft
            blogpost.status = 'draft'
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "draft.html", {'obj': obj, 'alert': alert})
    else:
        form = BlogPostForm()
    return render(request, "add_new_blog.html", {'form': form})


def draft(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "draft.html", {'ups': posts})


class UpdatePost(UpdateView):
    model = BlogPost
    template_name = 'edit_blog.html'
    fields = ['title', 'slug', 'content', 'image']


def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter(status='published').order_by('-dateTime')
    return render(request, "blog.html", {'posts': posts})


def Delete_Blog_Post(request, post_id):
    posts = BlogPost.objects.get(id=post_id)
    if request.method == "POST":
        posts.delete()
        return redirect('draft')
    return render(request, 'delete_blog_post.html', {'posts': posts})
# class BlogDeleteView(DeleteView):
#     model = BlogPost
#     template_name = "delete_blog.html"
#     success_url = reverse_lazy("index")
# from django.shortcuts import get_object_or_404
# from .models import BlogPost
# def edit_blog(request, blog_id):
#     blog_post = get_object_or_404(BlogPost, pk=blog_id)
#     blog_post = BlogPost.objects.get(pk=blog_id)
#     return HttpResponse("{blog_id}")


def blogs_comments(request, slug):
    random = BlogPost.objects.order_by('?')[:2] 
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Blog_Comment.objects.filter(blog=post)
    if request.method == "POST":
        user = request.user
        content = request.POST.get('content', '')
        # blog_id =request.POST.get('blog_id','')
        comment = Blog_Comment(user=user, content=content, blog=post)
        comment.save()
    return render(request, "post.html", {'post': post, 'comments': comments,'random': random})


def view_blog(request):
    random = BlogPost.objects.order_by('-dateTime')[:3] 
    return render(request, 'post.html', {'random': random})
# profile_user


def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post': post})


def Profile(request):
    return render(request, 'profile.html')


def ViewDraft(reqeust):
    # tim tat ca cac bai` viet draft`
    draft_post = BlogPost.objects.filter(status='draft')
    return render(reqeust, "draft.html", {'draft_post': draft_post})


def push_draft(request, slug):
    # bien nay se tim tat ca doi tuong , neu khong co thi tra ve 404
    post_df = get_object_or_404(BlogPost, slug=slug)
    # gan cho no bien nay dc push len
    post_df.status = 'published'
    post_df.save()
    return redirect('/')


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        form = ProfileForm(data=request.POST,
                           files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, "profile.html")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form': form})


def search(request):
    searched = request.GET['searched']
    blogs = BlogPost.objects.filter(title__contains=searched)
    return render(request, "search.html", {'searched': searched, 'blogs': blogs})

# def Delete_comment(request, post_id):
#     posts = Blog_Comment.objects.get(id=post_id)
#     if request.method == "POST":
#         posts.delete()
#         blog_id = BlogPost.slug.slug
#         return redirect(f'/blog/{blog_id}')
#     return render(request, 'delete_comment.html', {'cmt': posts})
# class UpdatePost(UpdateView):
#     model = BlogPost
#     template_name = 'edit_blog.html'
#     fields = ['title', 'slug', 'content', 'image']
def Delete_comment(request, comment_id):
    comment = get_object_or_404(Blog_Comment, id=comment_id) 
    # Kiểm tra xem người dùng hiện tại có quyền xóa bình luận hay không
    if comment.user == request.user:
        # Xóa tất cả các reply thuộc bình luận
        # Xóa bình luận
        comment.delete() 
        blog_id = comment.blog.slug   
    return redirect(f'/blog/{blog_id}')