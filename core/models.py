from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture-png.wbpg')
    location = models.CharField(max_length=100, blank=True)
    
    def __srt__(self):
        return self.user.username
    
class ClosetItem(models.Model):
    CATEGORY_CHOICES = [
        ('Tops', 'Tops'),
        ('Bottoms', 'Bottoms'),
        ('Shoes', 'Shoes'),
        ('Hats', 'Hats'),
        ('Accessories', 'Accessories')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links each item to a specific user
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # Selects the item category
    item_name = models.CharField(max_length=100)  # Name or description of the item
    image = models.ImageField(upload_to='closet_items')  # Image of the clothing item
    date_added = models.DateTimeField(default=datetime.now)  # Date the item was added

    # Optional Fields
    size = models.CharField(max_length=10, blank=True, null=True)  # e.g., S, M, L
    color = models.CharField(max_length=50, blank=True, null=True)  # e.g., Red, Blue
    brand = models.CharField(max_length=50, blank=True, null=True)  # e.g., Nike, Zara
    
    def __str__(self):
        return f"{self.item_name} ({self.category}) - {self.user.username}"
    
class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)  # Optional name for the outfit
    created_at = models.DateTimeField(default=datetime.now)
    
    # Link each part of the outfit to a ClosetItem, allowing null if not used
    hat = models.ForeignKey(ClosetItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="hat_outfits")
    top = models.ForeignKey(ClosetItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="top_outfits")
    bottom = models.ForeignKey(ClosetItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="bottom_outfits")
    shoes = models.ForeignKey(ClosetItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="shoes_outfits")
    accessories = models.ForeignKey(ClosetItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="accessories_outfits")

    def __str__(self):
        return f"{self.name} - {self.user.username}" if self.name else f"Outfit by {self.user.username}"
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user