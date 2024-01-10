from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import CustomUser
from .sendEmail import sendemail
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import json

# 存储邮箱和验证码的字典
validate_data = {}


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        # 检查邮箱是否已被注册
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'message': '该邮箱已经注册'}, status=400)

        # 生成验证码并发送
        code = get_random_string(length=4, allowed_chars='0123456789')
        sendemail(code, email) #出错点
        validate_data[email] = code
        return JsonResponse({'message': '验证码已发送，请检查您的邮箱'})

    return JsonResponse({'message': '无效请求'}, status=400)


@csrf_exempt
def validate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')     
        password = data.get('password')
        code = data.get('code')

        # 检查验证码
        if email in validate_data and validate_data[email] == code:
            # 创建新用户
            user = CustomUser.objects.create_user(username = email, email = email, password = password)
            user.save()
            return JsonResponse({'message': '注册成功'})

        return JsonResponse({'message': '验证码错误或已过期'}, status=400)

    return JsonResponse({'message': '无效请求'}, status=400)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = AuthenticationForm(request, data)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({
                    'token': token.key,
                    'message': '登录成功',
                    'access_system_a': user.access_system_a,
                    'access_system_b': user.access_system_b,
                    'access_system_c': user.access_system_c,
                    'access_system_d': user.access_system_d,
                    'access_system_e': user.access_system_c,
                    'access_system_f': user.access_system_c,
                    # 其他系统权限
                })
            else:
                return JsonResponse({'error1': 'Invalid username or password.'}, status=400)
        else:        
            return JsonResponse({'error2':str(form.cleaned_data)}, status=400)
            return JsonResponse({'error2': 'Invalid form data.'}, status=400)
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})