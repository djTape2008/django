from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Post

class LoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError(f'Пользователь {username} не найден!')

		user = User.objects.filter(username=username).first()
		if user:
			if not user.check_password(password):
				raise forms.ValidationError('Неверный пароль!')
		return self.cleaned_data

	class Meta:
		model = User
		fields = ['username', 'password']

class RegistrationForm(forms.ModelForm):

	confirm_password = forms.CharField(widget=forms.PasswordInput)
	password = forms.CharField(min_length=8, widget=forms.PasswordInput)
	email = forms.CharField(required=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'
		self.fields['confirm_password'].label = 'Подтвердите пароль'
		self.fields['email'].label = 'Электронная почта'
		self.fields['first_name'].label = 'Ваше имя'
		self.fields['last_name'].label = 'Ваша фамилия'

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError(f'Имя {username} уже занято')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(f'Электронная почта {email} уже занята')
		return email

	def clean(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']
		if password != confirm_password:
			raise forms.ValidationError(f'Пароли не совпадают')
		return self.cleaned_data		

	class Meta:
		model = User
		fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name']