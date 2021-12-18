from django.contrib import admin
from .models import ReviewReport, CommentReport, NestedCommentReport, RatingReport

# Register your models here.
admin.site.register(ReviewReport)
admin.site.register(CommentReport)
admin.site.register(NestedCommentReport)
admin.site.register(RatingReport)