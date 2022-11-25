from django.db import models
import os

# Create your models here.
class Student(models.Model):
  student_number = models.PositiveIntegerField(null=True)
  image = models.ImageField(upload_to='images/',null=True)
  first_name = models.CharField(max_length=50, null=True)
  last_name = models.CharField(max_length=50, null=True)
  email = models.EmailField(max_length=100, null=True)
  field_of_study = models.CharField(max_length=50, null=True)
  gpa = models.FloatField(null=True)

  def __str__(self):
    return f'{self.image.path}'

  def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
  
# class TimesheetHistory(models.Model):
#   student_number = models.PositiveIntegerField()
#   lastChecked = models.

#   def __str__(self):
#     return f'Student: {self.first_name} {self.last_name}'
