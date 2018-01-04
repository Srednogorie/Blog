from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from .views import Search


urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<post>[-\w]+)/$',
        views.post_detail, name='post_detail'),
    url(r'^contact/$', views.post_share, name='contact'),
    url(r'^about/$', TemplateView.as_view(template_name='blog/post/about.html')),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^sign/$', views.email_sign, name='email_sign'),
    url(r'^search/$', Search.as_view(), name='search'),
]