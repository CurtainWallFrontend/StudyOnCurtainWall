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
    time = models.DateTimeField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    device = models.ForeignKey(Device, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'log'
        unique_together = (('id', 'time', 'x', 'y', 'z', 'device'),)


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    password = models.CharField(max_length=45)
    authority = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'user'
