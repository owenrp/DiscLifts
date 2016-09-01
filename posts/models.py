import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.
class EventsManager(models.Manager):
    def future_events(self):
        future_events_qs = Events.objects.filter(end_date__gte=datetime.date.today()).order_by('start_date')
        return future_events_qs

    def past_events(self):
        past_events_qs = Events.objects.filter(end_date__lte=datetime.date.today()).order_by('start_date')
        return past_events_qs

class Events(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    location = models.CharField(max_length=120, null=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:event_posts', kwargs={'id': self.id})
        # return "/posts/events/%s" %(self.id)

    objects = EventsManager()


class Posts(models.Model):
    location = models.CharField(max_length=120)
    # The first element in each choices tuple is the actual value to be set on the model, and the second element is the
    # human-readable name
    lift_type = models.CharField(max_length=120,
                                 choices=(('I have space', 'I have space'), ('I need a ride', 'I need a ride')))
    leaving_time = models.CharField(max_length=120)
    spaces = models.IntegerField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    # Each post is linked to a User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    fulfilled = models.BooleanField(default=False)
    leaving_date = models.DateField(auto_now=False, auto_now_add=False)
    return_date = models.DateField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name_plural = "Posts"

    def get_absolute_url(self):
        return reverse('posts:posts', kwargs={'id': self.id})



class EventsManager(models.Manager):
    def future_events(self):
        future_events_qs = Events.objects.filter(end_date__gte=datetime.date.today()).order_by('start_date')
        return future_events_qs
