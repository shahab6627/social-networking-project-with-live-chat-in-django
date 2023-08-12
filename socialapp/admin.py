from django.contrib import admin
from .models import User, ProfilePicture,Post, PostLike, FriendRequest, UserChat

# Register your models here.

admin.site.register(User)
admin.site.register(ProfilePicture)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(FriendRequest)
admin.site.register(UserChat)



