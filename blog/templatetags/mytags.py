from django import template
import re
from ..models import Post, Comment
from django.db.models import Count
from ..forms import EmailSign, SearchForm


register = template.Library()

@register.simple_tag
def active(request, pattern):
   if re.search(pattern, request.path):
      return 'active'
   return ''


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/post/latest_comments.html')
def show_latest_comments(count=3):
    latest_comments = Comment.objects.order_by('-created')[:count]
    return {'latest_comments': latest_comments}


@register.assignment_tag
def get_most_commented_posts(count=3):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.inclusion_tag('blog/post/email_list.html')
def email_sign_form():
    email_form = EmailSign()
    return {'email_form': email_form}

@register.inclusion_tag('blog/post/search.html')
def search_form():
    search_form = SearchForm()
    return {'search_form': search_form}
