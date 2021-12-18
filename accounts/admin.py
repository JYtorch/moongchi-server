from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Playlist

# Register your models here.
admin.site.register(get_user_model())
admin.site.register(Playlist)