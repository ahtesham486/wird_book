# models.py

from django.db import models

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.number
    @property
    def is_authenticated(self):
        # Always return True to mimic authenticated user behavior
        return True

class CommunityMember(models.Model):
    COMMUNITY_CHOICES = [
        (1, 'Health'),
        (2, 'Software House'),
        (3, 'Sport')
    ]

    name = models.CharField(max_length=255)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, related_name="community_members")
    community = models.IntegerField(choices=COMMUNITY_CHOICES)
    profile_image = models.TextField()  # Store base64 image data as text

    def __str__(self):
        return self.name
    
    
class Token(models.Model):
    phone_number = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE, related_name="token")
    jwt_token = models.TextField()  # Store JWT as text to handle longer token strings
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.phone_number}"