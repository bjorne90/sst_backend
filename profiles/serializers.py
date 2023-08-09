from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone_number', 'about_me', 'profile_image', 'work_id', 'work_title', 'address']  # add other fields if necessary

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = Profile.objects.update_or_create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.update(UserSerializer(), instance.user, validated_data=user_data)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.about_me = validated_data.get('about_me', instance.about_me)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance
