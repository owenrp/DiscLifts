from __future__ import absolute_import
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from .models import Events, Posts, User
from .forms import AddPostForm, AddEventForm, EditPostForm
from userprofile.models import UserProfile


def index(request):
    # Home page

    # title is an example of a view function variable
    title = 'Welcome'
    if request.user.is_authenticated():
        title = 'Welcome %s' % (request.user)

    # A queryset of events filtered by the end_date being greater than today, and then ordered by the start_date
    # [:5] limits the queryset to show the first 5 results
    queryset = Events.objects.filter(end_date__gte=datetime.date.today()).order_by('start_date')[:5]
    context = {
        # These are template context variables
        'title': title,
        'queryset': queryset,
    }
    return render(request, 'posts/index.html', context)


def events(request):
    # Events page - shows all events
    # Query set of the posts to show how many posts are for each event
    posts_queryset = Posts.objects.all()
    events_queryset = Events.objects.filter(end_date__gte=datetime.date.today()).order_by('start_date')

    events_qs_paginator = create_pagination(request, events_queryset, 10)

    context = {
        # These are template context variables
        'posts_queryset': posts_queryset,
        'events_queryset': events_qs_paginator,
    }
    return render(request, 'posts/events.html', context)


def event_posts(request, id):
    # Event posts page, shows all the posts for the associated event.
    # id is being passed from the url to event_posts as a kwarg

    # Events.objects.get(id=id) returns the title of the event of the passed id
    event_title = get_object_or_404(Events, id=id)

    # The .filter(event=event_title) filters only posts that have the Posts.event equal to the event_title
    posts_queryset = Posts.objects.all().filter(event_id=event_title.id)
    current_user = request.user
    if (posts_queryset.count() == 0):
        no_posts = True
    else:
        no_posts = False

    posts_qs_paginator = create_pagination(request, posts_queryset, 10)

    context = {
        'posts_queryset': posts_qs_paginator,
        # {{ event_id }} is used in the template event_posts.html
        'event_id': event_title,
        'no_posts': no_posts,
        'current_user': current_user,

    }
    return render(request, 'posts/event_posts.html', context)


def posts(request, id):
    # Individual post page with information about a lift.
    posts_instance = get_object_or_404(Posts, id=id)
    current_user_id = request.user.id
    context = {
        'posts_instance': posts_instance,
        'current_user_id': current_user_id,
    }
    return render(request, 'posts/posts.html', context)


@login_required
def add_post(request, event_id=None):
    if request.method == 'POST':
        # The view will once again create a form instance and populate it with data from the request, binding the form.
        add_post_form = AddPostForm(request.POST or None)

        if add_post_form.is_valid():
            # The save(commit=False) part allows us to add data to other fields before the whole form is saved. In this
            # case the user has to be associated with a post which is done automatically with request.user which is
            # assigned to the user field in the model Posts
            form_instance = add_post_form.save(commit=False)
            # The add_post_form.save() returns the saved object, so the fields of the posts can be accessed with
            # form_instance.[field_name]
            form_instance.user = request.user
            form_instance.save()
            event_inst = Events.objects.get(id=form_instance.event_id)

            # Upon successfully creating a new post, this will return the events_post page
            return redirect(event_inst)

    else:
        # If the add_post view is called with an event_id argument != None, it will prepopulate the form with the
        # initial value of 'event' with the event
        if (event_id != None):
            event_inst = Events.objects.get(id=event_id)
            add_post_form = AddPostForm(initial={'event': event_inst,
                                                 'leaving_date': event_inst.start_date,
                                                 'return_date': event_inst.end_date})
        else:
            add_post_form = AddPostForm()

    # The add_post_form event field only shows events that are in the future
    add_post_form.fields['event'].queryset = Events.objects.filter(end_date__gte=datetime.date.today()).order_by(
        'start_date')

    context = {
        'add_post_text': 'Please enter details below',
        'add_post_form': add_post_form,
    }

    return render(request, 'posts/add_post.html', context)


@login_required
def add_event(request):
    if request.method == 'POST':
        add_event_form = AddEventForm(request.POST)

        if add_event_form.is_valid():
            form_instance = add_event_form.save(commit=False)
            form_instance.user = request.user
            event_title = add_event_form.cleaned_data['title']
            form_instance.save()
            event_inst = Events.objects.get(title=event_title)

            # Upon successfully adding an event, this will return the posts page of the new event. The
            # redirect(event_inst) uses the get_absolute_url method of the Events model to return the correct events_
            # posts page
            return redirect(event_inst)
    else:
        add_event_form = AddEventForm()

    context = {
        'add_event_form': add_event_form,
        'add_event_text': 'Please enter event details below',
    }
    return render(request, 'posts/add_event.html', context)


def edit_post(request, post_id):
    if request.method == 'POST':
        add_post_form = EditPostForm(request.POST)
        post_inst = get_object_or_404(Posts, id=post_id)
        # user_inst = UserProfile.objects.get(user_id=request.user.id)
        if add_post_form.is_valid():
            # form_instance = add_post_form.save(commit=False)
            post_inst.lift_type = add_post_form.cleaned_data['lift_type']
            post_inst.location = add_post_form.cleaned_data['location']
            post_inst.leaving_date = add_post_form.cleaned_data['leaving_date']
            post_inst.leaving_time = add_post_form.cleaned_data['leaving_time']
            post_inst.return_date = add_post_form.cleaned_data['return_date']
            post_inst.fulfilled = add_post_form.cleaned_data['fulfilled']
            post_inst.spaces = add_post_form.cleaned_data['spaces']
            post_inst.event = add_post_form.cleaned_data['event']
            post_inst.save()

            return redirect(post_inst)

    else:
        post_inst = get_object_or_404(Posts, pk=post_id)
        # This loads a form with an instance of the post we get from the id passed in the url
        add_post_form = EditPostForm(instance=post_inst)

    event_inst = get_object_or_404(Events, pk=post_inst.event_id)
    # print(event_inst.end_date)
    # If post is for event in the future all the events show up in the event drop down
    if event_inst.end_date > datetime.date.today():
        add_post_form.fields['event'].queryset = Events.objects.filter(end_date__gte=datetime.date.today()).order_by(
            'start_date')

    context = {
        'post_form': add_post_form,
        'page_title': 'Edit post',
    }
    return render(request, 'posts/edit_post.html', context)


def past_events(request):
    # Events page - shows all events
    # Query set of the posts to show how many posts are for each event
    posts_queryset = Posts.objects.all()
    events_queryset = Events.objects.filter(end_date__lte=datetime.date.today()).order_by('start_date')

    events_qs_paginator = create_pagination(request, events_queryset, 15)

    context = {
        # These are template context variables
        'posts_queryset': posts_queryset,
        'events_queryset': events_qs_paginator,
    }
    return render(request, 'posts/past_events.html', context)


@login_required
def delete_post(request, post_id):
    post_instance = get_object_or_404(Posts, id=post_id)
    context = {}
    if request.user.id == post_instance.user_id:
        event_instance_of_post = get_object_or_404(Events, id=post_instance.event.id)
        post_instance.delete()
    else:
        # If current user is not the one who created the post the page will redirect to the post page
        return redirect(post_instance)

    return redirect(event_instance_of_post)


# Delete event view redirects to the events page
@login_required
def delete_event(request, event_id):
    event_inst = Events.objects.get(id=event_id)
    event_inst_user = event_inst.user_id
    # Only user who created event can delete it
    if request.user.id == event_inst_user:
        event_inst.delete()

    return redirect('/events/')


def events_user(request, profile_id):
    current_user = request.user
    event_queryset = Events.objects.all().filter(user_id=profile_id)
    user_inst = get_object_or_404(User, id=profile_id)

    event_qs_paginator = create_pagination(request, event_queryset, 10)
    context = {
        'event_queryset': event_qs_paginator,
        'user_inst': user_inst,
        'current_user': current_user,
    }
    return render(request, 'posts/events_user.html', context)


@login_required
def edit_event(request, event_id):
    if request.method == 'POST':
        event_inst = get_object_or_404(Events, id=event_id)
        edit_event_form = AddEventForm(request.POST)
        if edit_event_form.is_valid():
            event_inst.title = edit_event_form.cleaned_data['title']
            event_inst.content = edit_event_form.cleaned_data['content']
            event_inst.location = edit_event_form.cleaned_data['location']
            event_inst.start_date = edit_event_form.cleaned_data['start_date']
            event_inst.end_date = edit_event_form.cleaned_data['end_date']
            event_inst.save()
            return redirect(event_inst)

    else:
        event_inst = get_object_or_404(Events, id=event_id)
        edit_event_form = AddEventForm(instance=event_inst)

    context = {
        'event_inst': event_inst,
        'edit_event_form': edit_event_form,
        'page_title': 'Edit event',
    }
    return render(request, 'posts/edit_event.html', context)


def event_info(request, event_id):
    event_inst = get_object_or_404(Events, id=event_id)
    context = {
        'event_inst': event_inst,
    }
    return render(request, 'posts/event_info.html', context)


def how_it_works(request):
    context = {}
    return render(request, 'posts/how_it_works.html', context)


def create_pagination(request, queryset, item_limit):
    paginator = Paginator(queryset, item_limit)

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    return queryset
