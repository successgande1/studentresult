from django.contrib import admin
from.models import (SchoolSession,
                    SchoolTerm,
                    SchoolLevel,
                    Subject,
                    Student,
                    StudentLevel,
                    Teacher,
                    FormMaster,
                    SubjectMaster,
                    TermResult,
                    Affective,
                    Psychomotor,
                    Attendance,
                    AnnualResults)

# Register your models here.
admin.site.register(SchoolSession)


admin.site.register(SchoolTerm)


admin.site.register(SchoolLevel)


admin.site.register(Subject)

admin.site.register(Student)


admin.site.register(StudentLevel)


admin.site.register(Teacher)


admin.site.register(FormMaster)


admin.site.register(SubjectMaster)


admin.site.register(TermResult)


admin.site.register(Affective)


admin.site.register(Psychomotor)


admin.site.register(Attendance)


admin.site.register(AnnualResults)
