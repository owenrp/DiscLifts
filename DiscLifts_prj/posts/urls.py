from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^events/$', views.events, name='events'),
    url(r'^past_events/$', views.past_events, name='past_events'),
    url(r'^events/(?P<id>\d+)/$', views.event_posts, name='event_posts'),
    url(r'^events/posts/(?P<id>\d+)/$', views.posts, name='posts'),
    url(r'^add_post/(?P<event_id>\d+)/$', views.add_post, name='add_post'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^add_event/$', views.add_event, name='add_event'),
    url(r'^edit_post/(?P<post_id>\d+)/$', views.edit_post, name='edit_post'),
    url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post, name='delete_post'),
    url(r'^delete_event/(?P<event_id>\d+)/$', views.delete_event, name='delete_event'),
    url(r'^events_user/(?P<profile_id>\d+)/$', views.events_user, name='events_user'),
    url(r'^event_info/(?P<event_id>\d+)/$', views.event_info, name='event_info'),
    url(r'^edit_event/(?P<event_id>\d+)/$', views.edit_event, name='edit_event'),
    url(r'^how_it_works/$', views.how_it_works, name='how_it_works'),

]
