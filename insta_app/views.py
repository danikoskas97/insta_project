from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from insta_app.forms import UserForm, UserProfileInfoForm , LoginForm, PostFrom, CommentForm
from insta_app.models import Profile , Post, Comment
from . import forms 
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


# Create your views here.
def signup(request):
		
	if request.method == 'POST' :
		user_form = forms.UserForm(data= request.POST) 
		profile_form = forms.UserProfileInfoForm(data= request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit= False)
			profile.user = user

			if 'photo' in request.FILES:
				profile.photo = request.FILES['photo']

			
			profile.save()
			print(profile.photo)
			login(request, user)
			return redirect('/insta_app/login')

		else : 
			print(user_form.errors, profile_form.errors)

	else: 
		user_form = forms.UserForm()
		profile_form = forms.UserProfileInfoForm()

	return render(request, 'signup.html', context = {
		'user_form' : user_form,
		'profile_form' : profile_form,
		})

def login_auth(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		profile = Profile.objects.get(user=user)
		print(user)
		if user is not None:
			login(request, user)
		return redirect('/insta_app/myprofile/')

	return render(request, 'login.html', context= {'login_form': LoginForm()})

def logout_auth(request):
	logout(request)
	return redirect('/insta_app/signup')

def myprofile(request):
	user = request.user
	profile = Profile.objects.get(user=user)
	# posts = Post.objects.get(profile=profile)
	# print(posts)
	return render(request , 'myprofile.html', context={'profile':profile })
	
def all_users(request):
	user = request.user
	my_profile = Profile.objects.get(user=user)
	profiles = Profile.objects.all()
	my_followers = my_profile.follows.all()

	return render(request, 'all_users.html', context= { 'profiles':profiles, 'my_prof':my_profile, 'my_followers': my_followers })


def folows(request , username):
	profile_connected_user = Profile.objects.get(user = request.user)
	user = User.objects.get(username=username)
	user_to_follow = Profile.objects.get(user=user)
	profile_connected_user.follows.add(user_to_follow)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def unfollow(request , username):
	profile_connected_user = Profile.objects.get(user = request.user)
	user_to_unfollow = Profile.objects.get(user__username=username)
	print(user_to_unfollow)
	profile_connected_user.follows.remove(user_to_unfollow)
	print(profile_connected_user.follows)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
	 
def getposts_byfollowers(user_id):
		user = User.objects.get(id=user_id)
		profile = Profile.objects.get(user=user)
		list_people_follow = profile.follows.all()

		posts_with_followers = []
		for follower in list_people_follow:
			post = Post.objects.filter(profile=follower)
			posts_with_followers.append(post)

		return posts_with_followers


def home(request):
	if request.user.is_authenticated:
		user = request.user

		# on recuper le user conecter
		profile = Profile.objects.get(user=user)

	return render(request, 'home.html', context={'posts_with_followers' : getposts_byfollowers(user.id)})

def like(request , post_id):
	profile_connected_user = Profile.objects.get(user = request.user)
	like = Post.objects.get(id=post_id)
	profile_connected_user.like.add(like)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def sendpost(request):
	if request.user.is_authenticated:
		user = request.user
		profile = Profile.objects.get(user=user)

	if request.method == 'POST' :
		send_post_form = forms.PostFrom(data= request.POST) 

		if send_post_form.is_valid():
			
			send_post = send_post_form.save(commit= False)
			send_post.profile = profile


			if 'photo' in request.FILES:
				send_post.photo = request.FILES['photo']

			send_post = send_post_form.save()

	else: 
		send_post_form = forms.PostFrom()
		

	return render(request, 'send_post.html', context={
		'send_post_form' : send_post_form,
		})	

def profile(request , username):
	user = User.objects.get(username=username)
	profile_connected_user = Profile.objects.get(user = request.user)
	profile =Profile.objects.get(user=user)
	return render(request, 'profile.html' , context={'profile_connected_user':profile_connected_user , 'user':user })





def comment_form(request, post_id):
	if not request.user.is_authenticated:
		return redirect('/insta_app/')

	user = request.user
	profile=Profile.objects.get(user=user)
	if request.method == 'POST':


		Comment.objects.get_or_create(

			text=request.POST.get('text'),
		 	profile=profile,
		 	post=Post.objects.get(id=post_id)
		 	)
			

		return redirect('/insta_app/home')
	
	return render(request, 'comment_form.html', context={ 'user': user,
		'comment_form': CommentForm() })



    


