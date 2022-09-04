from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from auth.models import Account
from institution.models import Institution

from .serializers import InstitutionSerializer


@api_view(['GET'])
@authentication_classes((IsAuthenticated,))
def get_institution(response, institution_id=-1):
    try:
        inst = Institution.objects.get(institution_id=institution_id)
        serializer = InstitutionSerializer(inst)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "institution id not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_institution_users(response, institution_id=-1):
    # TODO: return array of users inside the current institution
    try:
        # queryset =
        pass
    except Exception as e:
        print(e)
        return Response({"message": "institution id not found"}, status=status.HTTP_404_NOT_FOUND)


class InstitutionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = InstitutionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            inst = serializer.create(request.data)
            return Response(status=status.HTTP_200_OK, data=inst)

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


