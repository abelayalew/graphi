from .graphi_types import Types
import re
import graphene
from django.apps import apps
from graphene import List, ObjectType
from .filters import StringFilterKeywordsInputType, DateFilterKeywordsInputType, NumberFilterKeywordsInputType




class Queries(Types, ObjectType):
    non_filterable_field_types = [
        "ManyToManyRel",
        "ManyToOneRel",
        "OneToOneRel",
        "ImageField",
        "FileField",
        "ForeignKey",
        "JSONField",
    ]

    @classmethod
    def where_clause_from_internal_field(cls, internal_type):
        date_fields = ["DateTimeField", "DateField"]
        number_fields = ["IntegerField", "FloatField", "DecimalField"]

        if internal_type in cls.non_filterable_field_types:
            return None

        if internal_type in date_fields:
            return DateFilterKeywordsInputType()
        
        if internal_type in number_fields:
            return NumberFilterKeywordsInputType()

        return StringFilterKeywordsInputType()

    @classmethod
    def generate_where_clause(cls, model):
        attrs = {}
        for field in model._meta.fields:
            internal_type = field.get_internal_type()
            field_where_clause = cls.where_clause_from_internal_field(internal_type)
            if not field_where_clause:
                continue

            attrs[field.name] = field_where_clause

        return type(
            f"{model.__name__}FilterCLass", (graphene.InputObjectType,), {**attrs}
        )()

    @classmethod
    def get_fields(cls, model):
        excluded_fields = []
        if hasattr(model, "graphql_fields") and hasattr(
            model, "graphql_exclude_fields"
        ):
            raise Exception(
                f"please remove graphql_fields or graphql_exclude_fields from {model}"
            )

        if hasattr(model, "graphql_fields"):
            if not isinstance(model.graphql_fields, (list, tuple)):
                raise Exception(f"graphql_fields must be iterable on model {model}")
            return model.graphql_fields

        if hasattr(model, "graphql_exclude_fields"):
            if not isinstance(model.graphql_exclude_fields, (list, tuple)):
                raise Exception(
                    f"graphql_exclude_fields must be iterable on model {model}"
                )
            excluded_fields = model.graphql_exclude_fields
        fields = []
        for field in model._meta.fields:
            if field.name not in excluded_fields:
                fields.append(field.name)
        return fields

    @classmethod
    def query_set_builder(cls, where: dict):
        _ = {}
        if not where:
            return _

        for field, lookup in where.items():
            for lookup_word, value in lookup.items():
                _[f"{field}__{lookup_word}"] = value
        return _

    @classmethod
    def generate_resolve_method(cls, model):        
        def _(root, info, *args, **kwargs):
            where = kwargs.get("where")
            offset = kwargs.get("offset")
            limit = kwargs.get("limit")

            queryset = model.objects.all()
            query = cls.query_set_builder(where)
            queryset = queryset.filter(**query)

            if offset:
                queryset = queryset[offset:]

            if limit:
                queryset = queryset[:limit]

            return queryset

        return _

    @classmethod
    def to_snake_case(cls, name):
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        name = re.sub("__([A-Z])", r"_\1", name)
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        return name.lower()

    @classmethod
    def generate_queries(cls, _apps: list):
        models = cls.find_all_models(_apps)
        for model in models:
            if hasattr(model, "graphql_exclude"):
                if model.graphql_exclude:
                    continue
            where_clause = cls.generate_where_clause(model)
            model_type = cls.get_or_generate_django_object_type(model)
            resolve_method = cls.generate_resolve_method(model)
            query_name = cls.to_snake_case(model.__name__)
            setattr(
                cls,
                query_name,
                List(
                    model_type,
                    where=where_clause,
                    offset=graphene.Int(),
                    limit=graphene.Int(),
                ),
            )
            setattr(cls, f"resolve_{query_name}", resolve_method)

    @classmethod
    def find_all_models(cls, _apps: list):
        all_apps = [apps.get_app_config(app) for app in _apps]
        for app in all_apps:
            models = app.get_models()
            for model in models:
                yield model
