from django.contrib import admin
from .models import Events, Posts

# Register your models here.

class EventsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'updated']
    class Meta:
        model = Events

class PostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'location', 'leaving_time', 'lift_type', 'event', 'user']
    class Meta:
        model = Posts

# Adding the EventsAdmin below will cause the above class EventsAdmin list_display to show up in the admin site
admin.site.register(Events, EventsAdmin)
admin.site.register(Posts, PostsAdmin)
