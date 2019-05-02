from django.contrib.auth import login, authenticate

from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'other_email','password1']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password']

    def get_user(self):
        cleaned_data = super(LoginForm, self).clean()
        user = cleaned_data.get("email")
        pwd = cleaned_data.get("password")

        if '@' in user:
            kwargs = {'email': user}
        else:
            kwargs = {'username': user}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(pwd):
                return user
        except:
            raise forms.ValidationError("credentials are wrong")
