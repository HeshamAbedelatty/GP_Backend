from groups.models import Group
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Post(models.Model):
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post by {self.user.username} in {self.group.title}"

class Comment(models.Model):
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='comments/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id} in {self.group.title}"

class Reply(models.Model):
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='replies/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Reply by {self.user.username} on comment {self.comment.id} in {self.group.title}"
