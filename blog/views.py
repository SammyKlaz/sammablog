from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Post, Comment, Profile, ContactMessage
from .forms import CommentForm, PostForm, ProfileForm, ContactForm


def home(request):

    posts = Post.objects.all().order_by(
        '-created_at'
    )

    post_count = posts.count()

    context = {
        'posts': posts,
        'post_count': post_count
    }

    return render(
        request,
        'blog/home.html',
        context
    )

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    saved_posts = request.session.get('saved_posts', [])

    is_saved = post.id in saved_posts

    if request.method == 'POST' and request.user.is_authenticated:
    
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.post = post

            comment.user = request.user

            comment.save()

            return redirect('post_detail', slug=post.slug)

    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'is_saved': is_saved
    })

def about(request):
    
    return render(request, 'blog/about.html')

def contact(request):

    submitted = False

    if request.method == 'POST':

        form = ContactForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            submitted = True

    else:

        form = ContactForm()

    return render(
        request,
        'blog/contact.html',
        {
            'form': form,
            'submitted': submitted
        }
    )


def save_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    saved_posts = request.session.get('saved_posts', [])

    if post.id not in saved_posts:
        saved_posts.append(post.id)

    request.session['saved_posts'] = saved_posts

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def saved_posts(request):
    saved_posts = request.session.get('saved_posts', [])

    posts = Post.objects.filter(id__in=saved_posts)

    return render(request, 'blog/saved_posts.html', {
        'posts': posts
    })


def remove_saved_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    saved_posts = request.session.get('saved_posts', [])

    if post.id in saved_posts:
        saved_posts.remove(post.id)

    request.session['saved_posts'] = saved_posts

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def like_post(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.user in post.likes.all():

        post.likes.remove(request.user)

    else:

        post.likes.add(request.user)

    return redirect('post_detail', slug=post.slug)




@login_required
def create_post(request):

    if not request.user.profile.is_author:
        return redirect('profile')

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user

            post.save()

            return redirect(
                'post_detail',
                slug=post.slug
            )

    else:

        form = PostForm()

    return render(
        request,
        'blog/create_post.html',
        {
            'form': form
        }
    )
@login_required
def profile(request):

    profile = request.user.profile

    posts = request.user.posts.all()

    post_count = posts.count()


    total_likes = 0

    total_comments = 0

    for post in posts:
        total_likes += post.likes.count()
        total_comments += post.comments.count()

    context = {
        'user': request.user,
        'profile': profile,
        'posts': posts,
        'post_count': post_count,
        'total_likes': total_likes,
        'total_comments': total_comments
    }

    return render(
        request,
        'blog/profile.html',
        context
    )


@login_required
def edit_profile(request):

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=request.user.profile
        )

    return render(request, 'blog/edit_profile.html', {'form': form})

def author_profile(request, username):

    author = get_object_or_404(
        User,
        username=username
    )

    posts = author.posts.all()

    post_count = posts.count()

    context = {
        'author': author,
        'profile': author.profile,
        'posts': posts,
        'post_count': post_count
    }

    return render(
        request,
        'blog/author_profile.html',
        context
    )

@login_required
def edit_post(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect(
                'post_detail',
                slug=post.slug
            )

    else:

        form = PostForm(
            instance=post
        )

    return render(
        request,
        'blog/edit_post.html',
        {
            'form': form,
            'post': post
        }
    )

@login_required
def delete_post(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':

        post.delete()

        return redirect('profile')

    return render(
        request,
        'blog/delete_post.html',
        {
            'post': post
        }
    )

@login_required
def request_author(request):

    profile = request.user.profile

    profile.author_request = True

    profile.save()

    return redirect('profile')