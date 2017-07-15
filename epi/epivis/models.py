from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    basemount_point = models.CharField(max_length=5000)
    #cache_path = models.CharField(max_length=5000)
    username_linux = models.CharField(max_length=30,unique=True,default='')
    password_linux = models.CharField(max_length=30,unique=True,default='')

class Project(models.Model):
    projectid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Sample(models.Model):
    sampleid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    projectid = models.ForeignKey(Project,on_delete=models.CASCADE)

class File(models.Model):
    fileid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    mate = models.IntegerField(default=-1)
    sampleid = models.ForeignKey(Sample, on_delete = models.CASCADE)
    feature = models.CharField(max_length=200)
    #sample          ForeignKey to sample



# Create your models here.
