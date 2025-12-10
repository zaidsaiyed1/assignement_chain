from django.shortcuts import render
from django.contrib.auth import authenticate
# Create your views here.
from rest_framework import viewsets
from .serializers import *
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
user = get_user_model()

class CustomUserApi(APIView):
      def get_permissions(self):
        if self.request.method in ['POST']:
            return [AllowAny()]  # Allow anyone to register
        elif self.request.method in ['GET', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]  # Require login for sensitive actions
        else:
            return [IsAuthenticated()] 
      
      def get(self,request):
             if not request.user.is_authenticated:
              return Response({"error": "Invalid Credentials"}, status=401)

             user_id = request.query_params.get("id")
             if user_id:
                 queryset = CustomUser.objects.filter(id=user_id)
                 serializer = CustomUserSerializer(queryset, many=True)
                 return Response({"data": serializer.data})
             else:
               queryset = CustomUser.objects.all()
               serializer = CustomUserSerializer(queryset, many=True)
               return Response({"data": serializer.data})



      def post(self,request):
            dataNoti = request.data
            serializer = CustomUserSerializer(data=dataNoti)
            if not serializer.is_valid():
                  return Response({
                        "message":"Data is invalid",
                        "errors":serializer.errors,
                  })
            serializer.save()

            return Response({
                  "message":"Data Saved",
                  "data":serializer.data,
            })

      def put(self,request):
            return Response({
                  "message":"this is a put method for api"
            })
      def patch(self,request):
            data = request.data
            if not data.get('id'):
                  return Response({
                        "message":"Data not updated",
                        "errors":"id is invalid",
                  })
            notification = CustomUser.objects.get(id=data.get('id'))
            serializer=CustomUserSerializer(notification,data=data,partial=True)
            if not serializer.is_valid():
                  return Response({
                        "message":"Data is invalid",
                        "errors":serializer.errors,
                  })
            serializer.save()
     
            return Response({
                  "message":"Data Saved",
                  "data":serializer.data,
            })
      def delete(self,request):
             data = request.data
             if not data.get('id'):
                   return Response({
                         "message":"Data not updated",
                         "errors":"id is invalid",
                   })
             user = CustomUser.objects.get(id=data.get('id')).delete()
             
             return Response({
                   "message":"Data Delete",
                   "data":{},
             })
      
 


class UserLoginView(APIView):
      def get_permissions(self):
        if self.request.method in ['POST']:
            return [AllowAny()]  # Allow anyone to register
        elif self.request.method in ['GET', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]  # Require login for sensitive actions
        else:
            return [IsAuthenticated()] 
      



      def get(self,request):
             if not request.user.is_authenticated:
                   return Response("Invalid Credentials")
             
             user = request.user
            #  queryset = CustomUser.objects.all()
             serializer=CustomUserSerializer(user.email,many=True)
             return Response({
                 "data":serializer.data
               }) 
      def post(self,request):
            print("login")
            data = request.data
            print(data)
            user_data = CustomUser.objects.get(email=data.get('email'))
            print(user_data.email)
            if user_data is not None:
                  credentials = {
                        'lemail':user_data.email,
                        'lpassword':data.get('password')
                  }
                  user = authenticate(email=credentials["lemail"],password=credentials["lpassword"])

                  print(user)
                  if user and user.is_active:
                        user_serializer = CustomUserSerializer(user)
                        return Response(user_serializer.data,status=200)

            return Response("Invalid Credentials",status=403)
      



class EventApi(APIView):
      def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]  
        elif self.request.method in ['GET', 'PUT', 'DELETE']:
            return [IsAuthenticated()]  
        else:
            return [IsAuthenticated()] 
      
      def get(self,request):
             if not request.user.is_authenticated:
              return Response({"error": "Invalid Credentials"}, status=401)

             eid = request.query_params.get("id")
             if eid:
                 queryset = Event.objects.filter(id=eid)
                 serializer = EventSerializer(queryset, many=True)
                 return Response({"data": serializer.data})
             else:
               queryset = Event.objects.all()
               serializer = EventSerializer(queryset, many=True)
               return Response({"data": serializer.data})



      def post(self,request):
            if not request.user.is_authenticated:
                     return Response({"error": "Invalid Credentials"}, status=401)

            dataN = request.data
            serializer = EventSerializer(data=dataN)
            if not serializer.is_valid():
                  return Response({
                        "message":"Data is invalid",
                        "errors":serializer.errors,
                  })
            serializer.save()

            return Response({
                  "message":"Data Saved",
                  "data":serializer.data,
            })

      def put(self, request):
        try:
            eid = request.query_params.get("id")
            event = Event.objects.get(id=eid)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        if event.organizer != request.user:
            return Response({"error": "You are not the organizer of this event"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event updated successfully", "data": serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
      def delete(self,request):
             data = request.data
             if not data.get('id'):
                   return Response({
                         "message":"Data not updated",
                         "errors":"id is invalid",
                   })
             if request.user != Event.objects.get(id=data.get('id')).organizer:
                   return Response({
                         "message":"You are not authorized to delete this event",
                         "errors":"authorization error",
                   }, status=status.HTTP_403_FORBIDDEN)
             else:
                   u = Event.objects.get(id=data.get('id')).delete()
             
             return Response({
                   "message":"Data Delete",
                   "data":{},
             })
      
 
