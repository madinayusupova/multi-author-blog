from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm, EmailPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from slugify import slugify as transliterate






@login_required()
def create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.slug = slugify(transliterate(post.title))
        post.save()
        
        return redirect('blog:post_list')
    return render(request, 'blog/post/create.html', {'form': form})

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

@login_required()
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug= post, status= 'published', publish__year= year, publish__month= month, publish__day= day)
    comments = post.comments.filter(active = True)
    new_comment = None
    total_likes = post.total_likes()
    if request.method == "POST":
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment, 'total_likes':total_likes})


@login_required()
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = 'published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}({cd['email']}), recommends you reading {post.title}"
            message = f"Read '{post.title}' at {post_url} where {cd['name']} comments {cd['comments']}"
            send_mail(subject, message, 'admin@gmail.com', [cd['to']])
            sent =True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})





@login_required
def UpdatePostView(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = 'published') 
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post1 = form.save(commit=False)
                post1.status = 'published'
                post1.author = request.user
                post1.slug = post.slug
                post1.save()
                return render(request, 'blog/post/detail.html', {'post': post})
            else:
                form = PostForm(instance=post)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post/update.html', {'post': post, 'form':form,})
    else:
        return render(request, 'blog/post/ups.html')



@login_required
def DeletePostView(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = 'published')
    if request.user == post.author:
        if request.method == "POST":
            post.delete_post()
            return redirect('blog:post_list')

        return render(request, 'blog/post/delete.html', {'post': post})
    else:
        return render(request, 'blog/post/ups.html')




def LikeView(request, post_id):
    post = get_object_or_404(Post, id = post_id, status='published')
    post.likes.add(request.user)
    # return HttpResponseRedirect(reverse('post_detail', kwargs={'year':post.publish.year, 'month':post.publish.month, 
                                                                # 'day':post.publish.day, 'post':post.slug}))
    return render(request, 'blog/post/detail.html', {'post': post, 'total_likes': post.total_likes})



def search(request):
    query = request.GET.get('q')
    object_list = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    if object_list:
        return render(request, 'blog/post/search.html', {'object_list':object_list , "query":query})

    else:
        text = "Sorry, nothing found"
        return render(request, 'blog/post/search.html', {'object_list':object_list, 'text':text, "query":query})



