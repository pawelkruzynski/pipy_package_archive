import os
import pytest
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from lib.tools import (
    get_item_details,
    get_items_from_xml_source,
    paginated_slice,
)


@pytest.mark.django_db
class TestTools(TestCase):

    def setUp(self) -> None:
        self.good_xml = os.path.join(settings.MOCK_DIR, 'good.xml')
        self.bad_xml = os.path.join(settings.MOCK_DIR, 'bad.xml')

        self.good_html = os.path.join(settings.MOCK_DIR, 'good.html')
        self.bad_html = os.path.join(settings.MOCK_DIR, 'bad.html')

    @patch('lib.tools.requests.get')
    def test_get_items_from_xml_source(self, mock_get):
        with open(self.good_xml, 'rb') as good_xml:
            mock_get.return_value.content = good_xml.read()
            good_items = get_items_from_xml_source()
            self.assertTrue(isinstance(good_items, list))
            self.assertTrue(good_items[0].get('link').startswith('http'))

        with open(self.bad_xml, 'rb') as bad_xml:
            mock_get.return_value.content = bad_xml.read()
            bad_items = get_items_from_xml_source()
            self.assertTrue(isinstance(bad_items, list))
            self.assertTrue(bad_items == [])

    @patch('lib.tools.requests.get')
    def test_get_item_details(self, mock_get):
        with open(self.good_html, 'rb') as good_html:
            mock_get.return_value.content = good_html.read()
            good_details = get_item_details('http://fake.url')
            self.assertTrue(isinstance(good_details, dict))
            self.assertIsNotNone(good_details.get('author', None))
            self.assertTrue(isinstance(good_details.get('tags', None), list))

        with open(self.bad_xml, 'rb') as bad_html:
            mock_get.return_value.content = bad_html.read()
            bad_details = get_item_details('http://fake.url')
            self.assertTrue(isinstance(bad_details, dict))

        mock_get.return_value.ok = False
        not_ok = get_item_details('http://fake.url')
        self.assertTrue(isinstance(not_ok, dict))

    def test_paginated_slice(self):
        sample_obj = range(100)
        pagination = 15
        self.assertEqual(paginated_slice(sample_obj, pagination), range(15))
        self.assertEqual(
            paginated_slice(sample_obj, pagination, 3), range(30, 45)
        )