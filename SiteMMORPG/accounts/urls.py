from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, register_view, enter_code_view


urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name = 'accounts/login.html'), name = 'login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name = 'accounts/logout.html'), name = 'logout'),
    
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('register/', register_view, name = 'register'),
    path('enter-code/', enter_code_view, name='enter_code'),

]