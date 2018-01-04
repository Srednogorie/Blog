from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
import redis
import json
from taggit.models import Tag
from .models import Post, Comment, Email
from .forms import EmailPostForm, CommentForm, EmailSign, SearchForm


# Create your views here.
# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 1)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    for post in posts:
        comments = post.comments.filter(active=True)

    for look in posts:
        total_views = r.get('post:{}:views'.format(look.id))

    return render(request, 'blog/post/list.html', {'page':page, 'posts': posts, 'tag': tag, 'comments': comments,
                                                   'total_views': total_views})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # increment total image views by 1
    total_views = r.incr('post:{}:views'.format(post.id))

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Get values for Json Response
            name = new_comment.name
            body = new_comment.body
            # Save the comment to the database
            new_comment.save()
            created = new_comment.created.strftime("%b. %-d, %Y, %H:%M")
            comment_form = CommentForm()
            up_comment = comments.count()
            data = {'up_comment': up_comment, 'name': name, 'body': body, 'created': created, 'active_tab': 'myanchor',
                    'total_views': total_views, 'success': True}
            return JsonResponse(data)

            #return render(request, 'blog/post/detail.html',
                          #{'new_comment': new_comment,
                           #})
        else:
            data = {'success': False, 'errors': comment_form.errors.as_json()}
            return JsonResponse(data)

    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form,
                                                     'total_views': total_views})


def post_share(request):
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            #cd = form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            company = form.cleaned_data['company']
            comments = form.cleaned_data['comments']
            # ... send email
            subject = 'Someone want to tell you something'
            message = comments + "\n" + name + "\n" + company + "\n" + email
            send_mail(subject, message, 'djangoenv7@gmail.com', ['akrachunov@gmail.com'])
            sent = True
            form = EmailPostForm()
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/contact.html', {'form': form, 'sent': sent})


def email_sign(request):
    if request.method == 'POST':
        email_form = EmailSign(data=request.POST)
        if email_form.is_valid():
            new_email = email_form.save(commit=False)
            new_email.save()
            json_email = Email.objects.last()
            js_email = serializers.serialize('json', [ json_email, ])
            return JsonResponse({'success': True, 'js_email': js_email,
                                 'message': 'Your e-mail has been added to the list!', })
        else:
            data = {'success': False, 'errors': email_form.errors.as_json()}
            return JsonResponse(data)


class Search(View):
    #Search all tweets with query /search/?query=<query> URL
    def get(self, request):
        form = SearchForm(request.GET)
        posts = Post.objects.all()
        for post in posts:
            comments = post.comments.filter(active=True)
            if form.is_valid():
                query = form.cleaned_data['query']
                posts = Post.objects.filter(body__icontains=query)
                return render(request, 'blog/post/search_results.html', {'posts': posts, 'query': query,
                                                                         'comments': comments})
            else:
                HttpResponseRedirect("/search")
