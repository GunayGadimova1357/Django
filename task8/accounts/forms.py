from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import UserProfile

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class BannedUserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if hasattr(user, "profile") and user.profile.is_banned:
            raise forms.ValidationError(
                "This account is banned.",
                code="banned",
            )


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
        }


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar"]
