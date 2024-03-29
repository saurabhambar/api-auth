from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


@api_view(['GET'])
def restricted(request, *args, **kwargs):
    return Response(data="Only for logged in User", status=status.HTTP_200_OK)
