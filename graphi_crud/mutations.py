from .graphi_types import Types
import graphene
from django.db.utils import IntegrityError
from graphene_file_upload.scalars import Upload
from django.db import models
from django.contrib.auth import get_user_model


class MutationsMixin(Types, graphene.ObjectType):
    user_model = get_user_model()

    @classmethod
    def map_field_to_graphene_type(cls, field_name: str, model):
        if field_name.endswith("_id") and model == cls.user_model:
            return graphene.String(default_value="default_id")

        if field_name.endswith("_ids"):
            return graphene.List(graphene.String)

        field = model._meta.get_field(field_name)
        field_type = field.get_internal_type()
        type_mapping = {
            'CharField': graphene.String(),
            'IntegerField': graphene.Int(),
            'BooleanField': graphene.Boolean(),
            'DateField': graphene.String(),
            'DateTimeField': graphene.String(),
            'DecimalField': graphene.Float(),
            'EmailField': graphene.String(),
            'FileField': graphene.String(),
            'FloatField': graphene.Float(),
            'ImageField': Upload(),
            'PositiveIntegerField': graphene.Int(),
            'PositiveSmallIntegerField': graphene.Int(),
            'SlugField': graphene.String(),
            'SmallIntegerField': graphene.Int(),
            'TextField': graphene.String(),
            'TimeField': graphene.String(),
            'UUIDField': graphene.String(),
            'BigIntegerField': graphene.Int(),
            'BinaryField': graphene.String(),
            'PositiveBigIntegerField': graphene.Int(),
            'PositiveDecimalField': graphene.Float(),
            'URLField': graphene.String(),
            'AutoField': graphene.Int(),
            'BigAutoField': graphene.Int(),
            'ForeignKey': graphene.String(),
            'JSONField': graphene.JSONString(),
        }
        return type_mapping.get(field_type)

    @classmethod
    def get_mutation_fields(cls, model):
        new_fields = []
        excluded_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

        for field_name in cls.get_fields(model):
            field = model._meta.get_field(field_name)

            if field_name in excluded_fields:
                continue

            if hasattr(field, 'primary_key'):
                if field.primary_key:
                    continue
            
            if not isinstance(field, models.Field):
                continue

            if field.get_internal_type() in ['ForeignKey', 'OneToOneField']:
                new_fields.append(f"{field_name}_id")
            elif field.get_internal_type() == 'ManyToManyField':
                new_fields.append(f"{field_name}_ids")
            else:
                new_fields.append(field_name)

        return new_fields

    @classmethod
    def generate_input_type(cls, model):
        fields = cls.get_mutation_fields(model)
        return type(
            f"{model.__name__}InputType",
            (graphene.InputObjectType, ),
            {
                field: cls.map_field_to_graphene_type(field, model) for field in fields
            }
        )

    @classmethod
    def resolve_related_objects_from_input(cls, model, _input: dict, info=None):
        related_objects = {}
        for input_field in _input:
            if input_field.endswith('_id'):
                field_name = input_field.replace('_id', '')
                related_model = model._meta.get_field(field_name).related_model
                if related_model == cls.user_model and _input[input_field] == "default_id":
                    if info and info.context.user:
                        _input[input_field] = info.context.user.id
                    else:
                        _input[input_field] = None
                try:
                    if _input[input_field] != None:
                        related_objects[field_name] = related_model.objects.get(pk=_input[input_field])
                except related_model.DoesNotExist:
                    raise Exception(f'{related_model.__name__} with id {_input[input_field]} does not exist.')
                except Exception as e:
                    raise Exception(f"{input_field} {e}")
            elif input_field.endswith('_ids'):
                field_name = input_field.replace('_ids', '')
                related_model = model._meta.get_field(field_name).related_model
                related_objects[field_name] = related_model.objects.filter(pk__in=_input[input_field])
            else:
                related_objects[input_field] = _input[input_field]
        return related_objects

    @classmethod
    def resolve_many_to_many(cls, model, _input: dict):
        related_objects = {}
        _input_copy = _input.copy()
        for input_field in _input:
            if input_field.endswith('_ids'):
                field_name = input_field.replace('_ids', '')
                related_model = model._meta.get_field(field_name).related_model
                related_objects[field_name] = related_model.objects.filter(pk__in=_input[input_field])
                del _input_copy[input_field]

        return related_objects, _input_copy

    @classmethod
    def check_permission(cls, user, model):
        if not hasattr(model, 'graphql_permissions'):
            return True

        if not model.graphql_permissions:
            return True

        if not user.is_authenticated:
            raise Exception('Permission Denied')
        
        if model.graphql_permissions == ('is_authenticated',):
            return True

        if not user.has_perms(model.graphql_permissions):
            raise Exception('Permission Denied')
        
        return True


