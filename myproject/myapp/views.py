from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PhoneNumber ,CommunityMember,Token  
from .serializers import PhoneNumberSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions
from .serializers import CommunityMemberSerializer
from .authentication import PhoneNumberJWTAuthentication


class RegisterPhoneNumberAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.save()
            # Return the message, number, and ID in the response
            return Response(
                {
                    "message": "The OTP is sent to your number",
                    "number": phone_number.number,
                    "number_id": phone_number.id  # Include ID in response
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # views.py


# # views.py
# class VerifyOTPAPI(APIView):
#     def post(self, request, *args, **kwargs):
#         number = request.data.get("number")
#         otp = request.data.get("otp")

#         try:
#             phone_instance = PhoneNumber.objects.get(number=number)
#         except PhoneNumber.DoesNotExist:
#             return Response(
#                 {"message": "Phone number not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         # If the number is already verified
#         if phone_instance.is_verified:
#             # Retrieve existing JWT or create a new one
#             refresh = RefreshToken.for_user(phone_instance)
#             jwt_token = str(refresh.access_token)

#             # Retrieve the community member details if they exist
#             try:
#                 community_member = CommunityMember.objects.get(phone_number=phone_instance)
#                 return Response(
#                     {
#                         "message": "The number is already verified",
#                         "jwt": jwt_token,
#                         "phone_number": phone_instance.number,
#                         "name": community_member.name,
#                         "community": dict(CommunityMember.COMMUNITY_CHOICES).get(community_member.community),
#                         "profile_image": community_member.profile_image
#                     },
#                     status=status.HTTP_200_OK
#                 )
#             except CommunityMember.DoesNotExist:
#                 return Response(
#                     {
#                         "message": "The number is already verified",
#                         "jwt": jwt_token,
#                         "phone_number": phone_instance.number,
#                         "name": "",
#                         "community": "",
#                         "profile_image": ""
#                     },
#                     status=status.HTTP_200_OK
#                 )

#         # If the OTP is correct and the user is not yet verified
#         if otp == "0000":
#             # Verify the phone number
#             phone_instance.is_verified = True
#             phone_instance.save()

#             # Generate JWT token
#             refresh = RefreshToken.for_user(phone_instance)
#             jwt_token = str(refresh.access_token)

#             return Response(
#                 {
#                     "message": "The user is verified now",
#                     "jwt": jwt_token,
#                     "phone_number": phone_instance.number,
#                     "name": "",
#                     "community": "",
#                     "profile_image": ""
#                 },
#                 status=status.HTTP_200_OK
#             )
#         else:
#             # If OTP does not match, ensure is_verified remains False
#             phone_instance.is_verified = False
#             phone_instance.save()

#             return Response(
#                 {"message": "Invalid OTP"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# # views.py



# class JoinCommunityAPI(APIView):
#     authentication_classes = [PhoneNumberJWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = CommunityMemberSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Retrieve the authenticated phone number
#             phone_number = request.user  # Already a PhoneNumber instance
            
#             community_member = CommunityMember.objects.create(
#                 name=serializer.validated_data['name'],
#                 phone_number=phone_number,
#                 community=serializer.validated_data['community'],
#                 profile_image=serializer.validated_data['profile_image']
#             )
            
#             token = request.auth

#             return Response(
#                 {
#                     "message": "Successfully joined community",
#                     "jwt": str(token),
#                     "phone_number": phone_number.number,
#                     "name": community_member.name,
#                     "community": dict(CommunityMember.COMMUNITY_CHOICES).get(community_member.community),
#                     "profile_image": community_member.profile_image
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class VerifyOTPAPI(APIView):
    def post(self, request, *args, **kwargs):
        number = request.data.get("number")
        otp = request.data.get("otp")

        try:
            phone_instance = PhoneNumber.objects.get(number=number)
        except PhoneNumber.DoesNotExist:
            return Response(
                {"message": "Phone number not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if phone_instance.is_verified:
            refresh = RefreshToken.for_user(phone_instance)
            jwt_token = str(refresh.access_token)

            # Save or update token in the Token model
            Token.objects.update_or_create(
                phone_number=phone_instance,
                defaults={"jwt_token": jwt_token}
            )

            try:
                community_member = CommunityMember.objects.get(phone_number=phone_instance)
                return Response(
                    {
                        "message": "The number is already verified",
                        "jwt": jwt_token,
                        "phone_number": phone_instance.number,
                        "name": community_member.name,
                        "community": dict(CommunityMember.COMMUNITY_CHOICES).get(community_member.community),
                        "profile_image": community_member.profile_image
                    },
                    status=status.HTTP_200_OK
                )
            except CommunityMember.DoesNotExist:
                return Response(
                    {
                        "message": "The number is already verified",
                        "jwt": jwt_token,
                        "phone_number": phone_instance.number,
                        "name": "",
                        "community": "",
                        "profile_image": ""
                    },
                    status=status.HTTP_200_OK
                )

        if otp == "0000":
            phone_instance.is_verified = True
            phone_instance.save()
            refresh = RefreshToken.for_user(phone_instance)
            jwt_token = str(refresh.access_token)

            # Save or update token in the Token model
            Token.objects.update_or_create(
                phone_number=phone_instance,
                defaults={"jwt_token": jwt_token}
            )

            return Response(
                {
                    "message": "The user is verified now",
                    "jwt": jwt_token,
                    "phone_number": phone_instance.number,
                    "name": "",
                    "community": "",
                    "profile_image": ""
                },
                status=status.HTTP_200_OK
            )
        else:
            phone_instance.is_verified = False
            phone_instance.save()

            return Response(
                {"message": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
            
class JoinCommunityAPI(APIView):
    authentication_classes = [PhoneNumberJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CommunityMemberSerializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = request.user
            
            community_member = CommunityMember.objects.create(
                name=serializer.validated_data['name'],
                phone_number=phone_number,
                community=serializer.validated_data['community'],
                profile_image=serializer.validated_data['profile_image']
            )

            # Retrieve the JWT token from the Token model
            token_instance = Token.objects.get(phone_number=phone_number)
            jwt_token = token_instance.jwt_token

            return Response(
                {
                    "message": "Successfully joined community",
                    "jwt": jwt_token,
                    "phone_number": phone_number.number,
                    "name": community_member.name,
                    "community": dict(CommunityMember.COMMUNITY_CHOICES).get(community_member.community),
                    "profile_image": community_member.profile_image
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
