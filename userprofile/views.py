from __future__ import absolute_import

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from .models import UserProfile
from .forms import UserProfileForm, UserForm
from posts.models import Posts


# from ..posts.forms import AddPostForm, AddEventForm

@login_required
def profile(request, profile_id):
    user_django_inst = get_object_or_404(User, id=profile_id)
    user_profile = get_object_or_404(UserProfile, user=profile_id)
    current_user_id = request.user.id
    form = UserProfileForm(initial={'email_notification': user_profile.email_notification})

    user_posts_qs = Posts.objects.all().filter(user_id=current_user_id)
    user_posts_qs_paginator = create_pagination(request, user_posts_qs, 5)

    context = {
        'user_profile': user_profile,
        'current_user_id': current_user_id,
        'user_posts_queryset': user_posts_qs_paginator,
        'user_django_inst': user_django_inst,

    }
    return render(request, 'userprofile/profile.html', context)


@login_required
def update_profile(request):
    user_instance = get_object_or_404(UserProfile, user=request.user)
    user_django_inst = get_object_or_404(User, id=user_instance.user_id)

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_profile_form.is_valid() and user_form.is_valid():
            # The save(commit=False) part allows us to add data to other fields before the whole form is saved. In this
            # case the user has to be associated with a post which is done automatically with request.user which is
            # assigned to the user field in the model Posts

            email_notification = user_profile_form.cleaned_data['email_notification']
            user_instance.email_notification = email_notification
            user_instance.save()

            user_django_inst.first_name = user_form.cleaned_data['first_name']
            user_django_inst.last_name = user_form.cleaned_data['last_name']
            user_django_inst.save()

            return redirect(user_instance)

    else:
        user_profile_form = UserProfileForm(instance=user_instance)
        user_form = UserForm(instance=user_django_inst)

    context = {
        'user_profile_form': user_profile_form,
        'user_form': user_form,
    }

    return render(request, 'userprofile/update_profile.html', context)


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


# Sends an email to the admin requesting the deletion of the users account.
def delete_profile_request(request):
    current_user_id = request.user.id
    user_profile = get_object_or_404(UserProfile, user=current_user_id)
    user_django_inst = get_object_or_404(User, id=current_user_id)

    message = 'Current user id: ' + str(current_user_id) + ' has requested a profile delete'
    send_mail(
                'New profile delete request from DiscLifts.com',
                message,
                user_django_inst.email,
                ['disclifts@gmail.com'],
                fail_silently=False,
            )
    return redirect(user_profile)
