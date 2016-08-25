from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contact/$', views.contact_page, name='contact_page'),
    url(r'^termsandconditions/$', views.tnc, name='tnc'),
    url(r'^privacypolicy/$', views.privacy_policy, name='privacy_policy'),
]
