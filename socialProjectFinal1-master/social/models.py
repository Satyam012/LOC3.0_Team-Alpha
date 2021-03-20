from django.db import models
from django.core.validators import FileExtensionValidator
class Post(models.Model):
    username = models.CharField(max_length = 120,null = True)
    desription= models.TextField(null = True)
    image = models.FileField(null= True,blank = True,validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])] )
    date = models.DateTimeField()
# Create your models here.
