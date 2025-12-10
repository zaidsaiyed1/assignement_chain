from django.shortcuts import render
from django.contrib.auth import authenticate
# Create your views here.
from rest_framework import viewsets, generics,filters
from .serializers import *
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import status
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
            serializer=CustomUserSerializer(data=data,partial=True)
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
      
      def get(self,request,eid=None):
             if not request.user.is_authenticated:
              return Response({"error": "Invalid Credentials"}, status=401)
             if eid:
                 try:
                     queryset = Event.objects.filter(id=eid)
                 except Event.DoesNotExist:
                     return Response({"error": "Event not found"}, status=404)
                 
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

      def put(self, request,eid):
        try:
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

     
      def delete(self,request,eid):
            
             if not eid:
                   return Response({
                         "message":"Data not deleted",
                         "errors":"id is invalid",
                   })
             if request.user != Event.objects.get(id=eid).organizer:
                   return Response({
                         "message":"You are not authorized to delete this event",
                         "errors":"authorization error",
                   }, status=status.HTTP_403_FORBIDDEN)
             else:
                   u = Event.objects.get(id=eid).delete()
             
             return Response({
                   "message":"Data Delete",
                   "data":{},
             })

class EventSearch(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'organizer__full_name', 'location']
 


class RSVPApi(APIView):
      def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]  
        elif self.request.method in ['GET', 'PUT', 'DELETE']:
            return [IsAuthenticated()]  
        else:
            return [IsAuthenticated()] 
      
      def post(self,request,eid):
            if not request.user.is_authenticated:
                     return Response({"error": "Invalid Credentials"}, status=401)
            try:
                  event = Event.objects.get(id=eid)
            except Event.DoesNotExist:
                 return Response({"error": "Event not found"}, status=404)

            dataN = {
                  "event": event.id,
                  "user": request.user.id,
                  "status": request.data.get("status")
              }
            serializer = RSVPSerializer(data=dataN)
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

      def patch(self, request,eid,rid):
            try:
                  rsvp = RSVP.objects.get(id=rid, event__id=eid)
            except RSVP.DoesNotExist:
                  return Response({"error": "RSVP not found"}, status=status.HTTP_404_NOT_FOUND)
      
            if rsvp.user != request.user:
                  return Response({"error": "You are not the owner of this RSVP"},
                              status=status.HTTP_403_FORBIDDEN)
      
            serializer = RSVPSerializer(rsvp, data=request.data, partial=True)
      
            if serializer.is_valid():
                  serializer.save()
                  return Response({"message": "RSVP updated successfully", "data": serializer.data})
      
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReviewApi(APIView):
      def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]  
        elif self.request.method in ['GET', 'PUT', 'DELETE']:
            return [IsAuthenticated()]  
        else:
            return [IsAuthenticated()] 
      
      def get(self,request,eid=None):
             if not request.user.is_authenticated:
              return Response({"error": "Invalid Credentials"}, status=401)
             if eid:
                 try:
                     event = Review.objects.filter(event=eid)
                 except Event.DoesNotExist:
                     return Response({"error": "Event not found"}, status=404)
                 
                 queryset = Review.objects.filter(event=eid)
                 serializer = ReviewSerializer(queryset, many=True)
                 return Response({"data": serializer.data})



      def post(self,request,eid):
            if not request.user.is_authenticated:
                     return Response({"error": "Invalid Credentials"}, status=401)
            try:
                  event =Event.objects.get(id=eid)
            except Event.DoesNotExist:
                 return Response({"error": "Event not found"}, status=404)

            dataN = {
                  "event": event.id,
                  "user": request.user.id,
                  "rating": request.data.get("rating"),
                  "comment": request.data.get("comment")
              }
            serializer = ReviewSerializer(data=dataN)
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
