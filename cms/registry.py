# -*- coding: utf-8 -*-
from collections import namedtuple
import inspect
import threading

from django.db import models as django_models
from django.db.models import fields as django_fields
from django.db.models.fields import related as django_related
from django.utils.lru_cache import lru_cache


# Represents an item in the registry
RegistryItem = namedtuple('RegistryItem', 'name klass')


class BaseRegistry(object):
    """
    Base class for registry
    """
    def __init__(self, populate=True):
        self.initialized = False
        self._registry = {}
        # Lock for thread-safe population.
        self._lock = threading.Lock()
        if populate:
            self.populate()

    def populate(self):
        """
        Populates the registry
        """
        raise NotImplementedError

    def register(self, obj, name):
        """
        Registers the obj with the name in the registry
        If name already exist in the registry raise RuntimeError
        """
        if name in self._registry:
            raise RuntimeError('The key %s already exist', name)

        item = RegistryItem(name, obj)
        self._registry[name] = item

    def get_by_name(self, name):
        """
        Returns the object associated with name
        If name is not in the registry it raises KeyError
        """
        # If name is not in data raise an exception.
        return self._registry[name]


class FieldRegistry(BaseRegistry):
    """
    Maps a name with a field class

    Example:
        >>> registry = FieldRegistry()
        >>> registry.get_by_name('CharField')
        django.db.models.fields.CharField
        >>>

        >>> registry.register(CustomField, 'MyCustomField')
        >>> registry.get_by_name('MyCustomField')
        path.to.module.CustomField
        >>>
    """
    @lru_cache(maxsize=None)
    def _get_django_fields(self):
        # Get all the classes inside the module.
        all_classes = inspect.getmembers(django_fields, inspect.isclass)
        cField = django_fields.Field
        # get all the subclasses of Field.
        field_classes = [t[1] for t in all_classes if issubclass(t[1], cField)]
        return field_classes

    def populate(self):
        """
        Overwritten
        """
        with self._lock:
            if self.initialized:
                return

            field_classes = self._get_django_fields()
            for field in field_classes:
                self.register(field, field.__name__)
            self.initialized = True


class RelatedRegistry(FieldRegistry):
    LOOKUP_NAMES = (
        'ForeignKey',
        'OneToOneField',
        'ManyToManyField'
    )

    @lru_cache(maxsize=None)
    def _get_django_fields(self):
        """
        Overwritten
        """
        # Get all the classes inside the module.
        all_classes = inspect.getmembers(django_related, inspect.isclass)
        names = RelatedRegistry.LOOKUP_NAMES
        # get all the subclasses of Field.
        field_classes = [t[1] for t in all_classes if t[1].__name__ in names]
        return field_classes


class ManagerRegistry(FieldRegistry):
    LOOKUP_NAMES = (
        'Manager'
    )

    @lru_cache(maxsize=None)
    def _get_django_fields(self):
        """
        Overwritten
        """
        # Get all the classes inside the module.
        all_classes = inspect.getmembers(django_models, inspect.isclass)
        names = ManagerRegistry.LOOKUP_NAMES
        # get all the subclasses of Field.
        field_classes = [t[1] for t in all_classes if t[1].__name__ in names]
        return field_classes


# Initialize the registries.
cms_fields = FieldRegistry()
cms_relateds = RelatedRegistry()
cms_managers = ManagerRegistry()