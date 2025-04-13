from django.contrib import admin
from django.urls import path, include
from pages import views


urlpatterns = [
    path('', views.inicio, name="inicio"),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout")

]