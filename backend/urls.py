from django.urls import path
from backend.views import GetImg
# from backend.views import UploadCsv
# from backend.views import FilterOutlier
from backend.views import VibrationData
from backend.views import SendMail

from backend.views import DeviceAPI

urlpatterns = [
    #path('对应url', 模块名.as_view({'请求类型': 'views.py中对应的函数名'})
    path('saveimage/', GetImg.as_view({'post': 'save_image'})),
    path('vibration/uploadCsv/', VibrationData.as_view({'post':'save_csv'})),
    path('vibration/filterOutlier/', VibrationData.as_view({'post':'filter_outlier'})),
    path('vibration/searchAbnormal/', VibrationData.as_view({'post':'search_abnormal'})),
    path('vibration/sendMail/', SendMail.as_view({'post': 'send_mail'})),
    path('vibration/getDevice/',DeviceAPI.as_view({'get':'get_device'})),
    path('vibration/addDevice/', DeviceAPI.as_view({'get': 'add_device'})),
    path('vibration/deleteDevice/', DeviceAPI.as_view({'get': 'delete_device'})),
    path('vibration/saveAbnormal/', VibrationData.as_view({'post': 'save_abnormal'}))
]
