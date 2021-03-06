# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2018 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from elasticsearch import Elasticsearch

from pygeoapi.provider.base import BaseProvider


class ElasticsearchProvider(BaseProvider):
    """generic Provider ABC"""

    def __init__(self, definition):
        """initializer"""

        BaseProvider.__init__(self, definition)

        url_tokens = self.url.split('/')

        self.index_name = url_tokens[-2]
        self.type_name = url_tokens[-1]
        self.es_host = url_tokens[2]

        self.es = Elasticsearch(self.es_host)

    def query(self):
        """
        query the provider

        :returns: dict of 0..n GeoJSON features
        """

        feature_collection = {
            'type': 'FeatureCollection',
            'features': []
        }

        results = self.es.search(index=self.index_name)

        for feature in results['hits']['hits']:
            feature_collection['features'].append(feature['_source'])

        return feature_collection

    def get(self, identifier):
        """
        query the provider by id

        :param identifier: feature id
        :returns: dict of single GeoJSON feature
        """

        try:
            es_results = self.es.get(self.index_name, doc_type=self.type_name,
                                     id=identifier)
        except Exception as err:
            return None

        return es_results['_source']

    def __repr__(self):
        return '<ElasticsearchProvider> {}'.format(self.url)
