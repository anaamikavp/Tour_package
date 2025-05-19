from django.db import models

from user.models import register_table


# Create your models here.
class package_table(models.Model):
    #id will be created automatically
    package_name=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    duration=models.CharField(max_length=50)
    price=models.FloatField()
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    description=models.CharField( max_length=150)
    start_date=models.DateField()
    end_date=models.DateField()
    images=models.ImageField(upload_to='images/')
    status=models.CharField(max_length=20)
    vendor_id=models.ForeignKey(register_table,on_delete=models.SET_DEFAULT,default=1)


    class Meta:
        db_table="packages"


class booking_table(models.Model):
    package_id = models.ForeignKey(package_table,on_delete=models.SET_DEFAULT,default=1)
    name = models.CharField(max_length=90, default=None)
    email = models.CharField(max_length=90, default=None)
    phone = models.CharField(max_length=10, default=None)
    no_of_persons = models.IntegerField()
    price = models.FloatField()
    payment_status = models.CharField(max_length=30)
    transaction_id = models.CharField(max_length=90, default="123")
    user_id = models.ForeignKey(register_table, on_delete=models.SET_DEFAULT, default=1)
    booking_status = models.CharField(max_length=30, default=None)
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField()

    class Meta:
        db_table = "bookings"