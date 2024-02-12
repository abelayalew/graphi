from .graphi_types import Types
import graphene
from django.db.utils import IntegrityError


class MutationsMixin(Types, graphene.ObjectType):
    @classmethod
    def map_field_to_graphene_type(cls, field_name: str, model):
        if field_name.endswith("_pk"):
            return graphene.String()

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
            'ImageField': graphene.String(),
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
        }
        return type_mapping.get(field_type)

    @classmethod
    def get_mutation_fields(cls, model):
        new_fields = []
        excluded_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

        for field_name in cls.get_fields(model):
            field = model._meta.get_field(field_name)
            if field.primary_key:
                continue
            if field_name in excluded_fields:
                continue

            if field.get_internal_type() == 'ForeignKey':
                new_fields.append(f"{field_name}_pk")
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
    def resolve_related_objects_from_input(cls, model, _input: dict):
        related_objects = {}
        for input_field in _input:
            if input_field.endswith('_pk'):
                field_name = input_field.replace('_pk', '')
                related_model = model._meta.get_field(field_name).related_model
                try:
                    related_objects[field_name] = related_model.objects.get(pk=_input[input_field])
                except related_model.DoesNotExist:
                    raise Exception(f'{related_model.__name__} with pk {_input[input_field]} does not exist.')
            else:
                related_objects[input_field] = _input[input_field]
        return related_objects

    @classmethod
    def check_permission(cls, user, model):
        if not hasattr(model, 'graphql_permissions'):
            return True

        if not model.graphql_permissions:
            return True

        if not user.is_authenticated:
            raise Exception('Permission Denied')

        if not user.has_perms(model.graphql_permissions):
            raise Exception('Permission Denied')
        
        return True


