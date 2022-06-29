from django import forms
from .models import _UserProfileModel

# We're creating a form that inherits from the ModelForm class, and we're using the UserProfile model
# as the base for the form.

class UserProfileForm(forms.ModelForm):

    twitter = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Username without @'}))
    facebook = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Username without @'}))
    linkedin = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Username without @'}))
    instagram = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Username without @'}))
    phone = forms.IntegerField(required=False, max_value=9999999999)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
          self.fields[field].widget.attrs.update({'class': 'form-control'})


# The `UserProfileForm` class inherits from the `ModelForm` class, and it's `Meta` class is set to the
# `_UserProfileModel` model, and the `exclude` attribute is set to `('user', 'is_2fa',
# 'profile_image')`
    class Meta:
        model = _UserProfileModel
        exclude = ('user', 'is_2fa', 'profile_image')
        widgets = {
          'bio': forms.Textarea(attrs={'rows':4, 'cols':20}),
        }


