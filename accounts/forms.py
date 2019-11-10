from django.contrib.auth import authenticate, get_user_model
from django import forms

User = get_user_model()

class UsersLoginForm(forms.Form):
	username = forms.CharField(label='Felhasználónév')
	password = forms.CharField(widget = forms.PasswordInput, label='Jelszó')

	def __init__(self, *args, **kwargs):
		super(UsersLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"username"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"password"})

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("Sikertelen bejelentkezés")
			if not user.check_password(password):
				raise forms.ValidationError("Sikertelen bejelentkezés")

		return super(UsersLoginForm, self).clean(*args, **keyargs)

class UsersRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"password",
			"confirm_password", 
		]
	username = forms.CharField(label='Felhasználónév')
	email = forms.EmailField(label = "Email")
	password = forms.CharField(widget = forms.PasswordInput, label='Jelszó')
	confirm_password = forms.CharField(widget = forms.PasswordInput, label = 'Jelszó megerősítése')

	def __init__(self, *args, **kwargs):
		super(UsersRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"username"})
		self.fields['email'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"email"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"password"})
		self.fields['confirm_password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"confirm_password"})

	def clean(self, *args, **keyargs):
		email = self.cleaned_data.get("email")
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		confirm_password = self.cleaned_data.get("confirm_password")

		if password != confirm_password:
			raise forms.ValidationError("A jelszavak nem egyeznek meg")
		
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Ezzel az email címmel már létezik regisztráció")

		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("Ezzel a felhasználónévvel már létezik regisztráció")

		if len(password) < 8:
			raise forms.ValidationError("A jelszónak hosszabbnak kell lennie 8 karakternél")

		return super(UsersRegisterForm, self).clean(*args, **keyargs)