from auth.serializers import AccountSerializer, serializers

from .models import Director, Reviewer, User


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        exclude = ('password',)

    def create(self, validated_data):
        return Director.objects.create_user(**validated_data)


class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        exclude = ('password',)

    def create(self, validated_data):
        return Reviewer.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
