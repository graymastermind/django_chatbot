# chatbot/models.py

from django.db import models

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    user_id = models.CharField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)  # New field for admin status

    def __str__(self):
        return self.username


class Notification(models.Model):
    content = models.TextField()

class Question(models.Model):
    phone_number = models.CharField(max_length=20)
    content = models.TextField()

class Assignment(models.Model):
    subject = models.CharField(max_length=255)
    file_storage = models.CharField(max_length=255)

class AssignmentResult(models.Model):
    subject = models.CharField(max_length=255)
    mark = models.IntegerField()

class ExamDate(models.Model):
    subject_name = models.CharField(max_length=255)
    exam_date = models.DateField()

class AccountInformation(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
