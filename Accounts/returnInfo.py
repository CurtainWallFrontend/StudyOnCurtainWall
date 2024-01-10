from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from django.http import JsonResponse
import json

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user_email(request):
    user = request.user
    return Response({'email': user.email})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user_info(request):
    user = request.user
    user_obj = CustomUser.objects.get(email=user)

    if user_obj:
        Info = {
            'id': user_obj.id,
            'email': user.email,
            'username': user_obj.username,
        }
        return JsonResponse({'message': '成功返回信息',
                            'data': Info })
    return Response({'message': '信息获取失败'}, status=400)
