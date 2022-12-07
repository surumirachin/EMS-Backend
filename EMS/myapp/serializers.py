from rest_framework import serializers
from myapp.models import User ,Leave
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ["password"]



class UserSerializer(serializers.ModelSerializer):
  
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = get_user_model().objects.create(
            **validated_data
        )

        user.set_password(password)
        user.save()

        return user
    
    class Meta:
        model = get_user_model()
        exclude = ["profile_pic"]

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class LeaveSerializer(serializers.ModelSerializer):

    class Meta:

        model = Leave

        fields = '__all__'