from django.contrib import admin
from .models import CustomUser, Profile,Post,LikePost,Follower
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follower)