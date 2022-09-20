from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.

def post_list(request):
    post_list = Post.published.all()
    #3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        #if page does not exist go to last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'anthology/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
            Post, 
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )
    return render(request, 'anthology/post/detail.html', {'post': post})


"""
class based view for list view
"""
class PostListView(ListView):
    queryset = Post.published.all()
    #for the queryset results
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'anthology/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        #FORM was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{clean_data['name']} recomends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{clean_data['name']}\'s comments: {clean_data['comments']}"
            send_mail(subject, message, 'fulphrone@gmail.com', [clean_data['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'anthology/post/share.html', {'post':post, 'form':form, 'sent': sent})
