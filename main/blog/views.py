from django.shortcuts import render # pragma: no cover
from django.views.generic import View
from elasticsearch import Elasticsearch
from django.views.decorators.http import require_GET
import json
es = Elasticsearch()


def prepare_data():
    data = open('/Users/catalin/Desktop/ENV/brand-ripplr/main/blog/static/data.txt')
    doc = json.load(data)  # deserialises it
    return doc


def index_data():  # pragma: no cover
    doc = prepare_data()
    for listing in doc['business']:
        es.index(index="business", doc_type='listing', id=listing['id'], body=json.dumps(listing))
    es.indices.refresh(index="business")
    return True


def search(q):
    query = {"query": {"match_phrase_prefix": {"name": q}}}
    response = es.search(index="business", doc_type="listing",body=query)
    return [item['_source'] for item in response['hits']['hits']]


class Index(View):
    template_name = 'blog/index.html'

    def get(self, request):
        query = request.GET.get('q', None)
        context = {}
        if query:
            result = search(query)
            if len(result):
                context['result'] = result
            else:
                context['result'] = [{'name': 'No Results found'}]
        return render(request, self.template_name, context)
