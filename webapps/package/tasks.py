from celery import shared_task

from lib.tools import get_items_from_xml_source, get_item_details


@shared_task
def update_data_from_source():
    from webapps.package.models import Package, Tag
    xml_items = get_items_from_xml_source()
    for item in xml_items:
        arguments = {
            'link': item.get('link'),
            'guid': item.get('guid'),
            'description': item.get('description'),
            'author_email': item.get('author'),
        }
        arguments.update(get_item_details(item.get('link')))
        tags = arguments.pop('tags')
        try:
            obj = Package.objects.get(guid=arguments.get('guid'))
            for key, value in arguments.items():
                setattr(obj, key, value)
        except Package.DoesNotExist:
            obj = Package(**arguments)
        obj.save()
        tags = [Tag.objects.get_or_create(name=value)[0] for value in tags]
        if tags:
            obj.tags.set(tags)
        obj.save()
