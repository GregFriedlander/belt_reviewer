from __future__ import unicode_literals
import bcrypt
import re
from django.db import models

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UsersManager(models.Manager):
    def validate_reg(self, post_data):
        errors = {}
        if len(post_data['name']) < 1:
            errors['name'] = "Please enter a Name into the name field"
        if len(post_data['alias']) < 1:
            errors['alias'] = "Please enter an Alias"
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "Please enter a valid Email"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if post_data['password'] != post_data['password_confirm']:
            errors['password_conf'] = "Please confirm your password correctly"
        if Users.objects.filter(email=post_data['email']):
            errors['email_exists'] = "Sorry but that email address is already in use"
        return errors
    
    def validate_login(self, post_data):
        user_to_check = Users.objects.get(email=post_data['email'])
        if user_to_check:
            if bcrypt.checkpw(post_data['password'].encode(), user_to_check.password.encode()):
                user = {
                    "user": user_to_check
                }
                return user
            else:
                errors = {
                    "error": "Login Invalid"
                }
                return errors
        else:
            errors = {
                "error": "Login Invalid"
            }
            return errors
        
        

class Users(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()

class Authors(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Authors, related_name="books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Reviews(models.Model):
    desc = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(Users, related_name="users")
    book = models.ForeignKey(Books, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)




