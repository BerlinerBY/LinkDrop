from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist

from .serializers import CollectionSerializer, LinkSerializer
from .models import Collection, Link

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_collection(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            serializer = CollectionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
                {"error": "You must be authenticated to create a collection."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_collections(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            collections = Collection.objects.filter(created_by=user)
            serializer = CollectionSerializer(collections, many=True)
            return Response(serializer.data)
        return Response(
                {"error": "You must be authenticated to view your collections."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_collection(request, collection_id):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            id = collection_id
            collection = Collection.objects.filter(
                created_by=user,
                id=id
                )
            serializer = CollectionSerializer(collection, many=True)
            return Response(serializer.data)
        return Response(
                {"error": "You must be authenticated to view your collections."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_collection(request, collection_id):
    if request.method == 'DELETE':
        user = request.user
        if user.is_authenticated:
            id = collection_id
            collection = Collection.objects.get(
                created_by=user,
                id=id
                )
            if user == collection.created_by:
                collection.delete()
                return Response(
                        {'message': 'Collection delete successfully'},
                        status=status.HTTP_200_OK
                    )
            return Response(
                    {"error": "You must be authenticated to delete your collections."}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(
                {"error": "You must be authenticated to delete your collections."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_collection(request, collection_id):
    if request.method == 'PUT':
        user = request.user
        if user.is_authenticated:
            id = collection_id
            collection = Collection.objects.get(
                created_by=user,
                id=id
                )
            serializer = CollectionSerializer(collection, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "You must be authenticated to update a collection."},
            status=status.HTTP_401_UNAUTHORIZED
            )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_link(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            from .utilities import get_open_graph_data
            data = get_open_graph_data(request.data["url"])
            data["collection"] = request.data["collection"]
            serializer = LinkSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_by=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
                {"error": "You must be authenticated to create a link."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_links(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            links = Link.objects.filter(created_by=user)
            serializer = LinkSerializer(links, many=True)
            return Response(serializer.data)
        return Response(
                {"error": "You must be authenticated to view your links."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_link(request, link_id):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            id = link_id
            link = Link.objects.filter(
                created_by=user,
                id=id
            )
            serializer = LinkSerializer(link, many=True)
            return Response(serializer.data)
        return Response(
                {"error": "You must be authenticated to view your links."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_link(request, link_id):
    if request.method == 'DELETE':
        user = request.user
        if user.is_authenticated:
            id = link_id
            link = Link.objects.get(
                created_by=user,
                id=id
            )
            if user == link.created_by:
                link.delete()
                return Response(
                        {'message': 'Link delete successfully'},
                        status=status.HTTP_200_OK
                    )
            return Response(
                    {"error": "You must be authenticated to delete your links."}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(
                {"error": "You must be authenticated to delete your links."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_link(request, link_id):
    if request.method == 'PUT':
        user = request.user
        if user.is_authenticated:
            id = link_id
            link = Link.objects.get(
                created_by=user,
                id=id                
            )
            serializer = LinkSerializer(link, data=request.data,  partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "You must be authenticated to update a link."},
            status=status.HTTP_401_UNAUTHORIZED
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_link_by_collection(request, collection_id):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            id = collection_id
            links = Link.objects.filter(
                created_by=user,
                collection=id
            )
            serializer = LinkSerializer(links, many=True)
            return Response(serializer.data)
        return Response(
                {"error": "You must be authenticated to view your links."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )