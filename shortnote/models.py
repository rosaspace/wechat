from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to="static/shortnote/user_images/",
        default="static/shortnote/user_images/default.jpg"
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField(
        "self", symmetrical=False, related_name="friend_of"
    )


class Friend(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendships"
    )
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "friend"]

    def __str__(self):
        return (f"{self.user.username} is friends with "
                f"{self.friend.username}")


class Chat(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_chats"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_chats"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(
        upload_to="chat_images/", null=True, blank=True
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return (f"Chat from {self.sender.username} to "
                f"{self.receiver.username} at {self.timestamp}")

    class Meta:
        ordering = ["timestamp"]
