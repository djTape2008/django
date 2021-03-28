from django.shortcuts import render
from .models import Post, Category, User
from django.views.generic import DetailView, View, TemplateView
import requests, datetime
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
import requests

def main(request):
	return render(
		request, 
		'pages/main.html',
		{	'posts' : Post.objects.all(),
			'categorys' : Category.objects.all(),
			'datetime' : datetime.datetime.now(),
			'last_posts': Post.objects.all().order_by("-date")[:4],
		}
	)

def all_category(request):
	return render(
		request, 
		'pages/all_category.html',
		{	'posts' : Post.objects.all(),
			'categorys' : Category.objects.all(),
			'datetime' : datetime.datetime.now(),
		}
	)

def category(request, slug):
	global x
	category = get_object_or_404(Category, slug=slug)
	posts = Post.objects.filter(category=category)
	return render(request, 'pages/category.html', {'category': category,'posts' : posts, 'datetime' : datetime.datetime.now()})

def article(request, slug, pk):
	category = get_object_or_404(Category, slug=slug)
	posts = Post.objects.filter(category=category, id=pk)

	ipaddress = request.META.get('REMOTE_ADDR')
	counter = Post.objects.get(category=category, id=pk)

	if ipaddress != counter.ip:

		counter.ip = ipaddress
		counter.save()
		counter.view += 1
		counter.save()

	return render(request, 'pages/post.html', {'category': category,'posts' : posts, 'datetime' : datetime.datetime.now()})


class NewsDetailView(DetailView):
	model = Post
	template_name = 'pages/post.html'
	context_object_name = 'post'

class LoginView(TemplateView):

	def get(self, request, *args, **kwargs):
		form = LoginForm(request.POST or None)

		categories = Category.objects.all()
		context = {'form': form, 'categories': categories}

		return render(request, 'pages/login.html', context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)	
			if user:
				login(request, user)
				return HttpResponseRedirect('/')
		return render(request, 'pages/login.html', {'form': form})

class RegistrationView(TemplateView):

	def get(self, request, *args, **kwargs):
		form = RegistrationForm(request.POST or None)

		categories = Category.objects.all()
		context = {'form': form, 'categories': categories}

		return render(request, 'pages/registration.html', context)

	def post(self, request, *args, **kwargs):
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.username = form.cleaned_data['username']
			new_user.first_name = form.cleaned_data['first_name']
			new_user.last_name = form.cleaned_data['last_name']
			new_user.email = form.cleaned_data['email']
			new_user.save()
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			login(request, user)
			return HttpResponseRedirect('/')

		return render(request, 'pages/registration.html', {'form': form})

class ProfileView(DetailView):
	def get(self, request, *args, **kwargs):
		form = LoginForm(request.POST or None)

		categories = Category.objects.all()
		context = {'form': form, 'categories': categories}

		return render(request, 'pages/profile.html', context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return HttpResponseRedirect('/')
		return render(request, 'pages/profile.html', {'form': form})