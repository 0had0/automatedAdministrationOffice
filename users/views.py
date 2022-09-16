from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from auth.models import Account

from .serializers import DirectorSerializer, ReviewerSerializer, UserSerializer
from .permissions import IsDirector


# TODO: add isAdmin permission, this should not be integrated in production
class DirectorAPIView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = DirectorSerializer

    def post(self, request):
        user = request.data.copy() if type(request.data) is dict else {}
        user['institution'] = user.get('institution_id')

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            director = serializer.create(user)
            return Response(status=status.HTTP_200_OK, data={"user_id": director.user_id, "token": director.token})

        return Response({"message": "Something is Wrong!"}, status=status.HTTP_403_FORBIDDEN)


class DirectorUserInteractionAPIView(APIView):
    permission_classes = (IsAuthenticated, IsDirector)

    def post(self, request):
        data = request.data if type(request.data) is dict else {}
        is_reviewer = data.pop('is_reviewer', False)
        serializer = ReviewerSerializer if is_reviewer else UserSerializer
        data['institution_id'] = request.user.director.institution_id
        serializer = serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "invalid director id"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        data = request.data if type(request.data) is dict else {}
        if data:
            director_id = data.pop('director_id', None)
            user_id = data.pop('user_id', None)
            if director_id and user_id:
                # TODO: delete user with user_id
                return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "invalid director id"}, status=status.HTTP_403_FORBIDDEN)


class UsersAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        if user_id:
            user = Account.objects.get(pk=user_id)
            is_director = user.is_director
            is_reviewer = user.is_reviewer

            if is_director:
                serializer = DirectorSerializer(user.director)
            elif is_reviewer:
                serializer = ReviewerSerializer(user.reviewer)
            else:
                serializer = UserSerializer(user.user)

            return Response(serializer.data, status=status.HTTP_200_OK)
