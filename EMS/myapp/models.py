from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
# group = (
#     ('1','A+'),
#     ('2','O+'),
#     ('3','B+'),
#     ('4','AB+'),
#     ('5','A-'),
#     ('6','O-'),
#     ('7','B-'),
#     ('8','AB-'),
# )
# class Employee(models.Model):
#     # Employee_name = models.CharField(max_length = 30,blank = True)
#     # Email = models.EmailField()
#     Contact_Number = models.IntegerField()
#     Emergency_ContactNumber = models.IntegerField()
#     Position = models.CharField(max_length=100,blank=True)
#     MaritalStatus = models.CharField(max_length=100,blank=True)
#     Blood_Group = models.CharField(max_length=50,choices=group)
#     JobTitle = models.CharField(max_length=100, blank=True)
#     WorkLocation = models.CharField(max_length=150, blank=True)
#     # DateOfJoining = models.DateField()
#     Reporting_to = models.CharField(max_length =100, blank=True)
#     Linkedin_link = models.URLField()
#     profile_pic = models.ImageField(upload_to="media/",blank=True, null=True)
    

#     def __str__(self):
#         return self.Employee_name

class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    reporting_to = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    contact_number = models.CharField(max_length=12)
    emergency_contact_number = models.CharField(max_length=12)
    position = models.CharField(max_length=100,blank=True)
    marital_status = models.CharField(max_length=100,blank=True)
    blood_group = models.CharField(max_length=10)
    job_title = models.CharField(max_length=100, blank=True)
    work_location = models.CharField(max_length=150, blank=True)
    linkedin_link = models.URLField()
    profile_pic = models.ImageField(upload_to="media/",blank=True, null=True)
    dob = models.DateField(null= True, blank=True)
    date_of_join=models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Leave(models.Model):

    employee_name = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    apply_date= models.DateField()
    nature_of_leave= models.CharField(max_length=100)
    first_day= models.DateField()
    last_day= models.DateField()
    number_of_days= models.PositiveIntegerField()
    status= models.CharField(max_length=100,default="pending")

    