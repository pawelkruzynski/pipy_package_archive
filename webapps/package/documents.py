from django_elasticsearch_dsl import (
    Document,
    fields,
    Index,
)

from webapps.package.models import Package

package_index = Index('package')

package_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@package_index.doc_type
class PackageDocument(Document):
    tag_values = fields.TextField(attr='get_tags')

    class Meta:
        doc_type = 'package_document'

    class Django:
        model = Package
        fields = [
            'id',
            'author',
            'author_email',
            'description',
            'title',
            'current_version',
            'maintainer',
        ]
