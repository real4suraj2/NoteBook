from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.SET_DEFAULT,default='')
    description = models.CharField(max_length=100, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    website = models.URLField(default='', blank=True)
    phone = models.IntegerField(default=0, blank=True)
    image = models.URLField(default='', blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class NoteCategory(models.Model):
    note_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200, default=1)
    
    CATEGORY_PIC = [ ('classwork','Class Work!'),('projectwork','Project Work!'),('labwork','Laboratory Work'),('explore','Explore the world!')]
    category_image = models.CharField(max_length=50,choices = CATEGORY_PIC, default = 'classwork')
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.note_category

class NoteSeries(models.Model):
    note_series = models.CharField(max_length=200)
    note_category = models.ForeignKey(NoteCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)
    series_image = models.TextField(default = 'https://source.unsplash.com/random/400x350')
    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.note_series

class Note(models.Model):
	note_title = models.CharField(max_length = 250)
	note_content = models.TextField(default = "")
	note_published = models.DateTimeField("date published",default = timezone.now())
	note_series = models.ForeignKey(NoteSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
	note_slug = models.CharField(max_length=200, default=1)
	
	def __str__(self):
		return self.note_title
		