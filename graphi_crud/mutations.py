from .graphi_types import Types
import graphene

class Mutations(Types, graphene.ObjectType):
    @classmethod
    def generate_argument_class(cls, model):
        fields = cls.get_fields(model)
        return type(
            f'Argument',
            (graphene.InputObjectType,),
            {field: graphene.String() for field in fields}
        )
    
    @classmethod
    def generate_mutation_class(cls, model):
        argument_class = cls.generate_argument_class(model)
        _ =  type(
            f'{model.__name__}Mutation',
            (graphene.Mutation,),
            {
                'Argument': argument_class,
                'data': graphene.Field(cls.get_or_generate_django_object_type(model)),
                'mutate': cls.create_mutate(model)
            }
        )
        return _
    
    @classmethod
    def create_mutate(cls, model):
        def mutate(self, info, **kwargs):
            data = kwargs.get('data')
            return model.objects.create(**data)
        return mutate
    
    @classmethod
    def generate_mutations(cls, _apps):
        models = cls.find_all_models(_apps)
        for model in models:
            mutation_class = cls.generate_mutation_class(model)
            setattr(cls, f'create_{model.__name__.lower()}', mutation_class.Field())