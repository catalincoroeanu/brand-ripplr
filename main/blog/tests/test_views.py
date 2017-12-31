# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .. import views
from django.core.urlresolvers import reverse
from django.test import Client


class TestElasticSearch:

    def test_prepare_data(self):
        doc = views.prepare_data()
        listings_count = len(doc['business'])

        assert listings_count == 500, 'Should return 500 listings'

    def test_search(self):
        q = 'AAA'
        response = views.search(q)

        assert int(response[0]['id']) == 3014
        assert q in response[0]['name'], 'Q Should be part of the response'
        assert response[0]['name'] == 'AAA Service Center', "Response['name'] should be exact match"


class TestIndex:

    def test_index(self):
        c = Client()
        query = {"q": "AAA"}
        response = c.post(reverse('Index'), {"test": "sample date"})
        assert response.status_code == 405, 'Should return 405 - Method not Allowed'

        response = c.get(reverse('Index'), query)
        assert response.status_code == 200, 'Should return Status Code 200'
        assert len(response.context['result']) == 1, 'Should return 1 item in Response List'
        assert query['q'] in response.context['result'][0]['name'], "Query term should be in Result"

        response = c.get(reverse('Index'), {"q": "1234567"})
        assert response.status_code == 200, 'Should return Status Code 200'
        assert response.context['result'][0]['name'] == 'No Results found', "Query return no results"



