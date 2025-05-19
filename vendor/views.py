import hashlib

from django.shortcuts import render
from django.db.models import Sum
from user.models import register_table
from vendor.models import booking_table, package_table
from datetime import datetime


# Create your views here.

def register(request):
    return render(request,'register_page.html')

def vendor_index(request):
    package_data = package_table.objects.filter(vendor_id = request.session['userid'])
    no_packages = package_data.count()  # Get total number of packages
    no_bookings = 0  # Initialize booking count
    total_earnings = 0  # Initialize earnings

    # Get all bookings related to the vendor's packages
    bookings = booking_table.objects.filter(package_id__in=package_data.values_list('id', flat=True), booking_status='booked')

    no_bookings = bookings.count()  # Get total number of bookings
    total_earnings = bookings.aggregate(Sum('price'))['price__sum'] or 0
    return render(request,'vendor_index.html',{'no_packages':no_packages,'no_bookings':no_bookings, 'earnings':total_earnings})

def package_form(request):
    return render(request,'create_package.html')

def package_view(request):
    package_data = package_table.objects.filter(vendor_id=request.session['userid'])
    return render(request,'view_packages.html',{'pdata':package_data})

def package_edit(request,id):
    package_data = package_table.objects.get(id=id)
    return render(request,'edit_package.html',{'pdata':package_data})




def vendor_registration(request):
    if request.method=="POST":

        #get data from form
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email_address")
        password=request.POST.get("password")
        confirm_password=request.POST.get("repeat_password")

    #variables to pass errors
        email_error=""
        password_error=""
        confirm_password_error=""

        flag=0 # variable to check if the form is valid or  not

        data=register_table.objects.all()    #get data from register_table from data base

        #validation
        #checking email already exists or  not
        for i in data:
            if email==i.email:
                email_error="Email already exists"
                flag=1

        if len(password)<8:
            password_error="Password should contain atleast 8 characters"
            flag=1

        if password!=confirm_password:
            confirm_password_error="Password and Confirm password should be same"
            flag=1

        if flag==1:
            return render(request,'register_page.html',{"e_error":email_error, "p_error":password_error, "cp_error":confirm_password_error})
        else:
        #object for register_table
            vendor_data=register_table()
            vendor_data.firstname=first_name
            vendor_data.lastname=last_name
            vendor_data.email=email
            vendor_data.password=hashlib.sha1(password.encode('utf-8')).hexdigest()  #encrypt password
            vendor_data.user_type='vendor'
            vendor_data.created_at=datetime.now()
            vendor_data.updated_at=datetime.now()
            vendor_data.save()
            return render(request,'index.html')

def package_creation(request):
    if request.method=="POST":

        #get data from form
        p_name=request.POST.get("package_name")
        dstnation=request.POST.get("destination")
        duration=request.POST.get("duration")
        price=request.POST.get("price")
        description=request.POST.get("description")
        image= request.FILES.get("image")
        startdate= request.POST.get("start_date")
        enddate= request.POST.get("end_date")


    #variables to pass errors
        startdate_error=""
        enddate_error=""


        flag=0 # variable to check if the form is valid or  not



        #validation
        #checking email already exists or  not

        date_format = "%Y-%m-%d"  # The format of the date string
        sdate_str_obj = datetime.strptime(startdate, date_format)
        edate_str_obj = datetime.strptime(enddate, date_format)
        if sdate_str_obj<=datetime.now():
            startdate_error="start date should be a future date"
            flag=1

        if edate_str_obj<sdate_str_obj:
            enddate_error="end date should be after start date"
            flag=1

        if flag==1:
            return render(request,'create_package.html',{"starterror":startdate_error, "enderror":enddate_error})
        else:
        #object for register_table
            package_data=package_table()
            package_data.package_name=p_name
            package_data.destination=dstnation
            package_data.duration=duration
            package_data.price=price
            package_data.created_at=datetime.now()
            package_data.updated_at=datetime.now()
            package_data.description=description
            package_data.images=image
            package_data.start_date=startdate
            package_data.end_date=enddate
            package_data.status='created'
            vendor_data=register_table.objects.get(id=request.session['userid'])
            package_data.vendor_id=vendor_data
            package_data.save()
            return render(request,'create_package.html',{'success':'Package created successfully'})



def package_updation(request,id):
    if request.method=="POST":

        #get data from form
        p_name=request.POST.get("package_name")
        dstnation=request.POST.get("destination")
        duration=request.POST.get("duration")
        price=request.POST.get("price")
        description=request.POST.get("description")
        image= request.FILES.get("image")
        startdate= request.POST.get("start_date")
        enddate= request.POST.get("end_date")


    #variables to pass errors
        startdate_error=""
        enddate_error=""


        flag=0 # variable to check if the form is valid or  not



        #validation
        #checking email already exists or  not

        date_format = "%Y-%m-%d"  # The format of the date string
        sdate_str_obj = datetime.strptime(startdate, date_format)
        edate_str_obj = datetime.strptime(enddate, date_format)
        if sdate_str_obj<=datetime.now():
            startdate_error="start date should be a future date"
            flag=1

        if edate_str_obj<sdate_str_obj:
            enddate_error="end date should be after start date"
            flag=1

        if flag==1:
            return render(request,'create_package.html',{"starterror":startdate_error, "enderror":enddate_error})
        else:
        #object for register_table
            package_data=package_table.objects.get(id=id)
            package_data.package_name=p_name
            package_data.destination=dstnation
            package_data.duration=duration
            package_data.price=price
            package_data.created_at=datetime.now()
            package_data.updated_at=datetime.now()
            package_data.description=description
            if image:
                package_data.images=image
            package_data.start_date=startdate
            package_data.end_date=enddate
            package_data.status='created'
            vendor_data=register_table.objects.get(id=request.session['userid'])
            package_data.vendor_id=vendor_data
            package_data.updated_at = datetime.now()
            package_data.save()
            return render(request,'create_package.html',{'success':'Package updated successfully'})



def bookings(request):
    bookings = booking_table.objects.filter(booking_status='booked')
    return render(request,'bookings.html', {'bookings': bookings})