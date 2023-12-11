from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from userAuthority.models import SEUser
from userAuthority.sendEmail import sendemail
from django.utils.crypto import get_random_string
import json

# 存储邮箱和验证码的字典
validate_data = {}

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            # 检查是否已经存在相同的邮箱账号
            if SEUser.objects.filter(email=email).exists():
                return HttpResponse(json.dumps({'message': '该邮箱已经注册'}), status=400)

            # 生成一个4位的随机验证码
            code = get_random_string(length=4, allowed_chars='0123456789')
            # 发送验证码到邮箱
            sendemail(code, email)
            # 存储邮箱和验证码
            validate_data[email] = code
            print('已发送给邮箱:'+email+'，验证码为:'+code)
            return HttpResponse(json.dumps({'message': '验证码已发送，请检查您的邮箱'}))
        except Exception as e:
            return JsonResponse({'error_code': 'INVALID_EMAIL', 'message': '不存在的邮箱'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return JsonResponse({'error_code': 'INVALID_ACTION', 'message': '无效请求'}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
def validate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            user_code = data.get('code')
            password = data.get('password')

            if email in validate_data and user_code == validate_data[email]:

                # 验证成功则将email从字典里删除
                del validate_data[email]

                # 将账号和密码写入数据库
                se_user = SEUser(email=email, password=password, authority='visitor')
                se_user.save()

                return HttpResponse(json.dumps({'message': '注册成功'}))
            else:
                return HttpResponse(json.dumps({'message': '验证码不匹配'}), status=400)
        except Exception as e:
            return HttpResponse(json.dumps({'message': '验证失败'}), status=500)
    else:
        return HttpResponse(json.dumps({'message': '无效的请求'}), status=400)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            print('登录邮箱:' + email + ',登录密码:' + password)
            # 自己实现用户验证逻辑
            user = SEUser.objects.filter(email=email).first()
            if user is not None:
                if password == user.password:
                    return JsonResponse({'token': 'token.key', 'message': '登录成功', 'authority': user.authority})
                else:
                    return JsonResponse({'error_code': 'INVALID_PASSWORD', 'message': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({'error_code': 'USER_NOT_FOUND', 'message': '用户名不存在'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse({'error_code': 'INTERNAL_SERVER_ERROR', 'message': '登录失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'error_code': 'BAD_REQUEST', 'message': '无效的请求'}, status=status.HTTP_400_BAD_REQUEST)
