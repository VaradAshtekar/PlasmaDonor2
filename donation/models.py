from django.db import models

class Donor(models.Model):
    user_id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, default="")
    date_of_birth = models.DateField

    address = models.CharField(max_length=500)
    registration_date = models.DateField()
    city = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    blood_grp = models.CharField(max_length=2)
    covid_recovery_date = models.DateField()
    def __str__(self):
        return self.user_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=10, default="")
    desc = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Centers(models.Model):
    center_id = models.AutoField(primary_key = True)
    center_name = models.CharField(max_length=100)
    center_email = models.EmailField(max_length=70, default="")
    category = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.center_name
