from rest_framework import generics, permissions, pagination
from .serializers import TeacherSerializer
from .models import Teacher
from rest_framework.response import Response
from rest_framework.views import APIView

# Custom pagination class
class TeacherPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Teacher List and Create View
class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Auth required for POST
    pagination_class = TeacherPagination
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Auto-assign the current user

# Teacher Detail, Update, Delete View
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required for all operations

# Additional custom view example
class TeacherStats(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        stats = {
            'total': Teacher.objects.count(),
            'active': Teacher.objects.filter(is_approved=True).count(),
            'avg_rate': Teacher.objects.aggregate(models.Avg('hourly_rate'))['hourly_rate__avg']
        }
        return Response(stats)