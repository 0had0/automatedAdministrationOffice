from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (AccountSerializer, LoginSerializer)
from .models import Account


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def authenticate_account(request):
    user_id = request.data['user_id'] if type(request.data) is dict else -1
    user = Account.objects.get(pk=user_id)
    return Response({
            'email': user.email,
            'user_id': user.user_id,
            'token': request.auth,
            'is_director': user.is_director,
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        acc = serializer.create(request.data)
        return Response(status=status.HTTP_200_OK, data={"user_id": acc.user_id, "token": acc.token})


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data if type(request.data) is dict else {}

        serializer = self.serializer_class(data=user)

        data = serializer.validate(user)

        return Response(data, status=status.HTTP_200_OK)
