from django.urls import path
from .views import (
    login_view, logout_view, register_view, password_change_view
)

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('register/', register_view, name='register_view'),
    path('password_change/', password_change_view, name='password_change')
]