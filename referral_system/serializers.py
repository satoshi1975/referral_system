from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """serializer for all users fields"""
    referred_phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_referred_phone_numbers(self, user):
        referred_users = UserProfile.objects.filter(used_referral_code=user)
        phone_numbers = [
            referred_user.phone_number for referred_user in referred_users]
        return phone_numbers


class CreateProfileSerializer(serializers.ModelSerializer):
    """serializer for add new user"""
    class Meta:
        model = UserProfile
        fields = ['phone_number']


class ShowOtherProfileSerializer(serializers.ModelSerializer):
    """serializer for a user found by number """
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'referral_code']
