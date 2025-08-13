
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import RegisterForm, PostForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User

@login_required(login_url="/login")
def view_profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, 'main/profile.html', {"profile": profile, "user_obj": user})

@login_required(login_url="/login")
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Always sync superuser to admin role
    if request.user.is_superuser and profile.role != 'admin':
        profile.role = 'admin'
        profile.save()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        # Only admin/superuser can change role
        if not request.user.is_superuser and profile.role != 'admin':
            form.fields['role'].disabled = True
        if form.is_valid():
            # If superuser, always set role to admin
            instance = form.save(commit=False)
            if request.user.is_superuser:
                instance.role = 'admin'
            instance.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)
        if not request.user.is_superuser and profile.role != 'admin':
            form.fields['role'].disabled = True
    return render(request, 'main/edit_profile.html', {"form": form})

# Admin-only: edit any user's profile and role
@login_required(login_url="/login")
def admin_edit_profile(request, username):
    if not request.user.is_superuser:
        return redirect('home')
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    # Always sync superuser to admin role
    if user.is_superuser and profile.role != 'admin':
        profile.role = 'admin'
        profile.save()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            if user.is_superuser:
                instance.role = 'admin'
            instance.save()
            return redirect('view_profile_other', username=user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'main/edit_profile.html', {"form": form, "user_obj": user})

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        # Handle post deletion
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        # Only admin and post author can delete
        if post and (post.author == request.user or getattr(request.user.profile, 'role', None) == 'admin'):
            post.delete()
            return redirect('home')

        # Handle comment submission
        comment_post_id = request.POST.get("comment-post-id")
        content = request.POST.get("content")
        if comment_post_id and content:
            post = Post.objects.filter(id=comment_post_id).first()
            if post and post.author.is_superuser:
                comment = Comment(
                    author=request.user,
                    post=post,
                    content=content
                )
                comment.save()
                return redirect('home')

    return render(request, 'main/home.html', {
        "posts": posts,
        "comment_form": comment_form,
    })

# Superuser-only view to see only their posted comments
@login_required(login_url="/login")
def superuser_comments(request):
    if not request.user.is_superuser:
        return redirect('home')
    from .models import Comment
    comments = Comment.objects.filter(author=request.user)
    return render(request, 'main/superuser_comments.html', {"comments": comments})

@login_required(login_url="/login") 
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()
        
    return render(request, 'main/create_post.html', {"form": form})

# Delete comment view
@login_required(login_url="/login")
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Only admin, moderator, or comment author can delete
    user_role = getattr(request.user.profile, 'role', None)
    if user_role in ['admin', 'moderator'] or request.user == comment.author:
        comment.delete()
    next_url = request.GET.get('next', reverse('home'))
    return redirect(next_url)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Only admin and post author can delete
    if request.user == post.author or getattr(request.user.profile, 'role', None) == 'admin':
        post.delete()
    return redirect('home')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')

    else:
        form = RegisterForm()
        
    return render(request, 'registration/sign_up.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/login')
    