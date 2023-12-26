from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_system_permissions(request):
    user = request.user
    permissions = {
        'access_system_a': user.access_system_a,
        'access_system_b': user.access_system_b,
        'access_system_c': user.access_system_c,
        'access_system_d': user.access_system_d,
        'access_system_e': user.access_system_e,
        'access_system_f': user.access_system_f,
    }
    return Response(permissions)
