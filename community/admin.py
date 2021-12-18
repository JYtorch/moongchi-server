from django.contrib import admin
from .models import Review, Comment, NestedComment, Rating

# Register your models here.

admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(NestedComment)
admin.site.register(Rating)