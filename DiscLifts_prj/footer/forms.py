from django import forms


# our new form
class ContactForm(forms.Form):
    contact_name = forms.CharField(label='Your name', required=True)
    contact_email = forms.EmailField(label='Your email', required=True)
    message = forms.CharField(
        label='Message',
        required=True,
        widget=forms.Textarea
    )
