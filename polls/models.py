from django.db import models
from django.utils import timezone
import datetime

class Poll(models.Model):
    key = models.CharField(max_length=50, unique=True, 
                           help_text="Unique identifier for this poll.")
    published = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.key

class Question(models.Model):
    poll = models.ForeignKey(Poll)
    label = models.CharField(max_length=200)

    class Meta:
        order_with_respect_to = 'poll'

    def __unicode__(self):
        return self.label

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)

    class Meta:
        order_with_respect_to = 'question'    

    def __unicode__(self):
        return self.choice_text

class Answer(models.Model):
    choice = models.ForeignKey(Choice)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return str(self.created)


