# -*- coding: utf-8 -*-
import collections

from django.db import models

from cms.registry import cms_fields, cms_relateds, cms_managers


def _generate_attributes(schema_attributes, registry):
    """
    Returns a dict witn names an attributes based on schema_attributes.
    The attributes are searched in registry.

    Utility function used by create_model to generates the "fields"
    and "relations" in a model (low-level API).
    """
    attributes = collections.OrderedDict()
    for f_data in schema_attributes:
        try:
            registry_item = registry.get_by_name(f_data.kind)
        except KeyError:
            raise RuntimeError('Field not recognized: %s', f_data.kind)

        field_class = registry_item.klass
        args = f_data.args if f_data.args else tuple()
        kwargs = f_data.kwargs if f_data.kwargs else {}
        attributes[f_data.name] = field_class(*args, **kwargs)
    return attributes


def create_model(django_model_schema):
    """
    Creates a model class in runtime
    """
    # This will be the inner class in the model.
    class Meta:
        pass

    model_name = django_model_schema.name
    #TODO: add custom inheritance if needed, probably we will have CMSModel as base
    #inheritance = django_model_schema.inheritance
    inheritance = (models.Model,)

    # Generate the Fields, Relationships and Managers.
    attributes = collections.OrderedDict()
    schema_attrs = django_model_schema.fields
    schema_rels = django_model_schema.relations
    schema_managers = django_model_schema.managers

    m_fields = _generate_attributes(schema_attrs, cms_fields)
    m_relations = _generate_attributes(schema_rels, cms_relateds)
    m_managers = _generate_attributes(schema_managers, cms_managers)
    attributes.update(m_fields)
    attributes.update(m_relations)
    attributes.update(m_managers)

    #TODO: change this to a good module, the path need to exist on disk
    # how can we handle this ?
    #module = django_model_schema.module
    module_name = __name__
    attributes['__module__'] = module_name

    # Populate Meta inner class.
    for attribute, value in django_model_schema.metadata.items():
        setattr(Meta, attribute, value)
    attributes['Meta'] = Meta

    # Create the class.
    django_model_class = type(str(model_name), inheritance, attributes)
    return django_model_class