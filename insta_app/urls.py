from django.urls import path
from . import views

app_name = 'insta_app'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_auth, name='login'),
    path('logout/', views.logout_auth, name='logout_auth'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('all_users/', views.all_users, name='all_users'),
    path('all_user/<username>', views.folows, name='follow'),
    path('all_users/<username>', views.unfollow, name='unfollow'),
    path('home/', views.home, name='home'),
    path('home/send_post/', views.sendpost, name='sendpost'),
    path('profile/<username>' , views.profile , name='profile'),
    path('home/comment_form/<int:post_id>', views.comment_form, name='comment_form'),
    path('home/like/<int:post_id>', views.like, name='like'),


]