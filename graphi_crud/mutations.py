from .graphi_types import Types
import graphene
from django.db.utils import IntegrityError

class MutationsMixin(Types, graphene.ObjectType):
    pass


