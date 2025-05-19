import hashlib
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from user.models import register_table
from vendor.models import booking_table, package_table
from datetime import datetime
from django.utils import timezone
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def display_index(request):
    return render(request,'index.html')

def display_user_registration(request):
    return render(request,'register.html')

def display_packages(request):
    package_data = package_table.objects.filter(start_date__gt= timezone.now(),status='approved')
    return render(request,'packages.html', {'pdata': package_data})

def booking_form(request):
    if request.session.has_key('userid'):
        package_data = package_table.objects.filter(start_date__gt= timezone.now(),status='approved')
        return render(request,'booking.html', {'pdata': package_data})
    return redirect("/login")


def user_registration(request):
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

        data=register_table.objects.all()    #get data from register_table from data base , data=object

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
            return render(request,'register.html',{"e_error":email_error, "p_error":password_error, "cp_error":confirm_password_error})
        else:
        #object for register_table
            user_data=register_table()
            user_data.firstname=first_name
            user_data.lastname=last_name
            user_data.email=email
            user_data.password=hashlib.sha1(password.encode('utf-8')).hexdigest()  #encrypt password
            user_data.user_type='user'
            user_data.created_at=datetime.now()
            user_data.updated_at=datetime.now()
            user_data.save()
            return render(request,'index.html')

def display_login(request):
    return render(request,'login.html')

def login(request):
    if request.method=='POST':
        email1 = request.POST.get("email")
        password1 = hashlib.sha1(request.POST.get("password").encode('utf-8')).hexdigest()
        try:
            user=register_table.objects.get(email=email1,password=password1)
            request.session['userid']=user.id
            request.session['name']=f'{user.firstname} {user.lastname}'
            if user.user_type=='user':
                return render(request, 'index.html')
            elif user.user_type=='vendor':
                return redirect('/vendor_index/')
            elif user.user_type=='admin':
                return render(request,'admin_index.html')
        except:
            return render(request,'login.html',{"login_error":"Invalid Email or Password"})
        
def payment_page(request):
    return render(request,'payment.html')


def booking(request):

    if request.session.has_key('userid'):
        if request.method == 'POST':
            #get data from form
            name=request.POST.get("name")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
            package_id=request.POST.get("package")
            no_of_persons = request.POST.get("no_of_persons")

            package_data = package_table.objects.get(id=package_id)
            user_id = register_table.objects.get(id=request.session['userid'])

            price = float(no_of_persons) * float(package_data.price)

            booking = booking_table()
            booking.name = name
            booking.email = email
            booking.phone = phone
            booking.no_of_persons = no_of_persons
            booking.package_id = package_data
            booking.price = price
            booking.payment_status = 'pending'
            booking.created_at=datetime.now()
            booking.updated_at=datetime.now()
            booking.user_id = user_id
            booking.booking_status = 'pending'
            booking.save()
            request.session['booking_id'] = booking.id
            print("BOOKING ID: ", request.session['booking_id'])

            return render(request,'payment.html',{'booking': booking, 'razorpay_key': settings.RAZORPAY_KEY_ID})
    return redirect("/login")

def transaction(request, id):
    if request.method == 'POST':
        booking = booking_table.objects.get(id=id)
        booking.payment_status = 'success'
        booking.booking_status = 'booked'
        booking.updated_at = datetime.now()
        booking.save()
        return HttpResponse("<h2>Booking Successfull</h2>")


def logout_view(request):
    logout(request)  # Logs out the user
    request.session.flush()  # Clears the session data
    return redirect('/')

def package_readmore(request,id):
    package_data = package_table.objects.get(id=id)
    return render(request,'package_detail_view.html',{'pdata':package_data})

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_order(request, booking_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data['amount']  # already in paise

        order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })

        return JsonResponse({'order_id': order['id']})



def payment_success(request):
    payment_id = request.GET.get('payment_id')
    booking = booking_table.objects.get(id=request.session["booking_id"])
    booking.transaction_id = payment_id
    booking.payment_status = 'success'
    booking.booking_status = 'booked'
    booking.updated_at = datetime.now()
    booking.save()
    return render(request,"success.html",{'data': booking})



