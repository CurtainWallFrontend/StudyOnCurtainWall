# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Image(models.Model):
    func = models.CharField(blank=False,null=False,max_length=100,choices=[('A', 'segmentation'), ('B', 'explosion_identify')])
    image = models.FileField(upload_to='uploads/')

    class Meta:
        app_label = 'backend'
    def __str__(self):
        return self.name


class Abnormal(models.Model):
    time = models.DateTimeField(primary_key=True, db_comment='数据采集时间')  # The composite primary key (time, device_id, min, max, last_modified, data, direction) found, that is not supported. The first column is selected.
    device = models.ForeignKey('Device', models.DO_NOTHING, db_comment='传感器编号')
    min = models.FloatField(db_comment='阈值下限')
    max = models.FloatField(db_comment='阈值上限')
    last_modified = models.DateTimeField(db_comment='上次修改时间')
    data = models.FloatField(db_comment='异常值数据值')
    direction = models.CharField(max_length=255, db_comment='数据方向(x/y/z)')

    class Meta:
        managed = True
        db_table = 'abnormal'
        unique_together = (('time', 'device', 'min', 'max', 'last_modified', 'data', 'direction'),)



class Building(models.Model):
    building_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'building'


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=30, blank=True, null=True)
    building = models.ForeignKey(Building, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'device'

class Log(models.Model):
    time = models.DateTimeField(primary_key=True, db_comment='采集数据时间')  # The composite primary key (time, x, y, z, device_id) found, that is not supported. The first column is selected.
    x = models.FloatField(db_comment='x方向数据')
    y = models.FloatField(db_comment='y方向数据')
    z = models.FloatField(db_comment='z方向数据')
    device = models.ForeignKey(Device, models.DO_NOTHING, db_comment='传感器编号')

    class Meta:
        managed = True
        db_table = 'log'
        unique_together = (('time', 'x', 'y', 'z', 'device'),)


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    password = models.CharField(max_length=45)
    authority = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'user'
