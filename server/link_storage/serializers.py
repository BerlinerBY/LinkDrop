from rest_framework import serializers
from .models import Collection, Link


class CollectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Collections
    """

    class Meta:
        model = Collection
        fields = (
            'id',
            'title',
            'description',
            'date_of_created',
            'date_of_changed',
            'slug',
        )

class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer for Links
    """
    class Meta:
        model = Link
        fields = (
            'id',
            'title',
            'description',
            'url_field',
            'url_to_image',
            'type_of_link',
            'date_of_created',
            'date_of_changed',
            'slug',
            'collection',
        )