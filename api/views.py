# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import *

# Create your views here.


def current_user(request):
    user = request.user
    serial = CustomUserSerializer(user)
    return JsonResponse(serial.data, safe=False, status=200)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': CustomUserSerializer(user, context={'request': request}).data
    }


class UserListDetailView(viewsets.ModelViewSet):
    """
    Endpoint to retrieve user list
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all().exclude(username="admin")
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    filter_fields = ('id', 'username', 'school_name')
    search_fields = ('school_name', 'region')


class UserProfileAPIView(viewsets.ModelViewSet):
    """
        Protected endpoint to retrieve user profile.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()


class UserLoginAPIView(APIView):
    """
    Endpoint for user login. Returns authentication token on success.
    will be deprecated as soon as jwt works
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayeeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Payee.objects.all()
    serializer_class = PayeeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('email', 'name')


class FeeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    filter_fields = ('id', 'user', 'name')
    search_fields = ('name', )


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('paid_to', 'received_from', 'pay_date')
    search_fields = ('pay_date', )
    ordering_fields = ('id', 'pay_date')
