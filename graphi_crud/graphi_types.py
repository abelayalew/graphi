from graphene_django import DjangoObjectType
from django.apps import apps

class Types:
    django_object_types = dict()

    objects_generated = False

    @classmethod
    def get_or_generate_django_object_type(cls, model):
        if model not in cls.django_object_types:
            cls.django_object_types[model] = cls.generate_model_type(model)
        return cls.django_object_types[model]

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
        for field in model._meta.get_fields():
            if field.name not in excluded_fields and hasattr(model, field.name):
                try:
                    if getattr(model, field.name).reverse:
                        continue
                except AttributeError:
                    pass
                fields.append(field.name)
        return fields

    @classmethod
    def generate_model_type(cls, model):
        if model.__name__ == "Employee":
            print('-'*10)
            print("model:", model)
            print(cls.get_fields(model))
        model_type = type(
            f"{model.__name__.lower()}",
            (DjangoObjectType,),
            {
                "Meta": type(
                    "Meta",
                    (),
                    {"model": model, "fields": cls.get_fields(model)},
                ),
            },
        )
        return model_type
    
    @classmethod
    def find_all_models(cls, _apps: list):
        all_apps = [apps.get_app_config(app) for app in _apps]
        for app in all_apps:
            models = app.get_models()
            for model in models:
                if hasattr(model, "graphql_exclude"):
                    if model.graphql_exclude:
                        continue
                yield model
