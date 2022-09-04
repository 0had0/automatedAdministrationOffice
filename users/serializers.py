from auth.serializers import AccountSerializer

from .models import Director, Reviewer, User


class DirectorSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        model = Director

    def create(self, validated_data):
        return Director.objects.create_user(**validated_data)


class ReviewerSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        model = Reviewer

    def create(self, validated_data):
        return Reviewer.objects.create_user(**validated_data)


class UserSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        model = User

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
