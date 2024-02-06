import graphene
from .mutations import MutationsMixin
from .queries import Queries


class DeleteMutation(MutationsMixin):
   
    @classmethod
    def generate_where_type(cls, model):
        return Queries.generate_where_clause(model)

    @classmethod
    def generate_argument_class(cls, model):
        where_type = cls.generate_where_type(model)
        return type(
            f'Arguments',
            (),
            {
                "where": where_type,
            }
        )

    @classmethod
    def delete_mutate(cls, model):
        def mutate(root, info, *args, **kwargs):
            cls.check_permission(info.context.user, model)
            where = kwargs.get('where')

            if not where:
                raise Exception('there is no where clause')
            
            deleted_objects = []

            queryset = model.objects.all()
            query = Queries.query_set_builder(where)
            queryset = queryset.filter(**query)
            for obj in queryset:
                obj.delete()
                deleted_objects.append(obj)

            return {
                'affected_rows': len(deleted_objects)
            }
        return mutate

    @classmethod
    def generate_delete_mutation_class(cls, model):
        argument_class = cls.generate_argument_class(model)
        _ =  type(
            f'{model.__name__}DeleteMutation',
            (graphene.Mutation,),
            {
                'Arguments': argument_class,
                'affected_rows': graphene.Int(),
                'mutate': cls.delete_mutate(model)
            }
        )
        return _

    @classmethod
    def generate_mutations(cls, _apps):
        models = cls.find_all_models(_apps)
        for model in models:
            delete_mutation_class = cls.generate_delete_mutation_class(model)
            setattr(cls, f'delete_{model.__name__.lower()}', delete_mutation_class.Field())

