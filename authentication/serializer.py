from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import PasswordField

from authentication.models import User


class SignUpSerializer(ModelSerializer):

    password = PasswordField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

    def validate_password(self, password):
        if validate_password(password) is None:  # Raise a ValidationError with messages
            return make_password(password)


class UserSerializer(ModelSerializer):
    """ Simple serializer, used to display user in nested serializers """

    class Meta:
        model = User
        fields = ['id', 'email']
