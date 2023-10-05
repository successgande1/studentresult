from django.db import models
from django.contrib.auth.models import User
from accounts.models import BusinessAccount


# Create your models here.
class SchoolSession(models.Model):
    sess = models.CharField(max_length=100, null=False)
    organization = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.sess


class SchoolTerm(models.Model):
    TERM_CATEGORY = [
        ('first term', 'First Term'),
        ('second term', 'Second Term'),
        ('third term', 'Third Term'),
    ]
    term_name = models.CharField(choices=TERM_CATEGORY, max_length=50,blank=False, null=True)
    organization = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.term_name


class SchoolLevel(models.Model):
    LEVEL_CATEGORY = [
        ('jss', 'JSS'),
        ('sss', 'SSS'),
    ]

    LEVEL_NAME = [
        ('jss1', 'JSS1'),
        ('jss2', 'JSS2'),
        ('jss3', 'JSS3'),
        ('sss1', 'SSS1'),
        ('sss2', 'SSS2'),
        ('sss3', 'SSS3'),
    ]

    LEVEL_ARM = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
        ('f', 'F'),
        ('g', 'H'),
    ]
    organization = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    level = models.CharField(choices=LEVEL_NAME, max_length=50, blank=False, null=True)
    level_arm = models.CharField(choices=LEVEL_ARM, max_length=50, blank=False, null=True)
    category = models.CharField(choices=LEVEL_CATEGORY, max_length=50, blank=False, null=True)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Class: {self.level} - {self.level_arm} in  {self.category}'


class Subject(models.Model):
    organization = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=False)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    organization = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    student_id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    added_date = models.DateField(auto_now_add=True, null=True, blank=True)
    current_level = models.ForeignKey(SchoolLevel, on_delete=models.SET_NULL, null=True, blank=True)
    updated_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f'{self.studid} - {self.user.profile.surname}'


class StudentLevel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.student} - {self.level}'


class Teacher(models.Model):
    QUALIFICATION_CHOICES = [
        ('b.sc', 'B.SC'),
        ('nce', 'NCE'),
        ('pgde', 'PGDE'),
        ('nd', 'ND'),
        ('ond', 'OND'),
        ('ssce', 'SSCE'),
        ('hnd', 'HND'),
    ]
    organization = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    teacher_id = models.CharField(max_length=20, primary_key=True)
    specialization = models.CharField(max_length=50, blank=False, null=True)
    qualification = models.CharField(choices=QUALIFICATION_CHOICES, max_length=50, blank=False, null=True)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.profile.surname} - {self.qualification} - {self.specialization}'


class FormMaster(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    level = models.ForeignKey(StudentLevel, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher


class SubjectMaster(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    term = models.ForeignKey(SchoolTerm, on_delete=models.CASCADE)
    level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Teacher Name: {self.teacher} Subject:- {self.subject} Term:- {self.term}'


class TermResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    term = models.ForeignKey(SchoolTerm, on_delete=models.CASCADE)
    student_level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ca1 = models.IntegerField(null=True)
    ass1 = models.IntegerField(null=True)
    test1 = models.IntegerField(null=True)
    project = models.IntegerField(null=True)
    ca2 = models.IntegerField(null=True)
    ass2 = models.IntegerField(null=True)
    test2 = models.IntegerField(null=True)
    ca3 = models.IntegerField(null=True)
    ass3 = models.IntegerField(null=True)
    exam = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    position = models.IntegerField(null=True)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.student} Academic Session- {self.sess}  Term:- {self.term} Level:- {self.student_level} - {self.subject}'


class Affective(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    term = models.ForeignKey(SchoolTerm, on_delete=models.CASCADE)
    pclass = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    trait = models.CharField(max_length=50, null=False)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.student}'


class Psychomotor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    term = models.ForeignKey(SchoolTerm, on_delete=models.CASCADE)
    pclass = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    trait = models.CharField(max_length=50, null=False)
    rating = models.IntegerField()
 
    def __str__(self):
        return f'{self.student}'


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    term = models.ForeignKey(SchoolTerm, on_delete=models.CASCADE)
    pclass = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    total = models.IntegerField()
    obtained = models.IntegerField()
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.student} - {self.sess} - Term: {self.term} - Class: {self.pclass} - Total: {self.total}'


class AnnualResults(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sess = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    pclass = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term1 = models.IntegerField(null=True)
    term2 = models.IntegerField(null=True)
    term3 = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    position = models.IntegerField(null=True)
    added_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.student
