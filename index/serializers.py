from index.models import User

from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'is_active', 'username', 'email', 'first_name', 'last_name', 'user_type',
            'token')
    def get_token(self, obj):
            token=AccessToken.for_user(obj)
            # token=AccessToken.objects.get(user=obj)
            return str(token)

