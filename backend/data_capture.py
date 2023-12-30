import csv
import math
import os
import shutil
import sys

from datetime import datetime, timedelta
from sqlite3 import IntegrityError

import requests
import zipfile
import pandas as pd

import mysql.connector
from mysql.connector import Error

# 文件夹路径
root_path = './media/temp_file/'

# 登录信息
login_url = 'https://diggerinspection.cn/doLogin'
login_payload = {
    'username': 'lu',
    'password': 'tj221204'
}

# 数据库连接信息
db_user = 'root'
db_password = 'TJtj123123'
db_host = '1.117.76.28'
db_port = 3306
database = 'mydb'

# 提取device_id和device_name到一个列表中
device_list = []


# 设置阈值
min = -0.5
max = 0.5


def get_all_devices(cursor):
    # 执行SQL查询
    query = "SELECT device_id, device_name FROM device"
    cursor.execute(query)

    # 获取所有数据记录
    device_records = cursor.fetchall()

    global device_list
    # 将数据记录组装成字典列表
    device_list = [{"device_id": device[0],
                    "device_name": device[1]}
                   for device in device_records]


# 清空文件夹
def clear_dir(path):
    for filename in os.listdir(path):
        # 构造文件或文件夹的绝对路径
        file_path = os.path.join(path, filename)
        try:
            # 如果是文件，则删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # 如果是文件夹，则删除整个文件夹
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# 数据平滑
def data_smoothing(data, num_parts):
    n = len(data)
    chunk_size = n // num_parts  # 每份大小
    result = []
    if n == 0:
        return result
    if chunk_size == 0:
        chunk = data
        average = sum(chunk) / len(chunk)
    else:
        for i in range(0, n, chunk_size):
            chunk = data[i:i + chunk_size]
            average = sum(chunk) / len(chunk)
            result.append(average)
    return result


# 将csv文件的数据平滑后保存到数据log表中
def save_log(cursor, connection, filename, extracted_dir_path, start_time, equipment):

    # 读取csv文件
    csv_file_path = extracted_dir_path + '/' + filename

    # 从保存的.csv文件中读取数据并返回前端
    x_data = []
    y_data = []
    z_data = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            x_data.append(float(row[0].strip()))
            y_data.append(float(row[1].strip()))
            z_data.append(float(row[2].strip()))

    # 调用save_abnormal函数保存异常值
    save_abnormal(cursor, connection, start_time, equipment, x_data, y_data, z_data)

    parts = 600
    x_data = data_smoothing(x_data, parts)
    y_data = data_smoothing(y_data, parts)
    z_data = data_smoothing(z_data, parts)

    # 构建插入数据SQL
    query = "INSERT INTO log (time, x, y, z, device_id) VALUES (%s, %s, %s, %s, %s)"

    # 待插入数据记录
    records = []
    for i in range(parts):
        time = start_time + timedelta(seconds=i)
        record = (time, x_data[i], y_data[i], z_data[i], equipment["device_id"])
        records.append(record)

    # 保存到数据库
    try:
        # 批量插入数据
        cursor.executemany(query, records)
        connection.commit()
        print("insert logs successfully with " + equipment["device_name"])
    except Exception as e:
        print("insert logs error with " + equipment["device_name"], e)


# 筛选出其中的异常值保存在数据abnormal表中
def save_abnormal(cursor, connection, timestamp, equipment, x_list, y_list, z_list):
    # 筛选异常值
    x_abnormal = [x for x in x_list if x < min or x > max]
    y_abnormal = [y for y in y_list if y < min or y > max]
    z_abnormal = [z for z in z_list if z < min or z > max]

    # 构建插入数据SQL
    query = "INSERT INTO abnormal " \
            "(last_modified, device_id, min, max, direction, data, time) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"

    # 待插入记录列表

    def insert_data(datalist, type):
        records = []
        time = timestamp
        print(time)
        for i in range(len(datalist)):
            time = time + timedelta(seconds=int(i*0.01))
            record = (datetime.now(),
                      equipment["device_id"],
                      min,
                      max,
                      type,
                      datalist[i],
                      time
            )
            if record in records:
                continue
            else:
                records.append(record)

        try:
            # 批量插入数据
            cursor.executemany(query, records)
            # 要提交事务!!!
            connection.commit()
            print(type + "——Insert abnormal records successfully with " + equipment["device_name"] )
        except Exception as e:
            print(type + "——Insert error: insert abnormal with " + equipment["device_name"], e)

    insert_data(x_abnormal,'x')
    insert_data(y_abnormal,'y')
    insert_data(z_abnormal,'z')




# 使用账号密码爬取网站数据
def capture_csv(cursor, connection):

    # 获取时间
    now = datetime.now()
    f_date = now.strftime("%Y-%m-%d %H:%M:%S")
    ten_minutes_ago = now - timedelta(minutes=10)
    s_date = ten_minutes_ago.strftime("%Y-%m-%d %H:%M:%S")

    # 创建一个session对象，它会保存所有的请求和响应，使得你可以在多个请求之间保持某些参数。
    s = requests.Session()
    # 用用户名和密码登录网站
    login_req = s.post(login_url, data=login_payload)

    # 检查是否登录成功
    if login_req.status_code == 200:
        print("Login successfully.")
    else:
        print("Login failed.")

    # anomaly_data_list = []
    for device in device_list:
        download_url = 'https://diggerinspection.cn/download/DownloadFile?s_date=' + s_date + '&f_date=' + f_date + \
                       '&device=' + device["device_name"] + '&type=.csv&ip=diggerinspection.cn&channel=0'

        # 发送GET请求
        response = s.get(download_url, stream=True)

        # 检查请求是否成功s
        if response.status_code == 200:
            file = root_path + '/' + device["device_name"] + '.zip'
            # 打开一个新的文件并写入响应内容
            with open(file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("File " + device["device_name"] + ".zip downloaded successfully.")
            # 创建一个ZipFile对象
            with zipfile.ZipFile(file, 'r') as zip_ref:
                extracted_dir_path = root_path + '/' + device["device_name"]
                if not os.path.exists(extracted_dir_path):
                    os.makedirs(extracted_dir_path)
                # 解压文件
                zip_ref.extractall(extracted_dir_path)
                # 获取解压后的文件列表
                file_names = os.listdir(extracted_dir_path)

                for filename in file_names:
                    if filename.endswith('.csv'):
                        # 将文件数据保存到数据库log表中
                        save_log(cursor, connection, filename, extracted_dir_path, ten_minutes_ago, device)
                        print("Device " + device["device_name"] + " data saved successfully.")

        else:
            print("File " + device["device_name"] + ".zip downloaded failed.")


try:
    # 若根目录不存在则新建
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    # 连接MySQL数据库
    cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=database)

    cursor = cnx.cursor()

    # 清空文件夹
    clear_dir(root_path)

    # 获取所有device列表
    get_all_devices(cursor)

    # 从网站下载数据文件
    capture_csv(cursor, cnx)

    clear_dir(root_path)  # 清空暂存文件夹，避免占用内存


except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    # 关闭与数据库的连接
    if cnx is not None and cnx.is_connected():
        cnx.close()
        if cursor is not None:
            cursor.close()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
