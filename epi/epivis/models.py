from django.db import models

class User(models.Model):
    #userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    basemount_point = models.CharField(max_length=5000)
    #cache_path = models.CharField(max_length=5000)
    username_linux = models.CharField(max_length=30,unique=True,default='')
    password_linux = models.CharField(max_length=30,unique=True,default='')

class Project(models.Model):
    #projectid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)

class Sample(models.Model):
    #sampleid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    projectid = models.ForeignKey(Project,on_delete=models.CASCADE)

class File(models.Model):
    name = models.CharField(max_length=200,unique=True)
    mate = models.IntegerField(default=-1)
    sampleid = models.ForeignKey(Sample,on_delete = models.CASCADE)
    feature = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    viewer = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    createby = models.CharField(max_length=200)
    ancester = models.CharField(max_length=200,null=True)
    #sample          ForeignKey to sample

class Jobs(models.Model):
    cmd = models.CharField(max_length=300)
    priority = models.IntegerField()
    status = models.IntegerField()
    fullcmd = models.CharField(max_length=500)
    input = models.CharField(max_length=200,null=True)
    output = models.CharField(max_length=200,null=True)
    out = models.TextField()
    err = models.TextField()

class software(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField()
    document_json = models.CharField(max_length=200)
    input = models.IntegerField()
    output = models.IntegerField()
    

# Create your models here.
