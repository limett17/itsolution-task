from django.contrib import admin
from django.contrib.auth.views import LogoutView
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
]
