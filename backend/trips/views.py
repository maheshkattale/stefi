from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import TripPlan, ItineraryItem, TripInvoice
from .serializers import TripPlanSerializer, ItineraryItemSerializer, TripInvoiceSerializer
from User.jwt import userJWTAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def trip_list(request):
    """Get all trips for the authenticated user"""
    trips = TripPlan.objects.filter(user=request.user).order_by('-created_at')
    serializer = TripPlanSerializer(trips, many=True)
    return Response({
        'data': {'trips': serializer.data},
        'response': {
            'n': 1,
            'msg': 'Trips retrieved successfully',
            'status': 'success'
        }
    })

@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def create_trip(request):
    """Create a new trip"""
    serializer = TripPlanSerializer(data=request.data)
    if serializer.is_valid():
        trip = serializer.save(user=request.user)
        return Response({
            'data': {'trip_id': trip.id},
            'response': {
                'n': 1,
                'msg': 'Trip created successfully',
                'status': 'success'
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'data': {},
        'response': {
            'n': 0,
            'msg': 'Validation error',
            'status': 'error',
            'errors': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def trip_detail(request, trip_id):
    """Get trip details with itinerary"""
    try:
        trip = TripPlan.objects.get(id=trip_id, user=request.user)
    except TripPlan.DoesNotExist:
        return Response({
            'data': {},
            'response': {
                'n': 0,
                'msg': 'Trip not found',
                'status': 'error'
            }
        }, status=status.HTTP_404_NOT_FOUND)
    
    trip_serializer = TripPlanSerializer(trip)
    itinerary = ItineraryItem.objects.filter(trip=trip).order_by('date', 'time_of_day')
    itinerary_serializer = ItineraryItemSerializer(itinerary, many=True)
    
    return Response({
        'data': {
            'trip': trip_serializer.data,
            'itinerary': itinerary_serializer.data
        },
        'response': {
            'n': 1,
            'msg': 'Trip details retrieved',
            'status': 'success'
        }
    })

@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_itinerary_item(request):
    """Add an itinerary item to a trip"""
    serializer = ItineraryItemSerializer(data=request.data)
    if serializer.is_valid():
        try:
            trip = TripPlan.objects.get(id=request.data.get('trip_id'), user=request.user)
            item = serializer.save(trip=trip)
            return Response({
                'data': {'item_id': item.id},
                'response': {
                    'n': 1,
                    'msg': 'Itinerary item added successfully',
                    'status': 'success'
                }
            })
        except TripPlan.DoesNotExist:
            return Response({
                'data': {},
                'response': {
                    'n': 0,
                    'msg': 'Trip not found',
                    'status': 'error'
                }
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'data': {},
        'response': {
            'n': 0,
            'msg': 'Validation error',
            'status': 'error',
            'errors': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_itinerary_item(request, item_id):
    """Delete an itinerary item"""
    try:
        item = ItineraryItem.objects.get(id=item_id, trip__user=request.user)
        item.delete()
        return Response({
            'data': {},
            'response': {
                'n': 1,
                'msg': 'Itinerary item deleted successfully',
                'status': 'success'
            }
        })
    except ItineraryItem.DoesNotExist:
        return Response({
            'data': {},
            'response': {
                'n': 0,
                'msg': 'Item not found',
                'status': 'error'
            }
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def generate_invoice(request, trip_id):
    """Generate invoice for a trip"""
    try:
        trip = TripPlan.objects.get(id=trip_id, user=request.user)
        invoice, created = TripInvoice.objects.get_or_create(trip=trip)
        invoice.generate_invoice()
        
        serializer = TripInvoiceSerializer(invoice)
        return Response({
            'data': {'invoice': serializer.data},
            'response': {
                'n': 1,
                'msg': 'Invoice generated successfully',
                'status': 'success'
            }
        })
        
    except TripPlan.DoesNotExist:
        return Response({
            'data': {},
            'response': {
                'n': 0,
                'msg': 'Trip not found',
                'status': 'error'
            }
        }, status=status.HTTP_404_NOT_FOUND)
        