from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

# Create your models here.
class userpermission(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    is_student = models.BooleanField(default = False)
    is_counsellor = models.BooleanField(default = False)
    is_faculty = models.BooleanField(default = False)  
    def __str__(self):
        return self.user.username + ' premissions' 
class permittedlist(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    allowed = models.ManyToManyField("permittedlist")
    def __str__(self):
        return str(self.user.username)

    def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
        if created:
            try:
                Profile.objects.create(user=instance)
            except:
                pass
    post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
class resolvedlist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    resolved = models.ManyToManyField("resolvedlist")
    def __str__(self):
        return str(self.user.username)