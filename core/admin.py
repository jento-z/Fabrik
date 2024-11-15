from django.contrib import admin

from .models import Profile, Post, LikePost, FollowersCount, ClosetItem, Outfit

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(ClosetItem)
admin.site.register(Outfit)

# Register your models here.
