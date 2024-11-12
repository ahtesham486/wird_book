# authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import PhoneNumber

class PhoneNumberJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            phone_number_id = validated_token["user_id"]  # `user_id` should map to `PhoneNumber` ID
            phone_number = PhoneNumber.objects.get(id=phone_number_id)
            return phone_number
        except PhoneNumber.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")
