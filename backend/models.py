from django.db import models

# Create your models here.
class Image(models.Model):
    func = models.CharField(blank=False,null=False,max_length=100,choices=[('A', 'segmentation'), ('B', 'explosion_identify')])
    image = models.FileField(upload_to='uploads/')

    class Meta:
        app_label = 'backend'
    def __str__(self):
        return self.name
    

class title(models.Model):  #定义一个文章类 title
    title=models.CharField(max_length=20)   #文章名
    address=models.CharField(max_length=20)  #地址
