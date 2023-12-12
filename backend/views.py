from argparse import _ActionsContainer
import io
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from backend.models import *
from rest_framework import status
from backend.serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db import IntegrityError

from datetime import datetime, timedelta
from django.utils import timezone
import re

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import csv
import numpy as np
import torch
import cv2
import sys

class DeviceAPI(GenericViewSet):
    serializer_class = ImageSerializer
    queryset = Device.objects.all()

    @action(methods=['get'], detail=False)
    def get_device(self, request):
        devices = self.get_queryset()
        result = []
        for device in devices:
            building_option = next((opt for opt in result if opt["value"] == device.building.building_id),None)

            if building_option:
                #如果楼宇已在结果中存在
                building_option["children"].append({
                    "value": device.device_id,
                    "label": device.device_name
                })
            else:
                building_option ={
                    "value": device.building.building_id,
                    "label": device.building.building_name,
                    "children":[{
                        "value": device.device_id,
                        "label": device.device_name
                    }]
                }
                result.append(building_option)

        return Response({
            'options': result,
        },status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def add_device(self,request):

        building = Building.objects.get(pk='1')
        print(building)
        # device_id会自动生成
        device = Device(device_name='新设备',
                        building=building)
        device.save()

        response = {
            'message':'Device create successfully',
            'device_id': device.device_id,
            'device_name':device.device_name,
            'building':device.building.building_name,
        }
        return Response(response,status=status.HTTP_200_OK)

    @action(methods=['get'],detail=False)
    def delete_device(self,request):
        device = get_object_or_404(Device, pk='12')
        device.delete()
        return Response({
            'message':'device deleted successfully'
        },status=status.HTTP_200_OK)

class GetImg(GenericViewSet):
    serializer_class = ImageSerializer

    @action(methods=['post'], detail=False)
    def save_image(self, request):
        file_path = './media/' # 指定保存文件的文件夹路径
        # 若文件夹不存在则新建
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        if request.POST.get('func')  == 'A':

            file_path = os.path.join(file_path,'segmentaion')
            fs = FileSystemStorage(location=file_path)
            try:
                uploaded_file = request.FILES['image']  # 获取上传的图像文件
                FileSystemStorage(location=file_path)
                filename = fs.save(uploaded_file.name, uploaded_file)

                #返回图片先写死为原图片
                result_url = request.build_absolute_uri('/media/segmentation/' + filename)
                print(result_url)
                return Response({'message': 'Image Saving complete.',
                                 'total': 13,  #结果图片数量
                                 'pictures': [   #结果图片url
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url}, 
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                 ]}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e),'message': 'Image uploading fail.'}, status=status.HTTP_400_BAD_REQUEST)

                # 开始图像分割的操作————————————————————————————
                # 以下代码由严文昊小组填充修改———————————————————
                # 取消代码逻辑，后续用链接代替

        elif request.POST.get('func')  == 'B':
            file_path = os.path.join(file_path,'explosion_identify')
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            fs = FileSystemStorage(location=file_path)

            try:
                uploaded_file = request.FILES['image']  # 获取上传的图像文件
                filename = fs.save(uploaded_file.name, uploaded_file)


                 # 开始识别玻璃内爆的操作—————————————————————————
                 # 以下代码由邓丁熙小组填充修改———————————————————

                #返回图片先写死为原图片
                result_url = request.build_absolute_uri('/media/explosion_identify/' + filename)
                return Response({'message': 'Image Saving complete.',
                                 'total': 13,  #结果图片数量
                                 'pictures': [   #结果图片url
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                     {'url': result_url},
                                 ]}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e),'message': 'Image uploading fail.'}, status=status.HTTP_400_BAD_REQUEST)

            # 数据平滑

#数据平滑
def data_smoothing(data, num_parts):
    n = len(data)
    chunk_size = n // num_parts  # 每份大小
    result = []
    for i in range(0, n, chunk_size):
        chunk = data[i:i + chunk_size]
        average = sum(chunk) / len(chunk)
        result.append(average)
    return result

#从用户上传的文件名中提取长度
def extract_time(origin_string):
    pattern = r"\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}"
    match = re.search(pattern, origin_string)
    if match:
        datetime_str = match.group()
    datetime_obj = datetime.strptime(datetime_str,"%Y_%m_%d_%H_%M_%S")
    return datetime_obj

class VibrationData(GenericViewSet):
    serializer_class = ImageSerializer

    # 保存csv文件到数据库
    @action(methods=['post'], detail=False)
    def save_csv(self,request):
        file_path = './backend/media/' # 指定保存文件的文件夹路径

        file_path = os.path.join(file_path,'vibration/')
        # 若文件夹不存在则新建
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        try:
            uploaded_file = request.FILES['csv']  # 获取上传的图像文件
            device_name = uploaded_file.name.split("_")[0][6:] #设备名称
            device = Device.objects.get(device_name=device_name)
            start_time = extract_time(uploaded_file.name)

            # 判断文件是否存在
            if os.path.exists(file_path + uploaded_file.name):
                #文件已存在
                print("该文件已上传过")
            else:
                #文件尚不存在
                # 创建文件系统存储对象
                fs = FileSystemStorage(location=file_path)
                fs.save(uploaded_file.name, uploaded_file)

            # 从保存的.csv文件中读取数据并返回前端
            x_data=[]
            y_data=[]
            z_data=[]

            with open(file_path + uploaded_file.name,'r') as file:
                reader =csv.reader(file,delimiter=',')
                for i,row in enumerate(reader):
                    x_data.append(float(row[0].strip()))
                    y_data.append(float(row[1].strip()))
                    z_data.append(float(row[2].strip()))

            parts = 3600
            x_data = data_smoothing(x_data,parts)
            y_data = data_smoothing(y_data,parts)
            z_data = data_smoothing(z_data,parts)


            unique_logs = []
            existing_records = set()

            #保存到数据库
            for i in range(parts):
                time = start_time + timedelta(seconds=i)
                log = Log(time=time,
                          x=x_data[i],
                          y=y_data[i],
                          z=z_data[i],
                          device_id=device.device_id)
                record_key = (log.time,log.x,log.y,log.z,log.device_id)
                if record_key not in existing_records:
                    unique_logs.append(log)
                    existing_records.add(record_key)
            try:
                Log.objects.bulk_create(unique_logs)
            except IntegrityError:
                # 处理插入冲突错误
                error_message = "Duplicate records found"
                error_code = "DUPLICATE_RECORDS"
                return Response({"error": error_message, "code": error_code,
                                 "device_id": device.device_id,
                                 "yData":{
                                     'x': x_data,
                                     'y': y_data,
                                     'z': z_data,
                                 }}, status=status.HTTP_200_OK)
            except Exception as e:
                # 处理其他插入错误
                error_message = str(e)
                error_code = "INSERT_ERROR"
                return Response({"error": error_message, "code": error_code}, status=500)

            return Response({
                'yData':{
                    'x':x_data,
                    'y':y_data,
                    'z':z_data,
                },
                "device_id": device.device_id,
                'csv_url': file_path + uploaded_file.name,
            },status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def filter_outlier(self,request):
        file_path = os.path.join('./backend/media/','vibration/')
        try:
            min = request.POST['min']
            max = request.POST['max']
            file_url = request.POST['csv_url']
            min = float(min)
            max = float(max)

            print(file_url)

            # 从保存的.csv文件中读取数据并返回前端
            x_data=[]
            y_data=[]
            z_data=[]

            with open(file_url,'r') as file:
                reader =csv.reader(file,delimiter=',')
                for i,row in enumerate(reader):
                    x_data.append(float(row[0].strip()))
                    y_data.append(float(row[1].strip()))
                    z_data.append(float(row[2].strip()))

            # 筛选异常值
            x_abnormal = [ x for x in x_data if x < min or x > max]
            y_abnormal = [ y for y in y_data if y < min or y > max]
            z_abnormal = [ z for z in z_data if z < min or z > max]

            return Response({
                'yData':{
                    'x':x_abnormal,
                    'y':y_abnormal,
                    'z':z_abnormal,
                },
            },status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #保存异常值
    @action(methods=['post'], detail=False)
    def save_abnormal(self,request):
        device_id = request.data['device']
        abnormalData = request.data['abnormalData']
        min = request.data['min']
        max = request.data['max']
        file_name = os.path.basename(request.data['url'])
        start_time = extract_time(file_name)

        unique_logs = []
        existing_records = set()
        records = []

        try:
            # 保存到数据库
            for i in range(len(abnormalData['x'])):
                record = Abnormal(time=start_time,
                          device_id=device_id,
                          min=min,
                          max=max,
                          direction='x',
                          data=abnormalData['x'][i],
                          last_modified=datetime.now())
                records.append(record)
            for i in range(len(abnormalData['y'])):
                record = Abnormal(time=start_time,
                          device_id=device_id,
                          min=min,
                          max=max,
                          direction='y',
                          data=abnormalData['y'][i],
                          last_modified=datetime.now())
                records.append(record)
            for i in range(len(abnormalData['z'])):
                record = Abnormal(time=start_time,
                          device_id=device_id,
                          min=min,
                          max=max,
                          direction='z',
                          data=abnormalData['z'][i],
                          last_modified=datetime.now())
                records.append(record)

            try:
                Abnormal.objects.bulk_create(records,ignore_conflicts=True)
            except Exception as e:
                # 处理其他插入错误
                error_message = str(e)
                error_code = "INSERT_ERROR"
                return Response({"error": error_message, "code": error_code}, status=500)

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    #搜索正常值
    @action(methods=['post'], detail=False)
    def search_abnormal(self,request):
        try:
            building_id = request.POST['building']
            device_id = request.POST['equipment']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            pageNo = request.POST['pageNo']
            pageSize = request.POST['pageSize']

            #数据库查找
            building = Building.objects.get(building_id=building_id)
            logs = Abnormal.objects.filter(device_id=device_id)
            result = []
            for log in logs:
                row = {
                    "time": log.time.strftime('%Y-%m-%d %H:%M:%S'),
                    "building": building.building_name,
                    "equipment": log.device.device_name,
                    "data": log.data,
                    "direction": log.direction,
                    "last_modified": log.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
                    "min": log.min,
                    "max": log.max,
                }
                result.append(row)
            paginator = Paginator(result, pageSize)
            records = list(paginator.get_page(pageNo))

            return Response({
                'total': len(result),
                'records': records,
            },status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# 发送邮件到指定邮箱
class SendMail(GenericViewSet):
    serializer_class = ImageSerializer

    @action(methods=['post'], detail=False)
    def send_mail(self,request):
        info = request.data;
        sender_address = 'curtainwall2023@163.com'
        receiver_address = info['address']
        subject = '异常数据报告'

        x_str = ';  '.join(str(x) for x in info['data']['x']) if info['data']['x'] else ''
        y_str = ';  '.join(str(y) for y in info['data']['y']) if info['data']['y'] else ''
        z_str = ';  '.join(str(z) for z in info['data']['z']) if info['data']['z'] else ''

        message = f"异常范围：[{info['min']},{info['max']}]\n" \
                 f"传感器编号：{info['device']} \n" \
                 f" x方向:\n {x_str} \n\n" \
                 f" y方向:\n {y_str} \n\n" \
                 f" z方向:\n {z_str} "

        # 创建邮件内容
        msg = MIMEMultipart()
        msg['From'] = sender_address
        msg['To'] = receiver_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        try:
            # #连接SMTP服务器并发送邮件
            smtp_server = 'smtp.163.com'
            port = 25
            username = 'curtainwall2023@163.com'
            password = 'ZFTHMXDLEOEZDJTS'

            with smtplib.SMTP(smtp_server, port) as server:
                server.login(username, password)
                server.sendmail(sender_address, receiver_address, msg.as_string())

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# def segment_image(input_image_data, output_dir='/root/StudyOnCurtainWall/backend/media/segged', sam_checkpoint="backend\sam_vit_h_4b8939.pth", model_type="vit_h"):
#     # Check if CUDA is available
#     if torch.cuda.is_available():
#         device = "cuda"
#     else:
#         device = "cpu"
#     # Create the output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)
#     print("here")
#
#     # Load the SAM model
#     sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
#     sam.to(device=device)
#     mask_generator = SamAutomaticMaskGenerator(sam)
#
#     # Process the input image data
#     image = cv2.cvtColor(input_image_data, cv2.COLOR_BGR2RGB)
#     width = int(image.shape[1] * 25 / 100)
#     height = int(image.shape[0]* 25 / 100)
#     size = width * height
#     image = cv2.resize(image, (width, height))
#     masks = mask_generator.generate(image)
#
#     def generate_anns(anns, image, size):
#         original_image = image
#         if len(anns) == 0:
#             return
#
#         sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
#         img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
#         img[:, :, 3] = 0
#
#         for index, ann in enumerate(sorted_anns):
#             m = ann['segmentation']
#             if ann['area'] > size / 24 and ann['area'] < size / 2:
#                 img_tosave = np.where(m[..., None] == 1, original_image, 255)
#                 img_tosave = cv2.cvtColor(img_tosave, cv2.COLOR_BGR2RGB)
#                 output_filename = f"{index}_saved.png"
#                 output_path = os.path.join(output_dir, output_filename)
#                 cv2.imwrite(output_path, img_tosave)
#
#     generate_anns(masks, image, size)


# 数据平滑处理

# -----------------------------------------------------------------------------------------------------------------------------------
# 用户信息登录/注册/发送验证码
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from backend.models import User
from backend.sendEmail import sendemail
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
            if User.objects.filter(email=email).exists():
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
                se_user = User(email=email, password=password, authority='visitor')
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
            user = User.objects.filter(email=email).first()
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


# -----------------------------------------------------------------------------------------------------------------------------------