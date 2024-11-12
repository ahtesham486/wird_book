# serializers.py

from rest_framework import serializers
from .models import PhoneNumber,CommunityMember
 
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['number']

    def validate_number(self, value):
        # Check if the phone number is unique
        if PhoneNumber.objects.filter(number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value


class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = ['name', 'community', 'profile_image']

    def validate_community(self, value):
        # Ensure the community choice is valid
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Invalid community selection.")
        return value