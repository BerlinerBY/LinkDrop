from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist

from .serializers import CollectionSerializer, LinkSerializer, CreateLinkSerializer
from .models import Collection, Link

from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, OpenApiExample
from drf_spectacular.utils import extend_schema, inline_serializer

### Collections' part
@extend_schema(
    tags=["Collection"],
    summary="Create collection",
    request=CollectionSerializer,
    responses={
        status.HTTP_201_CREATED: CollectionSerializer,
        status.HTTP_400_BAD_REQUEST: CollectionSerializer.errors,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to create a collection.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]    
)
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
    

@extend_schema(
    tags=["Collection"],
    summary="Read collections",
    request=[],
    responses={
        status.HTTP_200_OK: CollectionSerializer(many=True),
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to view your collections.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_collections(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            collections = Collection.objects.filter(created_by=user)
            serializer = CollectionSerializer(collections, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
                {"error": "You must be authenticated to view your collections."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

@extend_schema(
    tags=["Collection"],
    summary="Read collection",
    request=[],
    responses={
        status.HTTP_200_OK: CollectionSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to view your collections.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
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
            return Response(serializer.data,  status=status.HTTP_200_OK)
        return Response(
                {"error": "You must be authenticated to view your collections."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@extend_schema(
    tags=["Collection"],
    summary="Delete collection",
    request=[],
    responses={
        status.HTTP_200_OK: inline_serializer(
            "Collection delete successfully.",
            fields={'message': serializers.CharField()}
        ),
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to delete your collections.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
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

@extend_schema(
    tags=["Collection"],
    summary="Update collection",
    request=CollectionSerializer,
    responses={
        status.HTTP_200_OK: CollectionSerializer,
        status.HTTP_400_BAD_REQUEST: CollectionSerializer.errors,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to update your collections.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
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
    
### Links' part
@extend_schema(
    tags=["Link"],
    summary="Create link",
    request=CreateLinkSerializer,
    responses={
        status.HTTP_201_CREATED: LinkSerializer,
        status.HTTP_400_BAD_REQUEST: LinkSerializer.errors,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to create a link.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_link(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            from .utilities import get_open_graph_data
            data = get_open_graph_data(request.data["url_field"])
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

@extend_schema(
    tags=["Link"],
    summary="Read links",
    request=[],
    responses={
        status.HTTP_200_OK: LinkSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to create a link.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_links(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            links = Link.objects.filter(created_by=user)
            serializer = LinkSerializer(links, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
                {"error": "You must be authenticated to view your links."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@extend_schema(
    tags=["Link"],
    summary="Read link",
    request=[],
    responses={
        status.HTTP_200_OK: LinkSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to create a link.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
                {"error": "You must be authenticated to view your links."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
@extend_schema(
    tags=["Link"],
    summary="Delete link",
    request=[],
    responses={
        status.HTTP_200_OK: inline_serializer(
            "Link delete successfully.",
            fields={'message': serializers.CharField()}
        ),
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to delete your links.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
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
    
@extend_schema(
    tags=["Link"],
    summary="Update link",
    request=LinkSerializer,
    responses={
        status.HTTP_200_OK: LinkSerializer,
        status.HTTP_400_BAD_REQUEST: LinkSerializer.errors,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to update your link.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
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


@extend_schema(
    tags=["Link"],
    summary="Links by collection",
    request=[],
    responses={
        status.HTTP_200_OK: LinkSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "You must be authenticated to view your links.",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
                {"error": "You must be authenticated to view your links."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )