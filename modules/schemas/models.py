# -*- coding: utf-8 -*-
from mongoengine import document, fields as me_fields


class DjangoFieldSchema(document.EmbeddedDocument):
    """
    Represents a Django Field and its options
    """
    name = me_fields.StringField()
    kind = me_fields.StringField()
    args = me_fields.ListField(me_fields.StringField())
    kwargs = me_fields.DictField()


class DjangoModelSchema(document.Document):
    """
    Represents a Django Model, its fields
    and options
    """
    meta = {
        "db_alias": "schema_alias",
        "collection": "model_schemas"
    }
    name = me_fields.StringField()
    app_name = me_fields.StringField()
    module = me_fields.StringField()
    fields = me_fields.ListField(me_fields.EmbeddedDocumentField(DjangoFieldSchema))
    relations = me_fields.ListField(me_fields.EmbeddedDocumentField(DjangoFieldSchema))
    # ['BoincBaseModel', 'TerritoryModelMixin']
    inheritance = me_fields.ListField(me_fields.StringField())
    # [dict(name='objects', manager='ActiveManager')]
    managers = me_fields.ListField(me_fields.EmbeddedDocumentField(DjangoFieldSchema))
    # inner class Meta:
    metadata = me_fields.DictField()