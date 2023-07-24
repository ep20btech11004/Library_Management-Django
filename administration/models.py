from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, Q
import datetime


# Create your models here.
class Login(AbstractUser):
    is_subadmin = models.BooleanField(default = False)
    is_librarian = models.BooleanField(default = False)
    is_customer = models.BooleanField(default = False)

class Book(models.Model):
    name = models.CharField(max_length = 25)
    author = models.CharField(max_length = 15)
    isbn = models.PositiveBigIntegerField(unique = True)
    copies = models.PositiveSmallIntegerField()
    rel_date = models.DateField()
    genre = models.CharField(max_length = 100)
    lang = models.CharField(max_length = 10)
    description = models.TextField(default = '')
    image = models.ImageField(upload_to = "books", null = True)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(rel_date__lte = datetime.date.today()), 
                name = 'Release Date',
                violation_error_message='Invalid Release Date',
            ),
        ]
    
class Customer(models.Model):
    user = models.OneToOneField(Login, on_delete = models.CASCADE, related_name = 'customer')
    fine = models.IntegerField(default = 0)
    name = models.CharField(max_length = 20)
    occupation = models.CharField(max_length = 15)
    age = models.PositiveSmallIntegerField()
    roll_no = models.CharField(max_length = 15, unique = True)
    email = models.EmailField(max_length = 20, unique = True)
    contact = models.IntegerField(null = True)
    gender = models.CharField(max_length = 10)
    image = models.ImageField(upload_to = "customer", null = True)

    def __str__(self):
        return self.name

class SubAdmin(models.Model):
    user = models.OneToOneField(Login, on_delete = models.CASCADE, related_name = 'subadmin')
    name = models.CharField(max_length = 20)
    contact = models.IntegerField(unique = True)
    age = models.PositiveSmallIntegerField() 
    gender = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 20, unique = True)
    image = models.ImageField(upload_to = 'subadmin', null = True) 

    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    user = models.OneToOneField(Login, on_delete = models.CASCADE, related_name = 'librarian')
    name = models.CharField(max_length = 20)
    contact = models.IntegerField(unique = True)
    age = models.PositiveIntegerField()
    designation = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 20, unique = True)
    image = models.ImageField(upload_to = "librarian", null = True)

    def __str__(self):
        return self.name
    
class Reserve(models.Model):
    user = models.ForeignKey(Login, on_delete = models.CASCADE, related_name = 'cust')
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = 'issued_book')
    valid_till = models.DateField()
    status = models.CharField(max_length = 10)
    fine = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

class Configure(models.Model):
    fine = models.IntegerField()
    hike = models.IntegerField()
    interval = models.PositiveIntegerField()
    issue_till = models.PositiveIntegerField()
    reserve_till = models.PositiveIntegerField()

    def __str__(self):
        return "conf"

class Message(models.Model):
    sender = models.ForeignKey(Login, on_delete = models.CASCADE, related_name = 'sender', null = True)
    receiver = models.ForeignKey(Login, on_delete = models.CASCADE, related_name = 'receiver')
    contact = models.IntegerField(null = True)
    message = models.CharField(max_length = 30)
    time =models.DateField(null = True)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.time

class Organization(models.Model):
    name = models.CharField(max_length = 30)
    estd = models.DateField()
    contact = models.IntegerField()
    building = models.CharField(max_length = 30)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    country = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class Genre(models.Model):
    genre = models.CharField(max_length = 10)

    def __str__(self):
        return self.genre
    
class Language(models.Model):
    lang = models.CharField(max_length = 10)

    def __str__(self):
        return self.lang

class Occupation(models.Model):
    occupation = models.CharField(max_length = 10)

    def __str__(self):
        return self.occupation
    
class Int(models.Model):
    num = models.IntegerField()




    
