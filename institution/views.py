from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from auth.models import Account
from institution.models import Institution
from users.permissions import IsDirector
from users.models import User, Reviewer, Director
from users.serializers import UserSerializer, ReviewerSerializer, DirectorSerializer

from .serializers import InstitutionSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_institution(response, institution_id=-1):
    try:
        inst = Institution.objects.get(institution_id=institution_id)
        serializer = InstitutionSerializer(inst)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "institution id not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsDirector))
def get_institution_users(response, institution_id=-1):
    # TODO: return array of users inside the current institution
    try:
        users_queryset = UserSerializer(User.objects.filter(institution_id=institution_id), many=True, allow_null=True, allow_empty=True)
        reviewers_queryset = ReviewerSerializer(Reviewer.objects.filter(institution_id=institution_id), many=True, allow_null=True, allow_empty=True)
        directors_queryset = DirectorSerializer(Director.objects.filter(institution_id=institution_id), many=True, allow_null=True, allow_empty=True)
        return Response({"directors": directors_queryset.data, "users": users_queryset.data, "reviewers": reviewers_queryset.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "institution id not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsDirector))
def add_document(response, institution_id=-1, director_id=-1):
    if institution_id == -1 or director_id == -1:
        return Response({"message": "institution id or director id are missing"}, status=status.HTTP_403_FORBIDDEN)
    try:
        inst = Institution.objects.get(institution_id=institution_id)
        # director_id = Director.objects.get(pk=director_id)
    except Exception as e:
        print(e)
        return Response({"message": "institution id not found"}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['POST'])
def create_institution(request):
    serializer = InstitutionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.create()
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user_id = request.data.pop('user_id', None)
        if user_id:
            director = Account.objects.get(user_id=user_id).director
            if director and director.institution_id:
                if director.is_director:
                    institution = Institution.objects.get(institution_id=director.institution_id)
                    serializer = InstitutionSerializer(institution, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(status=status.HTTP_200_OK, data=serializer.data)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "User is not a director"})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": 'User or Institution not found'})


