from django.contrib import admin
from .models import Post, PostLike, Comment, Reply, CommentLike, ReplyLike

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(CommentLike)
admin.site.register(ReplyLike)