from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
	owner=models.ForeignKey(User)
	title=models.CharField(max_length=100)
	text=models.CharField(max_length=500)
	createTime=models.DateTimeField()	

from django.forms import ModelForm

class NoteForm(ModelForm):
	class Meta:
		model=Note
		#use "fields=[] in include fields and exclude=[] to exclude fields"
		exclude=["owner"]


from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class NoteResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
        authorization= Authorization()