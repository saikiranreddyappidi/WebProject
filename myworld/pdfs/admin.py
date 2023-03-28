from django.contrib import admin

from .tables import StudentInfo, Faculty, ApporvedFiles, DeclinedFiles

admin.site.register(StudentInfo)
admin.site.register(Faculty)
admin.site.register(ApporvedFiles)
admin.site.register(DeclinedFiles)
