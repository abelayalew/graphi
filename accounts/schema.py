import graphene
from graphene_django import DjangoObjectType
from accounts.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class SignUpMutation(graphene.Mutation):
    class Argument:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()
    
    data = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, *args, **kwargs):
        return SignUpMutation(data=User.objects.first())


class Mutation(graphene.ObjectType):
    signup = SignUpMutation.Field()
