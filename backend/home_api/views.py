from rest_framework.decorators import api_view
from rest_framework.response import Response
from Masters.models import State, Destination
from django.db.models import Count, Q

@api_view(['GET'])
def api_search_destinations(request):
    """API endpoint for destination search"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({
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
    ).select_related('state')[:10]
    
    results = []
    for dest in destinations:
        results.append({
            'id': dest.id,
            'name': dest.name,
            'state': dest.state.name,
            'type': dest.get_destination_type_display(),
            'image_url': dest.image.url if dest.image else '/static/assets/images/default-destination.jpg',
            'url': f"/destinations/{dest.id}/"
        })
    
    return Response({
        'success': True,
        'message': f'Found {len(results)} results',
        'results': results
    })

@api_view(['GET'])
def api_get_states(request):
    """API endpoint to get states with destinations"""
    states = State.objects.annotate(
        destination_count=Count('destinations')
    ).filter(is_active=True, destination_count__gt=0).order_by('-destination_count')[:12]
    
    state_data = []
    for state in states:
        state_data.append({
            'id': state.id,
            'name': state.name,
            'code': state.code,
            'destination_count': state.destination_count,
            'image_url': state.image.url if state.image else '/static/images/default-state.jpg',
            'description': state.description,
            'url': f"/states/{state.id}/"
        })
    
    return Response({
        'success': True,
        'states': state_data
    })

@api_view(['GET'])
def api_get_popular_destinations(request):
    """API endpoint to get popular destinations"""
    destinations = Destination.objects.filter(
        is_active=True, is_popular=True
    ).select_related('state')[:8]
    
    destination_data = []
    for dest in destinations:
        destination_data.append({
            'id': dest.id,
            'name': dest.name,
            'state': dest.state.name,
            'type': dest.get_destination_type_display(),
            'image_url': dest.image.url if dest.image else '/static/assets/images/default-destination.jpg',
            'description': dest.description,
            'url': f"/destinations/{dest.id}/"
        })
    
    return Response({
        'success': True,
        'destinations': destination_data
    })

@api_view(['GET'])
def api_get_destination_types(request):
    """API endpoint to get destination types"""
    destination_types = Destination.objects.filter(
        is_active=True
    ).values_list('destination_type', flat=True).distinct()
    
    type_choices = dict(Destination.DESTINATION_TYPES)
    type_data = [{'value': dt, 'label': type_choices.get(dt, dt)} for dt in destination_types]
    
    return Response({
        'success': True,
        'types': type_data
    })