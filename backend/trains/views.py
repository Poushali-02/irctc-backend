
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Train
from .serializers import TrainDetailSerializer

# view for creating train

@extend_schema(tags=['Trains'])
class TrainCreateView(generics.CreateAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainDetailSerializer
    
    # anyone can create an account
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        train = serializer.save()
        
        return Response(
            {
                "train": {
                    "id": train.id,
                    "train_number": train.train_number,
                    "name": train.name,
                    "source": train.source,
                    "destination": train.destination,
                    "departure_time": train.departure_time,
                    "arrival_time": train.arrival_time,
                    "total_seats": train.total_seats,
                    "available_seats": train.available_seats
                }
            },
            status=status.HTTP_201_CREATED
        )
        
# view for search
@extend_schema(
    tags=['Trains'],
    parameters=[
        OpenApiParameter(
            name='source',
            description='Filter by source station',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='destination',
            description='Filter by destination station',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='date',
            description='Filter by date (YYYY-MM-DD format)',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='limit',
            description='Number of results to return',
            required=False,
            type=int
        ),
        OpenApiParameter(
            name='offset',
            description='Starting offset for pagination',
            required=False,
            type=int
        ),
    ]
)
class TrainSearchView(generics.ListAPIView):
    serializer_class = TrainDetailSerializer
    
    # only authenticated users can search
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Train.objects.all()
           
        source = self.request.query_params.get('source')
        destination = self.request.query_params.get('destination')
        date = self.request.query_params.get('date')
        
        if source: # filtering by source
            queryset = queryset.filter(source__icontains=source)
            
        if destination: # filtering by destination
            queryset = queryset.filter(destination__icontains=destination)
            
        if date: # filtering by date
            from datetime import datetime
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(departure_time__date=search_date)
            
        return queryset
    
    # listing trains
    def list(self, request, *args, **kwargs):
        import time
        from datetime import datetime
        from common.mongo import DATABASE
        
        start_time = time.time()
        response = super().list(request, *args, **kwargs)
        execution_time = time.time() - start_time
        
        if isinstance(response.data, dict):
            # Paginated response: {'count': 10, 'results': [...]}
            results_count = len(response.data.get('results', []))
        else:
            # Non-paginated response: [...]
            results_count = len(response.data) if response.data else 0
        
        BACKEND_URL="https://localhost:8000"
        log_entry = {
            'endpoint': BACKEND_URL + request.path,
            'method': request.method,
            'timestamp': time.time(),
            'timestamp_iso': datetime.now().isoformat(),
            
            'user_id': request.user.id,
            'user_email': request.user.email,
            'is_staff': request.user.is_staff,
            
            'query_params': dict(request.query_params),
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            
            'status_code': response.status_code,
            'results_count': results_count,
            'execution_time': execution_time,
            
            'search_filters': {
                'source': request.query_params.get('source'),
                'destination': request.query_params.get('destination'),
                'date': request.query_params.get('date')
            }
        }
        try:
            DATABASE.api_logs.insert_one(log_entry)
        except Exception as e:
            print(f"Mongodb logging failed: {str(e)}")
        return response