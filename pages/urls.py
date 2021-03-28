from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views
import os

urlpatterns = [
	path('', views.main, name = 'main'),
	path('category/', views.all_category, name = 'all_category'),
	path('category/<str:slug>/', views.category, name = 'category'),
	path('category/<str:slug>/<int:pk>', views.article, name = 'news_detail'),
	path('login/', views.LoginView.as_view(), name = 'login'),
	path('logout/', LogoutView.as_view(next_page='/'), name = 'logout'),
	path('registration/', views.RegistrationView.as_view(), name = 'registration'),
	path('profile/', views.ProfileView.as_view(), name = 'profile'),
]