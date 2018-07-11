from rest_framework import serializers
from chit_app.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', )

class ChitlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Chit
        fields = '__all__'
        read_only_fields = ('id', )
