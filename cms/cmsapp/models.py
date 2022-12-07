
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name
class Course(models.Model):
    
    title = models.CharField(max_length =200)
    category = models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True,default=1)
    image = models.ImageField(upload_to = 'img')
    slug= models.SlugField(unique = True)
    created = models.DateTimeField(auto_now_add = True)
 
    def __str__(self):
        return self.title
    @staticmethod
    def get_all_product_by_id(category_id):
        if category_id:
            return Course.objects.filter(category = category_id)
        else:
            return Course.objects.all()
            
        

class lessons(models.Model):
    title = models.CharField(max_length= 200)
    Course = models.ForeignKey(Course,on_delete = models.CASCADE)
    body = RichTextUploadingField(blank = True,null = True)
    created = models.DateTimeField(auto_now_add = True)
    lesson_number = models.IntegerField(null = False,default = 1)
    id = models.AutoField(primary_key = True,null = False)



    def __str__(self):
        return self.title

class Person(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default= False)

    def __str__(self):
        return self.user.username
class watch_later(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course_id = models.CharField(max_length = 20000,default="")


    

