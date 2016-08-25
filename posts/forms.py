from django import forms
from .models import Posts, Events


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['event', 'lift_type', 'spaces', 'location', 'leaving_time', 'leaving_date', 'return_date', 'comments']
        # This is for the date picker popup
        widgets = {
            'leaving_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'return_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        labels = {
            'location': ('Location'),
        }
        help_texts = {
            'location': ('Location you are leaving from'),
        }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }

        # When this validation is applied and 12 is picked for spaces the submit button returns a None value instead of a
        # httpresponse object
        # def clean_spaces(self):
        #     spaces = self.cleaned_data.get('spaces')
        #     if spaces not in range(1, 10):
        #         raise forms.ValidationError('Please pick a number between 1 and 10')
        #     return spaces


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'content', 'location', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['event', 'lift_type', 'spaces', 'location', 'leaving_time', 'leaving_date', 'return_date',
                  'fulfilled', 'comments']
        widgets = {
            'leaving_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'return_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        labels = {
            'location': ('Location'),
        }
        help_texts = {
            'location': ('Location you are leaving from'),
        }
