from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters


from profiles_api import serializers
from profiles_api import models
from profiles_api import permission
# Create your views here.


class HelloApiView(APIView):
    """Test APIView"""
    serializer_class = serializers.HelloSerializers

    def get(self,request,format=None):
        """Return a list of APIView feature"""
        an_apiview=[
         'Uses HTTP methods as functions (get,post,patch,put,delete)',
         'Is similar to a traditional Django View',
         'Gives you the most control over you application logic',
         'Is mapped manually to URLs'
        ]
        return Response({'message':'Hello','an_apiview':an_apiview})
    def post(self,request):
        """Create a hello message with our name"""
        serializer  = self.serializer_class(data=request.data)
        # print(request.data)
        # serializer=request.data
        ###Start---------------------
        """ At this point we've translated the model instance into Python native datatypes.
        To finalise the serialization process we render the data into json."""
        # from rest_framework.renderers import JSONRenderer
        #
        # json = JSONRenderer().render(request.data)
        # print(json)
        # return Response({'msg':'Hi'})
        ###-----------------END
        if serializer.is_valid():

            name = serializer.validated_data.get('name')
            message  =f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        """Handle the updating an object"""
        return Response({"method":"put"})

    def patch(self,request,pk=None):
        """Handle the partial update of an object"""
        return Response({"method":"patch"})

    def delete(self,request,pk=None):
        """Delete an object"""
        return Response({"method":"delete"})


class HelloViewSet(viewsets.ViewSet):
    """Hadle the ViewSet test"""
    serializer_class = serializers.HelloSerializers

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create,retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code']

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})


    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})



class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializers
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_filter = ('name','email',)
