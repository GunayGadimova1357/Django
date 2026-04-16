from django.urls import path

from accounts.views import (
    register_view,
    register_success_view,
    login_view,
    dashboard_view,
    contact_view,
    contact_success_view,
)

app_name = "accounts"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register/success/', register_success_view, name='register_success'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('contact/', contact_view, name='contact'),
    path('contact/success/', contact_success_view, name='contact_success'),
]
