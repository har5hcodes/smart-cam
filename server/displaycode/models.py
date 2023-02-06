# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

#A model for code snippet pasted by user.
#related_name: https://stackoverflow.com/questions/40329196/how-to-list-related-objects-in-django-rest-framework
class Snippet(models.Model):    
    author = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE,
      null=True,
      related_name="snippets"
    )
    title = models.TextField(default="codeforreview")
    text = models.TextField()
    #This could be an enum but for now, I will go with the simpler string.
    language = models.TextField(default="clike")
    def __str__(self):
            return "id:"+str(self.id)+"~"+"title:"+str(self.title)+"~text:"+str(self.text[:40])


class Comment(models.Model):
    author = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE,
      null=True
    )
    #By default just assume it belongs to first Snippet
    snippetId = models.IntegerField()
    text = models.TextField()
    line = models.IntegerField(default=-1)
    #Not interested in create data right now
    #Flicked from https://tutorial.djangogirls.org/en/django_models/
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        #return "id:"+str(self.id)+"~"+"linenum:"+str(self.linenum)+"~"+"text:"+self.text
        return "id:"+str(self.id)+"~"+"snippetId:"+str(self.snippetId)+"~"+"line:"+str(self.line)+"~"+"text:"+self.text


class WaitListUser(models.Model):
    email = models.EmailField(max_length=254)
    #Choose a username. We will try reserve it when the site becomes live.
    username = models.TextField();
    #Add information about yourself. 
    # If you are a candidate, then add how many years of experience you have, technologies experienced in, 
    # what position you are interviewing for, linkedin/github urls, resume link etc. 
    #Also add what you would like to gain from this website and any suggestion/feature requests.
    # If you are a code reviewer/hiring manager, then add how many years of experience you have, what is your current position
    # what is your current position, what technologies are you recruiting for? Add linkedin/github URLs.
    # Feel free to communicate with developers of interviewblindspots.com through this field.
    #Also add what you would like to gain from this website and any suggestion/feature requests.
    aboutme = models.TextField(); 
    #Add information on what you features are missing and what would like to see in current interview preparation sites.
    #You can also add what annoys you about current interview preparation sites.
    painpoints = models.TextField(blank=True, null=True);
    #When did the person join the wait list.
    joinedDate = models.DateTimeField(blank=True, null=True)
    #which website did the user join us from?
    referralUrl = models.TextField(null=True)

    def __str__(self):
        #return "id:"+str(self.id)+"~"+"linenum:"+str(self.linenum)+"~"+"text:"+self.text
        return "id:"+str(self.id)+"~"+"email:"+str(self.email)+"~"+"username:"+str(self.username)+"~"+"aboutme:"+str(self.aboutme)+"~"+"painpoints:"+str(self.painpoints)+"~"+"joinedDate:"+str(self.joinedDate)+"~"+"referralUrl:"+str(self.referralUrl)


class Camera(models.Model):
  camId = models.IntegerField(max_length=500)
  camUrl = models.URLField()
  camLoc = models.TextField(blank=True)

  # https://dev.to/thepylot/how-to-add-tags-to-your-models-in-django-django-packages-series-1-3704
  # in case if we want metadata as tags 
  metadata = models.TextField(blank=True)  

  def __str__(self): 
        return "camId:"+str(self.camId)+"~"+"camUrl:"+str(self.camUrl)+"~"+"camLoc:"+str(self.camLoc)+"~"+"metadata:"+str(self.metadata) 
  
class SnapshotDetails(models.Model):
  snapshotId = models.IntegerField()
  dirLoc = models.TextField()
  capturedTime = models.DateTimeField(blank=True, null=True)
  camera = models.ForeignKey(
      'Camera',
      on_delete=models.CASCADE,
      null=False
    )
 
  def __str__(self): 
        return "snapshotId:"+str(self.snapshotId)+"~"+"snapshotId:"+str(self.snapshotId)+"~"+"capturedTime:"+str(self.capturedTime)+"~"+"camera:"+str(self.camera) 



