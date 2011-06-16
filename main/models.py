from django.db import models
from django.contrib.auth.models import User  

class Msg(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100,blank=True)    
    content = models.TextField()
    date = models.DateTimeField()
    fav = models.ManyToManyField(User,related_name = 'fav',blank=True)
    fav_num = models.IntegerField(default=0)
    reply_msg = models.IntegerField(blank=True,null=True)
    reply_user = models.IntegerField(blank=True,null=True)
    
    def __unicode__(self):
        return self.content
        
class UserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)

    # The rest is completely up to you...
    profile_img = models.ImageField(upload_to='profile_img',default='profile_img/default.jpg')