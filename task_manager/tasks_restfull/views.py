from django.core.management.sql import emit_post_migrate_signal
from rest_framework import viewsets, filters, status
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from tasks_restfull.authentication import CustomTokenAuthentication, CustomJWTAuthentication
from tasks_restfull.utils import creat_token_for_user, generate_jwt_token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes

from tasks.models import Task
from tasks_restfull.serializers import TaskSerializer


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['completed', 'user']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'completed']
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class TaskReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["completed", "user"]


class TaskCustomViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Task.objects.filter(completed=False)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        task = Task.objects.filter(pk=pk, completed=False).first()
        response = {"error": "Task does not exist"}
        status = 500
        if task:
            serializer = TaskSerializer(task)
            response = serializer.data
            status = 200
        return Response(data=response, status=status)

class TaskFilterViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Task.objects.all()
        completed = self.request.query_params.get('only_completed', None)
        moderation_approved = self.request.query_params.get('allowed_to_show', None)

        if completed:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        if moderation_approved == 'true':
            queryset = queryset.filter(moderation_status=Task.APPROVED)
        return queryset


class TaskCreateViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateViewSet(viewsets.ViewSet):
    def update(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Oops! No task matching the query"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, create = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})

@api_view(["POST"])
@permission_classes([])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(username=email, password=password)
    if user:
        token = creat_token_for_user(user)
        return Response({
            "token": token.key,
            "expires_at": token.expires_at,
            "role": "staff" if any([user.is_staff, user.is_superuser]) else "member"
        })
    return Response({"error": "Wrong credentials"}, status=401)


@api_view(["POST"])
@permission_classes([])
def login_jwt(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(username=email, password=password)
    if user:
        token = generate_jwt_token(user)
        return Response({
            "access_key": token
        })
    return Response({"error": "Wrong credentials"}, status=401)

