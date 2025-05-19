from django.shortcuts import render
from user.models import register_table
from vendor.models import booking_table, package_table
from django.db.models import Sum

# Create your views here.
def admin_index(request):
    approved_package_data = package_table.objects.filter(status='approved')
    no_approved_packages = approved_package_data.count()  # Get total number of packages
    no_bookings = 0  # Initialize booking count
    total_earnings = 0  # Initialize earnings
    total_packages = package_table.objects.all().count()
    approval_pending = package_table.objects.filter(status='created').count()

    # Get all bookings related to the vendor's packages
    bookings = booking_table.objects.filter(package_id__in=approved_package_data.values_list('id', flat=True), booking_status='booked')

    no_bookings = bookings.count()  # Get total number of bookings
    total_earnings = bookings.aggregate(Sum('price'))['price__sum'] or 0
    return render(request,'admin_index.html',{'approval_pending':approval_pending,'no_bookings':no_bookings, 'earnings':total_earnings, 'total_packages':total_packages})


def admin_packages(request):
    package_data = package_table.objects.all()
    return render(request,'admin_view_packages.html',{'pdata':package_data})

def package_details(request,id):
    package_data = package_table.objects.get(id=id)
    return render(request,'package_details.html',{'pdata':package_data})

def approve_package(request, id):
    package_data = package_table.objects.get(id=id)
    package_data.status = "approved"
    package_data.save()
    return render(request,'package_details.html',{'pdata':package_data})

def reject_package(request, id):
    package_data = package_table.objects.get(id=id)
    package_data.status = "rejected"
    package_data.save()
    return render(request,'package_details.html',{'pdata':package_data})

def view_bookings(request):
    bookings = booking_table.objects.filter(booking_status='booked')
    return render(request,'bookings_view.html', {'bookings': bookings})

def view_vendors(request):
    vendors = register_table.objects.filter(user_type='vendor')
    return render(request,'view_vendors.html',{'vendors': vendors})