from django.db import models


class SEUser(models.Model):
    email = models.CharField(primary_key=True)
    password = models.CharField(max_length=255)
    authority = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'  # 指定数据库表的名称，与现有表名保持一致
        app_label = 'userAuthority'

