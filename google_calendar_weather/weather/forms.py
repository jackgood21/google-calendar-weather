from django import forms
from .models import UserInfo
class UserRegisterForm(forms.ModelForm):
	class Meta:
		model = UserInfo
		fields = ['zip_code','unit_of_temperature']