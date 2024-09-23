from django.contrib import admin

# from django.contrib.auth.models import User
from .models import Friend, Chat, User

# Register your models here.
admin.site.register(User)
admin.site.register(Friend)
admin.site.register(Chat)
