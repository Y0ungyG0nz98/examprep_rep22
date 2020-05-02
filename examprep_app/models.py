from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    
    def registrationValidator(self, forminfo):
        validationErrors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        print('printing forminfo in validator function')
        print(forminfo)
        if len(forminfo['fname']) < 2:
            validationErrors['firstName'] = "Come'on SON! First name must be at least 2 characters"
        if len(forminfo['lname']) < 2:
            validationErrors['lastname'] = "Oye! Last name must be at least 2 characters"
        if len(forminfo['email']) < 1:
            validationErrors['email'] = " Yo' Email is required SON!"
        elif not EMAIL_REGEX.match(forminfo['email']):
            validationErrors['emailformat'] = "Errrr!!!: Email is invalid"
        else:
            usersWithEmail = User.objects.filter(email = forminfo['email'])
            print("printing users with email now")
            print(usersWithEmail)
            if len(usersWithEmail)>0:
                validationErrors['emailTaken'] = "Email is already taken bro, git yo-self another email address!"
        if len(forminfo['pw']) < 8:
            validationErrors['password'] = "Yo collar boy! Password must be at least 8 characters"
        if forminfo['pw'] != forminfo['cpw']:
            validationErrors['confirm'] = "Password and confirm password must be a match"

        return validationErrors

    def loginValidator(self, forminfo):
        errors = {}
        if len(forminfo['email']) < 1:
            errors['email'] = "Email is required"
        emailsExist = User.objects.filter(email = forminfo['email'])
        print(emailsExist)
        if len(emailsExist)== 0:
            errors['emailNotFound'] = "This email was not found. Please register first."
        else:
            user = emailsExist[0]

            if not bcrypt.checkpw(forminfo['pw'].encode(), user.password.encode()):
                errors['pw'] = "That Password don't match"

        return errors



class ItemManager(models.Manager):
    def validateItem(self, forminfo):
        errors = {}
        if len(forminfo['itemName'])<1:
            errors['itemNameRequired']= "Hey YOU! Item name is required"
        elif len(forminfo['itemName'])<4:
            errors['itemNameShort']= "TOO SMALL BRO'! Item name needs to be at least 4 characters!"
        print(errors)
        return errors


class User(models.Model):
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Item(models.Model):
    name = models.CharField(max_length = 255)
    uploader = models.ForeignKey(User, related_name = 'items_uploaded', on_delete = models.CASCADE)
    favoritor = models.ManyToManyField(User, related_name ='fav_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
