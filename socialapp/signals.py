from django.db.models.signals import post_save

from django.dispatch import receiver
from .models import PostLike, Post 

@receiver(post_save, sender=PostLike)
def update_post_likes(sender, instance, created, **kwargs):
    
    if created:
        post_likes = Post.objects.get(id = instance.post.id)
        post_likes.likes +=1
        post_likes.save()
