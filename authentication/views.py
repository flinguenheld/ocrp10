from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializer import SignUpSerializer


class SignUpView(APIView):

    serializer_class = SignUpSerializer

    def get(self, request):
        return Response(data={"Bienvenue, veuillez vous inscrire pour accéder à l'API"}, status=status.HTTP_405_NO_CONTENT)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
