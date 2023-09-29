from rest_framework.serializers import ModelSerializer, ValidationError, ImageField
from django.contrib.auth.models import User
from base.models import UserProfile
from rest_framework import serializers

from base.models import Note

class NotSerializer(ModelSerializer):
    class Meta: 
        model = Note
        fields = "__all__"


class UserRegister(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'id']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
       
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("this username is already taken try  new one ")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise ValidationError("this email is already used. try another")
        return value
    
    def create(self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        profile = UserProfile.objects.create(user_id = instance)
        profile.save()
        print("====================>>>>>>>>>>>>>>>", profile)
        return instance\
    
class ProfileSerializer(ModelSerializer):
    profile_img = ImageField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        print(validated_data)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)
        instance.Phone_no = validated_data.get('Phone_no', instance.Phone_no)
        instance.save()

        print('df')

        return instance
    


class SingleProfileSerializer(ModelSerializer):
    username = serializers.ReadOnlyField(source='user_id.username')
    email = serializers.ReadOnlyField(source='user_id.email')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'date_of_birth', 'Phone_no']
        
