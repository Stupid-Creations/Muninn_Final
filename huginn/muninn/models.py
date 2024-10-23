import time
from django.db import models
from django.contrib.auth.models import User

#  function to generate a dynamic timestamp
def generate_timestamp():
    return time.strftime("%Y%H%M%S%d")

# Function to generate a upload path based on the timestamp
def get_upload_path(instance, filename):
    return 'uploads/{}/{}'.format(instance.t, filename)

class Chapter(models.Model):
    #rendered information
    grade = models.CharField(max_length=100, default="Enter your grade")
    subject = models.CharField(max_length=100, default="Enter your subject")
    chapter = models.CharField(max_length=100, default="Chapter Name")

    sut = models.CharField(max_length=10000, default='NOT INITIALIZED')

    #stored information
    t = models.CharField(max_length=100, default=generate_timestamp)  #
    identity = models.IntegerField(default=0)  

    pdf = models.FileField(upload_to=get_upload_path) 
    fa = models.JSONField(default=list)  # Store list of answers
    fq = models.JSONField(default=list)  # Store list of questions

    questions = models.JSONField(default = list)
    answers = models.JSONField(default = list)
    grades = models.JSONField(default = list)
    remarks = models.JSONField(default = list)


    counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.identity:
            self.identity = int(self.t)  # Override inbuilt save function to set identity
        super().save(*args, **kwargs)

