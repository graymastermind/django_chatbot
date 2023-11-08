
from django.contrib import admin
from .models import User, Notification, Question, Assignment, AssignmentResult, ExamDate, AccountInformation, \
    Institution

admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Question)
admin.site.register(Assignment)
admin.site.register(AssignmentResult)
admin.site.register(ExamDate)
admin.site.register(AccountInformation)
admin.site.register(Institution)

