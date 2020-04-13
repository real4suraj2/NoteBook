from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required = True)
	
	class Meta:
		model = User
		fields = ('username','email','password1','password2')
		
	def save(self,commit = True):
		user = super(NewUserForm, self).save(commit = False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
		
class EditProfileForm(UserChangeForm):
    template_name='/something/else'
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'password'
			)
			
class EditUserProfileForm(UserChangeForm):
    template_name='/something/else'
    description = forms.CharField(max_length=350,required=False)
    city = forms.CharField(max_length=200,required=False)
    website = forms.URLField(required=False)
    phone = forms.IntegerField(required=False)
    image = forms.URLField(required=False)
    class Meta:
        model = UserProfile
        fields = (
            'description',
            'city',
            'website',
            'phone',
            'image',
			)