from __future__ import unicode_literals

from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from algoliasearch_django import AlgoliaIndex


class MainConfig(AppConfig):
    name = 'main'


    def ready(self):
        Property = self.get_model('Property')
        algoliasearch.register(Property)