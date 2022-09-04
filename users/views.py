from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import DirectorSerializer, ReviewerSerializer, UserSerializer
from .models import Director, User


# TODO: add isAdmin permission, this should not be integrated in production
class DirectorAPIView(APIView):
    # permission_classes = (IsAdmin,)
    serializer_class = DirectorSerializer

    def post(self, request):
        user = request.data if type(request.data) is dict else {}

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            director = serializer.create(request.data)
            return Response(status=status.HTTP_200_OK, data={"user_id": director.user_id, "token": director.token})

        return Response({"message": "Something is Wrong!"}, status=status.HTTP_403_FORBIDDEN)


class DirectorUserInteractionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # add user to an institution
        data = request.data if type(request.data) is dict else {}
        if data.director_id:
            director_id = data.pop('director_id', None)
            director = Director.objects.get(user_id=director_id)
            if director and director.institution_id:
                is_reviewer = data.pop('is_reviewer', False)
                serializer = ReviewerSerializer if is_reviewer else UserSerializer
                data['institution_id'] = director.institution_id
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
