from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    phone_number = models.TextField(max_length=50, unique=True)
    user_id = models.CharField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Notification(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content


class Question(models.Model):
    phone_number = models.CharField(max_length=20)
    content = models.TextField()

    def __str__(self):
        return self.content


class Assignment(models.Model):
    subject = models.CharField(max_length=255)
    file_storage = models.CharField(max_length=255)

    def __str__(self):
        return self.subject


class AssignmentResult(models.Model):
    subject = models.CharField(max_length=255)
    mark = models.IntegerField()

    def __str__(self):
        return f"{self.subject} - Mark: {self.mark}"


class ExamDate(models.Model):
    subject_name = models.CharField(max_length=255)
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.subject_name} - {self.exam_date}"


class ExaminationDate(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.description}"


class AccountInformation(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.phone_number} - Balance: {self.balance}"


class Institution(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name