from .graphi_types import Types
import graphene
from django.db.utils import IntegrityError

class MutationsMixin(Types, graphene.ObjectType):
    @classmethod
    def map_field_to_graphene_type(cls, field):
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
            'BigAutoField': graphene.Int()
        }
        return type_mapping.get(field_type)
    @classmethod
    def generate_input_type(cls, model):
        fields = cls.get_fields(model)
        return type(
            f"{model.__name__}InputType",
            (graphene.InputObjectType, ),
            {
                field: cls.map_field_to_graphene_type(model._meta.get_field(field)) for field in fields
            }
        )
    

    @classmethod
    def check_permission(user, model):
        if not user.is_authenticated:
            raise Exception('Permission Denied')
        
        if not hasattr(model, 'graphql_permissions'):
            return True
        
        if not model.graphql_permissions:
            return True
        
        if not user.has_perms(model.graphql_permissions):
            raise Exception('Permission Denied')
        
        return True


