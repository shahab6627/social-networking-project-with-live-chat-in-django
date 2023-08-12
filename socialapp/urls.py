from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('verify-account/<str:email>', activateAccount, name="activateAccount"),
    path('login', userLogin, name="userLogin"),
    path('profile', userProfile, name="profile"),
    path('upload-profile-image', uploadProfilePic, name="upload_profile_pic"),
    path('full-profile/<str:full_name>/<int:id>', otherUserProfile, name = 'full-profile'),
    path('post-like', likePost, name="like-post"),
    path('handel-friend', handelFriendRequests, name="handel-friend"),
    path('chat-between-<str:slug>', chat, name="chat"),
    path('send-invitation', sendInvitation, name="invitation"),
    path('delete-post', deletePost, name="delete_post"),
    
    path('logout', logoutUser, name="logout")
    
    
    
    
    
]
