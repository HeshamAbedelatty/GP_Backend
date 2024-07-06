from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    faculty = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.username

    def calculate_total_likes(self):
        from PostsAndComments.models import Comment, Reply
        comment_likes = Comment.objects.filter(user=self).aggregate(total_likes=models.Sum('likes'))['total_likes'] or 0
        reply_likes = Reply.objects.filter(user=self).aggregate(total_likes=models.Sum('likes'))['total_likes'] or 0
        return comment_likes + reply_likes

    
    def scale_rate(self, likes, max_rate=5, max_likes=50):
        rate = (likes / max_likes) * max_rate
        return min(rate, max_rate)
    
    def get_rating(self):
        oldRate = self.rate
        likes = self.calculate_total_likes()
        newRate = self.scale_rate(likes)
        if oldRate < newRate:
            self.rate = newRate
            self.save()
            return newRate
        return oldRate