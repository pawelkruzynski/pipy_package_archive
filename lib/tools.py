import requests
import xmltodict
from bs4 import BeautifulSoup

from optimo import settings


def get_items_from_xml_source():
    response = requests.get(settings.DATA_URL)
    items = xmltodict.parse(response.content).get(
        'rss', {}).get('channel', {}).get('item', {})
    if not items:
        return []
    return items


def get_item_details(url):
    response = requests.get(url)
    if not response.ok:
        return {}
    result = {}
    soup = BeautifulSoup(response.content, 'html.parser')
    author_tag = soup.find('strong', text='Author:')
    if author_tag:
        author = author_tag.parent.find('a')
        result['author'] = author.text if author else ''

    mainainers_tag = soup.find('h3', text='Maintainers')
    if mainainers_tag:
        mainainer = mainainers_tag.parent.findAll(
            'span', {'class': 'sidebar-section__user-gravatar-text'}
        )
        result['maintainer'] = ', '.join([m.text.strip() for m in mainainer])

    tags_tag = soup.find('p', {'class': 'tags'})
    result['tags'] = []
    if tags_tag:
        tags = tags_tag.findAll('span', {'class': 'package-keyword'})
        result['tags'] = [t.text.replace(',', '').strip() for t in tags]
    package_title = soup.find('h1', {'class': 'package-header__name'})
    if package_title:
        result['title'], result['current_version'] = \
            package_title.text.strip().split()
    return result


def paginated_slice(obj, pagination, page=1):
    start = (int(page) - 1) * int(pagination)
    end = (int(page)) * int(pagination)
    return obj[start:end]
