from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9copy.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors={}
		if len(postData['first_name']) < 2:
			errors['first_name'] = "First name cannot be less than 2 characters"
		elif len(postData['last_name']) < 2:
			errors['last_name'] = "Last name cannot be less than 2 characters"
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Invalid email"
		elif len(postData['password1']) < 8:
			errors['password1'] = "Invalid password"
		elif postData['password1'] != postData['password2']:
			errors['password2'] = "Passwords do not match"
		return errors

	def login_validation(self, postData):
		errors={}
		user = User.objects.get(email = postData['loginemail'])
		if not bcrypt.checkpw(postData['loginpw'].encode(), user.password.encode()):
			errors['fail'] = "Cannot log in"
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

	objects=UserManager()