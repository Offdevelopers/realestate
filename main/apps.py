from __future__ import unicode_literals

from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from algoliasearch_django import AlgoliaIndex


class MainConfig(AppConfig):
    name = 'main'


    def ready(self):
        Property = self.get_model('Property')
        Mortage=self.get_model('Mortage')
        algoliasearch.register(Property)
        algoliasearch.register(Mortage)
        