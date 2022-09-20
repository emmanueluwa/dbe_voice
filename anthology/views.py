from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
#count aggregation function of django orm
from django.db.models import Count
# Create your views here.

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        #if there is a given slug get the tag object
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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
    return render(request, 'anthology/post/list.html', {'posts': posts, 'tags': tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
            Post, 
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )
    #active comment list for post
    #leverage post object to retreive related comment objects
    comments = post.comments.filter(active=True)
    #for to add a comment
    form = CommentForm()
    #retrieving list of ids for tags of current post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]
    
    return render(request, 'anthology/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})


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

#commenting on post(post submission)
@require_POST #only allow post requests for this view
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    #variable used to store comment object when created
    comment = None
    #comment posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #create model instance(for comment object) but don't save it to db yet
        comment = form.save(commit=False)
        #assign post to the comment
        comment.post = post
        comment.save()
    return render(request, 'anthology/post/comment.html', {'post':post, 'form': form, 'comment': comment})

