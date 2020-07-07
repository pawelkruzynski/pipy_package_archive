from unittest import TestCase, mock

import django
import pytest

from optimo import settings

django.setup()
from webapps.package.models import Package
from webapps.package import tasks
from _collections import OrderedDict


def mock_get_items_from_xml_source():
    return [OrderedDict([
        ('title', 'optimo added to PyPI'),
        ('link', 'https://pypi.org/project/optimo/'),
        ('guid', 'https://pypi.org/project/optimo/'),
        ('description', 'mocked optimo description'),
        ('author', 'optimo@example.com'),
        ('pubDate', 'Mon, 06 Jul 2020 08:46:40 GMT')
    ])]


def mock_get_item_details(url):
    return {
        'author': 'Mocked author',
        'maintainer': 'mock maintainer',
        'tags': ['optimo', 'django'],
        'title': 'mock title',
        'current_version': '1.0.0'
    }


@pytest.mark.django_db
class TestTask(TestCase):

    @mock.patch(
        'webapps.package.tasks.get_items_from_xml_source',
        side_effect=mock_get_items_from_xml_source
    )
    @mock.patch(
        'webapps.package.tasks.get_item_details',
        side_effect=mock_get_item_details
    )
    def test_update_data_from_source(self, mocked_source, mocked_details):
        self.assertEqual(Package.objects.count(), 0)
        tasks.update_data_from_source.apply()
        self.assertEqual(Package.objects.count(), 1)
        self.assertEqual(Package.objects.first().title, 'mock title')
