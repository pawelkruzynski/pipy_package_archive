from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from elasticsearch_dsl.query import MultiMatch

from lib.tools import paginated_slice
from webapps.package.documents import PackageDocument
from webapps.package.forms import SearchForm


def index(request, *args, **kwargs):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searchstring = form.data.get('searchstring')
            request.session['searchstring'] = searchstring

    else:
        if not request.GET.get('page', False) \
                and request.session.get('searchstring', False):
            del request.session['searchstring']
        form = SearchForm()
        searchstring = request.session.get('searchstring', None)
    if searchstring:
        query = MultiMatch(
            query=searchstring, fields=[
                'title', 'author', 'author_email', 'description',
                'current_version', 'maintainer', 'tag_values'
            ], fuzziness='AUTO'
        )
    else:
        query = 'match_all'
    pagination = settings.FRONT_PAGINATION
    packages_list = PackageDocument.search().query(query)
    page = request.GET.get("page", 1)
    lines = range(packages_list.count())
    paginator = Paginator(lines, pagination)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    context = {
        'form': form,
        'lines': lines,
        'packages': paginated_slice(packages_list, pagination, page),
        'is_paginated': paginator.num_pages > 1
    }
    return render(request, 'package/list.html', context)
