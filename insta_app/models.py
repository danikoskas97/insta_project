from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to='photo_profile', blank=True)
	gender = models.CharField(max_length=264,blank=True)
	city = models.CharField(max_length=264,blank=True)
	bio = models.TextField()
	follows = models.ManyToManyField('Profile', related_name='follow', symmetrical=False, blank=True)

	def __str__(self):
		return self.user.username

	def __repr__(self):
		return "<Profile {}>".format(self.user.username)

class Post(models.Model):
	text = models.TextField()
	photo = models.ImageField(upload_to='post_photo', blank=True)
	date_filed = models.DateField(default=timezone.now)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE ,related_name='post')
	liked_by = models.ManyToManyField('Profile', related_name='like', symmetrical=False, blank=True)

class Comment(models.Model):
	text = models.TextField()
	date_filed = models.DateField(default=timezone.now)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE ,related_name='profile')
	post = models.ForeignKey(Post, on_delete=models.CASCADE ,related_name='comment')



	