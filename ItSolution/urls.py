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
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
