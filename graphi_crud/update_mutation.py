import graphene
from .mutations import MutationsMixin
from .queries import Queries


class UpdateMutation(MutationsMixin):
    @classmethod
    def generate_where_type(cls, model):
        return Queries.generate_where_clause(model)

    @classmethod
    def generate_argument_class(cls, model):
        input_type = cls.generate_input_type(model)
        where_type = cls.generate_where_type(model)
        return type(
            f'Arguments',
            (),
            {
                "where": where_type,
                "input": graphene.List(input_type)
            }
        )

    @classmethod
    def update_mutate(cls, model):
        def mutate(root, info, *args, **kwargs):
            cls.check_permission(info.context.user, model)
            inputs = kwargs.get('input')
            where = kwargs.get('where')

            if not inputs or not isinstance(inputs, list):
                raise Exception('there is no input')
            
            if not where:
                raise Exception('there is no where clause')
            
            updated_objects = []

            for _input in inputs:
                many_to_many_input, _input = cls.resolve_many_to_many(model, _input)
                print(many_to_many_input)
                _input = cls.resolve_related_objects_from_input(model, _input)
                queryset = model.objects.all()
                query = Queries.query_set_builder(where)
                queryset = queryset.filter(**query)
                for obj in queryset:
                    for field, value in _input.items():
                        setattr(obj, field, value)
                    for field, value in many_to_many_input.items():
                        getattr(obj, field).set(value)

                    obj.save()
                    updated_objects.append(obj)


            return {
                'data': updated_objects,
                'affected_rows': len(updated_objects)
            }
        return mutate

    @classmethod
    def generate_update_mutation_class(cls, model):
        argument_class = cls.generate_argument_class(model)
        _ =  type(
            f'{model.__name__}UpdateMutation',
            (graphene.Mutation,),
            {
                'Arguments': argument_class,
                'data': graphene.List(cls.get_or_generate_django_object_type(model)),
                'affected_rows': graphene.Int(),
                'mutate': cls.update_mutate(model)
            }
        )
        return _

    @classmethod
    def generate_mutations(cls, _apps):
        models = cls.find_all_models(_apps)
        for model in models:
            update_mutation_class = cls.generate_update_mutation_class(model)
            setattr(cls, f'update_{model.__name__.lower()}', update_mutation_class.Field())

