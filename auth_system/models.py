from django.db import models
from django.contrib.auth.models import User
from pymongo import MongoClient

client = MongoClient('mongodb+srv://capstonesummer1:9Q8SkkzyUPhEKt8i@cluster0.5gsgvlz.mongodb.net/')
db = client['Product_Comparison_System'] 
user_collection = db['Users']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    purpose = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.png')  # Add this field


    # Add any other fields you need

    def __str__(self):
        return self.user.username

class MongoDBUser:
    def __init__(self, username, email, password, fname, lname, gender, birthday, age, purpose):
        self.username = username
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname
        self.gender = gender
        self.birthday = birthday
        self.age = age
        self.purpose = purpose

    def save(self):
        user_collection.insert_one({
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'fname': self.fname,
            'lname': self.lname,
            'gender': self.gender,
            'birthday': self.birthday,
            'age': self.age,
            'purpose': self.purpose
        })

    @classmethod
    def find_by_username(cls, username):
        return user_collection.find_one({'username': username})