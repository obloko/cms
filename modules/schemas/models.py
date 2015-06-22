# -*- coding: utf-8 -*-
from mongoengine import document, fields


class DjangoFieldSchema(document.EmbeddedDocument):
    """
    Represents a Django Field and its options
    """
    name = fields.StringField()
    kind = fields.StringField()
    args = fields.ListField(fields.StringField())
    kwargs = fields.DictField()


class DjangoModelSchema(document.Document):
    """
    Represents a Django Model, its fields
    and options
    """
    meta = {
        "db_alias": "schema_alias",
        "collection": "model_schemas"
    }
    name = fields.StringField()
    app_name = fields.StringField()
    module = fields.StringField()
    attributes = fields.ListField(fields.EmbeddedDocumentField(DjangoFieldSchema))
    relations = fields.ListField(fields.EmbeddedDocumentField(DjangoFieldSchema))
    # ['BoincBaseModel', 'TerritoryModelMixin']
    inheritance = fields.ListField(fields.StringField())
    # [dict(name='objects', manager='ActiveManager')]
    managers = fields.ListField(fields.EmbeddedDocumentField(DjangoFieldSchema))
    # inner class Meta:
    metadata = fields.DictField()