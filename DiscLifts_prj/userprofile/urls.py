from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/(?P<profile_id>\d+)/$', views.profile, name='profile'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^delete_account/$', views.delete_profile_request, name='delete_profile_request'),

]
