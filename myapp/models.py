from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=200)
    department_details = models.CharField(max_length=200)

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_details = models.CharField(max_length=200)
    DEPARTMENT = models.ForeignKey(Department, on_delete=models.CASCADE)
    fee = models.CharField(max_length=200)
    total_semester = models.CharField(max_length=200)

class Staff(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    DEPARTMENT = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    house_name = models.CharField(max_length=200)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    image = models.CharField(max_length=900)
    qualification = models.CharField(max_length=900)
    experience = models.CharField(max_length=900)
    gender = models.CharField(max_length=900)

class Hod(models.Model):
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)

class Subject(models.Model):
    sub_name = models.CharField(max_length=200)
    sub_details = models.CharField(max_length=200)
    semester = models.CharField(max_length=200)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)

class Subject_staff(models.Model):
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)
    SUBJECT = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=200)

class Student(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    house_name = models.CharField(max_length=200)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    image = models.CharField(max_length=900)
    register_no = models.CharField(max_length=900)
    addmission_no = models.CharField(max_length=900)
    addmission_date = models.CharField(max_length=900)
    parent_name = models.CharField(max_length=900)
    parent_phone = models.CharField(max_length=900)
    semester = models.CharField(max_length=900)
    gender = models.CharField(max_length=900)
    academic_year = models.CharField(max_length=200)

class Chat(models.Model):
    message = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    HOD = models.ForeignKey(Hod,on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(Student,on_delete=models.CASCADE)

class Notification(models.Model):
    academic_year = models.CharField(max_length=200)
    semester = models.CharField(max_length=900)
    amount = models.CharField(max_length=900)
    start_date = models.DateField()
    end_date = models.DateField()
    COURSE = models.ForeignKey(Course,on_delete=models.CASCADE)

class Payment(models.Model):
    payment_method = models.CharField(max_length=900)
    status = models.CharField(max_length=200)
    date = models.CharField(max_length=900)
    STUDENT = models.ForeignKey(Student,on_delete=models.CASCADE)
    NOTIFICATION = models.ForeignKey(Notification,on_delete=models.CASCADE)

class Feedback(models.Model):
    STUDENT = models.ForeignKey(Student,on_delete=models.CASCADE)
    feedback = models.CharField(max_length=900)
    date = models.CharField(max_length=900)
    reply = models.CharField(max_length=900)
    status = models.CharField(max_length=900)
