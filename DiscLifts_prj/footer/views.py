from __future__ import absolute_import

from django.shortcuts import render
from django.core.mail import send_mail

from .forms import ContactForm


def tnc(request):
    context = {

    }
    return render(request, 'footer/tnc.html', context)


def privacy_policy(request):
    context = {

    }
    return render(request, 'footer/privacy_policy.html', context)


def contact_page(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact_name = contact_form.cleaned_data['contact_name']
            contact_email = contact_form.cleaned_data['contact_email']
            message = contact_form.cleaned_data['message']
            name_and_message = contact_name + ' ' + message

            send_mail(
                'New contact form submission from DiscLifts.com',
                name_and_message,
                contact_email,
                ['disclifts@gmail.com'],
                fail_silently=False,
            )
            context = {
                'confirmation_send_message': 'Thank you for your message, a member of our team will be in touch.',
            }
            return render(request, 'footer/contact_page.html', context)


    else:
        contact_form = ContactForm(

        )
    context = {
        'contact_form': contact_form,
    }
    return render(request, 'footer/contact_page.html', context)
