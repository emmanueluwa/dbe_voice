from django import template
from ..models import Post
from django.db.models import Count

#tag retrieving total posts published

#used to register template tags and filters of app
register = template.Library()
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('anthology/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

#building a Queryset using annotate() function to get number of comments for each post
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
