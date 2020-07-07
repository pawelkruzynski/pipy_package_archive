import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from webapps.package.documents import PackageDocument

class PackageDocumentSerializer(DocumentSerializer):
    """Serializer for the Book document."""

    class Meta(object):
        """Meta options."""

        # Specify the correspondent document class
        document = PackageDocument
        tags = serializers.SerializerMethodField()
        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            'id',
            'author',
            'author_email',
            'description',
            'title',
            'current_version',
            'maintainer',
            'tag_values'
        )