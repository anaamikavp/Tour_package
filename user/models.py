from django.db import models


# Create your models here.
class register_table(models.Model):
    #id will be created automatically
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email=models.CharField(max_length=90)
    password=models.CharField(max_length=50)
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    user_type=models.CharField(default=None, max_length=30)

    class Meta:
        db_table="registration"

