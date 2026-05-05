from django.contrib import messages
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AvatarForm, RegisterForm, UserInfoForm
from .models import UserProfile
from .permissions import is_editor

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("stdstack:article-list")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def users_admin(request):
    if not is_editor(request.user):
        return HttpResponseForbidden("Only admins can manage users.")
    for account in User.objects.filter(profile__isnull=True):
        UserProfile.objects.create(user=account)
    users = User.objects.select_related("profile").order_by("username")
    return render(request, "accounts/users_admin.html", {"users": users})


@login_required
def profile_settings(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    user_form = UserInfoForm(instance=user)
    avatar_form = AvatarForm(instance=profile)
    password_form = PasswordChangeForm(user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "profile":
            user_form = UserInfoForm(request.POST, instance=user)
            avatar_form = AvatarForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and avatar_form.is_valid():
                user_form.save()
                avatar_form.save()
                messages.success(request, "Profile updated.")
                return redirect("stdstack:profile-settings")

        elif action == "password":
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Password changed successfully.")
                return redirect("stdstack:profile-settings")

    return render(request, "accounts/profile_settings.html", {
        "user_form": user_form,
        "avatar_form": avatar_form,
        "password_form": password_form,
        "profile": profile,
    })


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        from django.contrib.auth import logout
        logout(request)
        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect("stdstack:article-list")
    return redirect("stdstack:profile-settings")


def update_user_role(request, pk, action):
    if request.method != "POST":
        return redirect("stdstack:users-admin")
    if not is_editor(request.user):
        return HttpResponseForbidden("Only admins can manage users.")

    user = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if action in {"promote", "demote"} and not request.user.is_superuser:
        return HttpResponseForbidden("Only super admin can assign admins.")
    if action == "promote" and not user.is_superuser:
        user.is_staff = True
        user.save(update_fields=["is_staff"])
    elif action == "demote" and not user.is_superuser:
        user.is_staff = False
        user.save(update_fields=["is_staff"])
    elif action == "ban" and not user.is_superuser:
        profile.is_banned = True
        profile.save(update_fields=["is_banned"])
    elif action == "unban":
        profile.is_banned = False
        profile.save(update_fields=["is_banned"])

    return redirect("stdstack:users-admin")
