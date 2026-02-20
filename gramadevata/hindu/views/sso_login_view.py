


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from ..models import Register

class SSOLoginVerify(APIView):

    def get(self, request):
        token = request.GET.get('token')

        if not token:
            return Response({"error": "Token missing"}, status=400)

        try:
            # 🔐 Decode token (same secret)
            access = AccessToken(token)

            user_id = access.get('user_id')
            username = access.get('username')
            email = access.get('email')
            contact = access.get('contact_number')

            if not user_id:
                return Response({"error": "Invalid token"}, status=401)

            # 🔎 Check user exists or not
            user = Register.objects.filter(id=user_id).first()

            if not user:
                # 🆕 Auto create user
                user = Register.objects.create(
                    id=user_id,
                    username=username,
                    email=email,
                    contact_number=contact,
                    status='ACTIVE'
                )

            # 🔁 Generate LOCAL JWT
            refresh = RefreshToken.for_user(user)
            local_access = refresh.access_token

            return Response({
                "refresh": str(refresh),
                "access": str(local_access),
                "message": "SSO Login Success"
            })

        except Exception as e:
            return Response({"error": "Invalid or expired token"}, status=401)
