from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.random_quote, name='index'),
    path('add', views.add_quote),
    path('top', views.top_quotes),
]
