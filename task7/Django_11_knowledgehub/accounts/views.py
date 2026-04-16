from django.shortcuts import render, redirect

from accounts.forms import RegisterForm, LoginForm, ContactForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            request.session['registered_user'] = form.cleaned_data['username']
            return redirect("accounts:register_success")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def register_success_view(request):
    return render(request, "accounts/register_success.html", {
        "username": request.session.get('registered_user', "New User")
    })

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['active_user'] = form.cleaned_data['username_or_email']
            return redirect("accounts:dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def dashboard_view(request):
    return render(
        request,
        "accounts/dashboard.html",
        {"active_user": request.session.get('active_user', "Guest")}
    )


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            request.session["contact_name"] = form.cleaned_data["name"]
            return redirect("accounts:contact_success")
    else:
        form = ContactForm()
    return render(request, "accounts/contact.html", {"form": form})


def contact_success_view(request):
    return render(
        request,
        "accounts/contact_success.html",
        {"contact_name": request.session.get("contact_name", "Guest")},
    )
