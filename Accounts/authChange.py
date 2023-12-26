from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_user_permissions(request):
    UserModel = get_user_model()
    data = request.data
    email = data.get('email')  # 获取要更新的用户邮箱

    # 检查执行操作的用户是否为超级用户
    if not request.user.is_superuser:
        return Response({"message": "只有超级用户才能执行此操作"}, status=403)

    try:
        # 根据邮箱查找用户
        user_to_update = UserModel.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response({"message": "未找到指定的用户"}, status=404)

    if request.user.is_superuser:
        # 示例：更新当前用户的权限，也可以根据需要更新其他用户
        user = request.user
        user_to_update.access_system_a = data.get('System_A', user_to_update.access_system_a)
        user_to_update.access_system_b = data.get('System_B', user_to_update.access_system_b)
        user_to_update.access_system_c = data.get('System_C', user_to_update.access_system_c)
        user_to_update.access_system_d = data.get('System_D', user_to_update.access_system_d)
        user_to_update.access_system_e = data.get('System_E', user_to_update.access_system_e)
        user_to_update.access_system_f = data.get('System_F', user_to_update.access_system_f)
        # ... 其他系统权限 ...
        user_to_update.save()

        return Response({"message": "权限更新成功"})
    else:
        return Response({"message": "无权限执行此操作"}, status=403)
