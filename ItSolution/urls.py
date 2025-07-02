from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.random_quote, name='index'),
    path('add/', views.add_quote),
    path('top/', views.top_quotes),
    path('rate_quote/', views.rate_quote, name='rate_quote'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/mine', views.my_quotes, name='my_quotes'),
    path('profile/rated', views.my_rated_quotes, name='my_rated_quotes'),
    path('profile/history', views.my_history, name='my_history'),
    path('profile/', views.profile_info, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/password_change/', auth_views.PasswordChangeView.as_view(template_name='profile_templates/password_change.html'), name='password_change'),
    path('profile/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='profile_templates/password_change_done.html'), name='password_change_done'),

]
