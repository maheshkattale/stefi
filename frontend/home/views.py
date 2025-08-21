from django.shortcuts import render, redirect, HttpResponse
import requests
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from helpers.validations import hosturl
from Masters.models import *
from User.models import *
from User.serializers import *
from trips.models import *
from trips.serializers import *
# API URLs
login_url = hosturl + "/api/User/login"
logout_url = hosturl + "/api/User/logout"

# Trip API URLs
create_trip_url = hosturl + "/api/trips/create"
get_trips_url = hosturl + "/api/trips/list"
get_trip_detail_url = hosturl + "/api/trips/detail"
add_itinerary_item_url = hosturl + "/api/trips/itinerary/add"
generate_invoice_url = hosturl + "/api/trips/invoice/generate"
delete_itinerary_item_url = hosturl + "/api/trips/itinerary/delete"

def landing_page(request):
    """Landing page with state-wise destination filtering"""
    # Get states with the most destinations
    print("jhiiii")
    states = State.objects.annotate(
        destination_count=Count('destinations')
    ).filter(is_active=True, destination_count__gt=0).order_by('-destination_count')[:12]

    # Get popular destinations
    popular_destinations = Destination.objects.filter(
        is_active=True, is_popular=True
    )[:8]
    
    # Get all unique destination types
    destination_types = Destination.objects.filter(
        is_active=True
    ).values_list('destination_type', flat=True).distinct()
    
    context = {
        'states': states,
        'popular_destinations': popular_destinations,
        'destination_types': destination_types,
    }
    print("context",context)
    
    return render(request, 'home/landing.html', context)

from django.http import JsonResponse

def search_destinations(request):
    """API endpoint for destination search"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({
            'success': False,
            'message': 'Please enter a search term',
            'results': []
        })
    
    # Search in destinations
    destinations = Destination.objects.filter(
        Q(name__icontains=query) |
        Q(state__name__icontains=query) |
        Q(description__icontains=query),
        is_active=True
    )[:10]
    
    results = []
    for dest in destinations:
        results.append({
            'id': dest.id,
            'name': dest.name,
            'state': dest.state.name,
            'type': dest.get_destination_type_display(),
            'image_url': dest.image.url if dest.image else '/static/images/default-destination.jpg',
            'url': f"/destinations/{dest.id}/"
        })
    
    return JsonResponse({
        'success': True,
        'message': f'Found {len(results)} results',
        'results': results
    })


from django.contrib.auth.decorators import login_required
from trips.models import TripPlan, TripInvoice
from datetime import datetime, timedelta


def dashboard(request):
    """Customer dashboard with travel statistics and upcoming trips"""
    user = request.session.get('user_id')
    if not user:
        messages.error(request, 'Please login first')
        return redirect('home:login')
    
    # Calculate statistics
    total_trips = TripPlan.objects.filter(user=str(user)).count()
    upcoming_trips = TripPlan.objects.filter(
        user=user,
        start_date__gte=datetime.now().date()
    ).count()
    completed_trips = TripPlan.objects.filter(
        user=user,
        end_date__lt=datetime.now().date()
    ).count()
    
    # Recent trips
    recent_trips = TripPlan.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Upcoming trips (next 30 days)
    thirty_days_later = datetime.now().date() + timedelta(days=30)
    upcoming_trips_list = TripPlan.objects.filter(
        user=user,
        start_date__range=[datetime.now().date(), thirty_days_later]
    ).order_by('start_date')[:3]
    
    # Total spending
    total_spent = TripInvoice.objects.filter(
        trip__user=user
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Favorite destinations (most visited)
    favorite_destinations = TripPlan.objects.filter(
        user=user
    ).values('destination').annotate(
        visit_count=Count('id')
    ).order_by('-visit_count')[:3]
    
    context = {
        'user': user,
        'total_trips': total_trips,
        'upcoming_trips': upcoming_trips,
        'completed_trips': completed_trips,
        'recent_trips': recent_trips,
        'upcoming_trips_list': upcoming_trips_list,
        'total_spent': total_spent,
        'favorite_destinations': favorite_destinations,
    }
    
    return render(request, 'customer/dashboard/customer-dashboard.html', context)


def trip_list(request):
    token = request.session.get('token')
    if not token:
        messages.error(request, 'Please login first')
        return redirect('home:login')
    
    headers = {'Authorization': f'Bearer {token}'}
    trips = []
    
    try:
        response = requests.get(get_trips_url, headers=headers)
        if response.status_code == 200:
            trips_data = response.json()
            if trips_data['response']['n'] == 1:
                trips = trips_data['data']['trips']
    except requests.RequestException:
        messages.error(request, 'Failed to load trips')
    
    return render(request, 'home/trips/list.html', {'trips': trips})

from datetime import datetime

# @login_required
def create_trip(request):
    """Create new trip page"""
    # Get destination from query parameter if available
    destination = request.GET.get('destination', '')
    print("destination", destination)
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Please login first')
        return redirect('home:login')


    if request.method == 'POST':
        if request.method == 'POST':
        # try:
            destination = request.POST.get('destination', '')

            # Prepare data for serializer
            post_data = request.POST.copy()
            print("post_data", post_data)
            # Create serializer instance
            serializer = TripPlanSerializer(data=post_data)
            print("destination2", destination)
            if serializer.is_valid():
                # Save the trip
                trip = TripPlan(
                    user=user_id,
                    title=serializer.validated_data['title'],
                    destination=destination,
                    persons=serializer.validated_data['persons'],
                    travel_method=serializer.validated_data['travel_method'],
                    budget=serializer.validated_data['budget'],
                    start_date=serializer.validated_data['start_date'],
                    end_date=serializer.validated_data['end_date'],
                    notes=serializer.validated_data.get('notes', '')
                )
                trip.save()
                messages.success(request, 'Trip created successfully!')
                return redirect('home:trip_detail', trip_id=trip.id)
            else:
                # Show validation errors
                for field, errors in serializer.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.title()}: {error}")
                        print(f"Validation error in {field}: {error}")
                return render(request, 'customer/trips/create.html', {'destination': destination})
        # except Exception as e:
        #     print("Error creating trip:", e)
        #     messages.error(request, f'Error creating trip: {str(e)}')
    
    # Pre-fill initial data
    initial_data = {}
    if destination:
        initial_data['title'] = f'Trip to {destination}'
        initial_data['destination'] = destination
    
    context = {
        'initial_data': json.dumps(initial_data),
        'destination': destination,
        'today': datetime.now().strftime('%Y-%m-%d')
    }


    
    return render(request, 'customer/trips/create.html',context)

def trip_detail(request, trip_id):
    token = request.session.get('token')
    if not token:
        messages.error(request, 'Please login first')
        return redirect('home:login')
    
    headers = {'Authorization': f'Bearer {token}'}
    trip = None
    itinerary = []
    
    # Fetch trip details
    try:
        response = requests.get(f"{get_trip_detail_url}/{trip_id}", headers=headers)
        if response.status_code == 200:
            trip_data = response.json()
            if trip_data['response']['n'] == 1:
                trip = trip_data['data']['trip']
                itinerary = trip_data['data']['itinerary']
            else:
                messages.error(request, trip_data['response']['msg'])
        else:
            messages.error(request, 'Failed to load trip details')
            
    except requests.RequestException:
        messages.error(request, 'Connection error. Please try again.')
        
    # Add itinerary item
    if request.method == 'POST':
        itinerary_data = {
            'trip_id': trip_id,
            'date': request.POST.get('date'),
            'time_of_day': request.POST.get('time_of_day'),
            'type': request.POST.get('type'),
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'cost_per_person': request.POST.get('cost_per_person'),
            'persons': request.POST.get('persons'),
            'duration_hours': request.POST.get('duration_hours'),
            'notes': request.POST.get('notes')
        }
        
        try:
            response = requests.post(add_itinerary_item_url, data=itinerary_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                if result['response']['n'] == 1:
                    messages.success(request, 'Activity added successfully!')
                    return redirect('home:trip_detail', trip_id=trip_id)
                else:
                    messages.error(request, result['response']['msg'])
            else:
                messages.error(request, 'Failed to add activity')
                
        except requests.RequestException:
            messages.error(request, 'Connection error. Please try again.')
    
    return render(request, 'customer/trips/detail.html', {
        'trip': trip,
        'itinerary': itinerary
    })


# from django.shortcuts import get_object_or_404

# # @login_required
# def trip_detail(request, trip_id):
#     """Trip detail page"""
#     try:
#         # Use get_object_or_404 for better error handling
#         trip = get_object_or_404(TripPlan, id=trip_id, user=user_id=request.session.get('user_id'))
#         itinerary_items = trip.itinerary.all().order_by('date', 'time_of_day')
        
#         # Calculate trip duration
#         trip.duration = (trip.end_date - trip.start_date).days + 1
        
#         context = {
#             'trip': trip,
#             'itinerary_items': itinerary_items
#         }
        
#         return render(request, 'home/trips/detail.html', context)
        
#     except Exception as e:
#         messages.error(request, f'Error loading trip: {str(e)}')
#         return redirect('home:trip_list')
    


def delete_itinerary_item(request, item_id):
    token = request.session.get('token')
    if not token:
        messages.error(request, 'Please login first')
        return redirect('home:login')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.post(f"{delete_itinerary_item_url}/{item_id}", headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['response']['n'] == 1:
                messages.success(request, 'Activity deleted successfully!')
            else:
                messages.error(request, result['response']['msg'])
        else:
            messages.error(request, 'Failed to delete activity')
            
    except requests.RequestException:
        messages.error(request, 'Connection error. Please try again.')
    
    # Redirect back to the trip detail page
    trip_id = request.GET.get('trip_id')
    if trip_id:
        return redirect('home:trip_detail', trip_id=trip_id)
    return redirect('home:trip_list')

def generate_invoice(request, trip_id):
    token = request.session.get('token')
    if not token:
        messages.error(request, 'Please login first')
        return redirect('home:login')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.post(f"{generate_invoice_url}/{trip_id}", headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['response']['n'] == 1:
                messages.success(request, 'Invoice generated successfully!')
                return redirect('home:view_invoice', trip_id=trip_id)
            else:
                messages.error(request, result['response']['msg'])
        else:
            messages.error(request, 'Failed to generate invoice')
            
    except requests.RequestException:
        messages.error(request, 'Connection error. Please try again.')
    
    return redirect('home:trip_detail', trip_id=trip_id)

def view_invoice(request, trip_id):
    token = request.session.get('token')
    if not token:
        messages.error(request, 'Please login first')
        return redirect('home:login')
    
    # In a real implementation, you would fetch invoice data from API
    # For now, we'll just render the template with trip_id
    return render(request, 'home/trips/invoice.html', {'trip_id': trip_id})


















# --------------------------------------------------------------------------------------


from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from helpers.validations import hosturl

# API URLs
login_url = hosturl + "/api/User/login"
logout_url = hosturl + "/api/User/logout"
api_states_url = hosturl + "/api/home/states"
api_popular_destinations_url = hosturl + "/api/home/popular-destinations"
api_destination_types_url = hosturl + "/api/home/destination-types"



def login(request):
    """Login page - template rendering only"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        data = {
            'email': email,
            'password': password,
            'source': 'Web'
        }

        try:
            login_request = requests.post(login_url, data=data)
            login_response = login_request.json()
            
            if login_response['response']['n'] == 1:
                token = login_response['data']['token']
                request.session['token'] = token 
                request.session['role_id'] = login_response['data']['role'] 
                request.session['role_name'] = login_response['data']['role_name']  
                request.session['user_name'] = login_response['data']['username']
                request.session['user_id'] = login_response['data']['user_id']
                
                messages.success(request, 'Login successful!')
                return redirect('home:dashboard')
            else:
                messages.error(request, login_response['response']['msg'])
                
        except requests.RequestException:
            messages.error(request, 'Connection error. Please try again.')
        
        return render(request, 'customer/authentication/login.html')
    
    return render(request, 'customer/authentication/login.html')

def logout(request):
    """Logout handling"""
    token = request.session.get('token')
    if token:
        try:
            headers = {'Authorization': f'Bearer {token}'}
            requests.post(logout_url, headers=headers)
        except requests.RequestException:
            pass
    
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('home:landing_page')



# Other view functions remain the same for template rendering...
# trip_list, create_trip, trip_detail, etc.





from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password
from User.models import User, Role

def customer_registration(request):
    """Customer registration page"""
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            mobile_number = request.POST.get('mobile_number')
            print("request.POST", request.POST)
            # Basic validation
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'home/customer_registration.html')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return render(request, 'home/customer_registration.html')
            
            # Get or create customer role (assuming role ID 3 is for customers)

            # Create user
            data={
                'Username': username,
                'email': email,
                'password': password,
                'textPassword': password,  # Store plain text password if needed
                'mobileNumber': mobile_number,
                'role': 2,  
                'status': True,
                'isActive': True
            }
            user_serializer = UserSerializer(data=data)

            if not user_serializer.is_valid():
                first_key, first_value = next(iter(user_serializer.errors.items()))
                messages.error(request, f"Invalid data: {first_key} - {first_value[0]}")

                return render(request, 'home/customer_registration.html')
            # Save user
            user_serializer.save()
            
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('home:login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'customer/authentication/customer_registration.html')



def admin_login(request):
    """Admin panel login page"""
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        data = {}
        data['email'] = email
        data['password'] = password
        data['source'] = 'Mobile'

        login_request = requests.post(login_url, data=data)
        login_response = login_request.json()
        print("login_response",login_response)
        if login_response['response']['n'] == 1:
            token = login_response['data']['token']
            request.session['token'] = token 
            request.session['role_id'] = login_response['data']['role'] 
            request.session['role_name'] = login_response['data']['role_name']  
            request.session['user_name'] = login_response['data']['username']   


            messages.success(request, 'Admin login successful!')
            return redirect('home:')
        else:
            messages.error(request, login_response['response']['msg'])
            return render(request, 'admin/authentication/login.html')
        


      
    else:
        print("hiii")
        return render(request, 'admin/authentication/login.html')

# @user_passes_test(lambda u: u.is_staff)
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta
from trips.models import TripPlan, TripInvoice
from User.models import User

def admin_dashboard(request):
    """Admin dashboard with statistics and analytics"""
    # Calculate statistics
    total_trips = TripPlan.objects.count()
    total_users = User.objects.count()
    total_revenue = TripInvoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Recent trips (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_trips = TripPlan.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Popular destinations
    popular_destinations = TripPlan.objects.values('destination').annotate(
        trip_count=Count('id')
    ).order_by('-trip_count')[:5]
    
    # Revenue by month (last 6 months)
    revenue_data = []
    for i in range(6):
        month = datetime.now() - timedelta(days=30*i)
        month_revenue = TripInvoice.objects.filter(
            issue_date__month=month.month,
            issue_date__year=month.year
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        revenue_data.append({
            'month': month.strftime('%b %Y'),
            'revenue': float(month_revenue)
        })
    revenue_data.reverse()
    
    # Recent activities
    recent_activities = TripPlan.objects.select_related('user').order_by('-created_at')[:10]
    
    # User growth (last 30 days)
    new_users = User.objects.filter(createdAt__gte=thirty_days_ago).count()
    
    context = {
        'total_trips': total_trips,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_trips': recent_trips,
        'popular_destinations': popular_destinations,
        'revenue_data': revenue_data,
        'recent_activities': recent_activities,
        'new_users': new_users,
    }
    
    return render(request, 'admin/dashboard/admin_dashboard.html', context)










