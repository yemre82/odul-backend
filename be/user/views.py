from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from be.responses import response_200, response_400, response_500
from rest_framework.authtoken.views import ObtainAuthToken
from user.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

from user.request_utils import check_register_request

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register_or_login(request):
    if not check_register_request(request.data):
        return response_400("bad request")
    
    device_id = request.data.get("device_id")
    try:
        user=CustomUser.objects.get(username=device_id)
        user.last_login=datetime.now()
        user.save()
    except ObjectDoesNotExist as e:
        user = CustomUser.objects.create(username=device_id)
        user.set_password(device_id)
        user.last_login=datetime.now()
        user.save()
    token, _ = Token.objects.get_or_create(user=user)
    return_obj = {
        "token": token.key
    }
    return response_200("success", return_obj)