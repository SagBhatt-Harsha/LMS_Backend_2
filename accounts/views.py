from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token # Used for login tokens.
from django.contrib.auth import authenticate # Verifies email + password.
 
from .models import User
from .serializers import UserSerializer, UserCreateUpdateSerializer
from .permissions import IsAdminUserRole

# Create your views here.

class LoginView(APIView):
    # POST /api/auth/login/
    permission_classes = []
    # Override default permissions and allow ANYONE to access this endpoint.Ensures login api endpoint has public access.

    def post(self, request):

        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')

        user = authenticate(
            request,
            username=email,
            password=password
        )
        
        # If standard auth fails, try case-insensitive email check
        if not user and email:
            try:
                user_obj = User.objects.get(email__iexact=email)
                if user_obj.check_password(password):
                    user = user_obj
            except User.DoesNotExist:
                pass

        # Even though frontend sends email, Django expects username param internally. username=email maps Username to email for Django.

        if not user:
            # Fallback for users created via admin panel or scripts where password might have been saved as plaintext
            try:
                potential_user = User.objects.get(email=email)
                if potential_user.password == password:
                    potential_user.set_password(password)
                    potential_user.save()
                    user = potential_user
            except User.DoesNotExist:
                pass

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "phone": getattr(user, 'phone', '') or ''
            }
        })


class LogoutView(APIView):
    # POST /api/auth/logout/
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response({"message": "Logged out successfully"})


class MeView(APIView):
    # POST /api/auth/me/
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "phone": getattr(user, 'phone', '') or ''
        })


class UserListCreateView(generics.ListCreateAPIView):
    # For POST and GET
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_serializer_class(self):
        # POST /api/users/
        if self.request.method == 'POST':
            return UserCreateUpdateSerializer

        return UserSerializer

    def get_queryset(self):
        # GET /api/users/?role=
        role = self.request.query_params.get('role')

        if role:
            return User.objects.filter(role=role)

        return User.objects.all()


class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # PUT /api/users/{id}/
    # DELETE /api/users/{id}/
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsAdminUserRole]

    serializer_class = UserCreateUpdateSerializer