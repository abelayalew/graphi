import graphene
from .mutations import MutationsMixin


class CreateMutation(MutationsMixin):
    @classmethod
    def generate_argument_class(cls, model):
        input_type = cls.generate_input_type(model)
        return type(
            f'Arguments',
            (),
            {
                "inputs": graphene.List(input_type)
            }
        )

    @classmethod
    def create_mutate(cls, model):
        def mutate(root, info, *args, **kwargs):
            cls.check_permission(info.context.user, model)
            inputs = kwargs.get('inputs')

            if not inputs or not isinstance(inputs, (list, dict)):
                raise Exception('Invalid Inputs, please provide a list of inputs or a single input object.')

            if isinstance(inputs, dict):
                inputs = [inputs]

            created_objects = []
            for _input in inputs:
                many_to_many_input, _input = cls.resolve_many_to_many(model, _input)
                _input = cls.resolve_related_objects_from_input(model, _input)
                instance = model.objects.create(**_input)

                for field, value in many_to_many_input.items():
                    getattr(instance, field).set(value)

                created_objects.append(instance)

            return {
                'data': created_objects,
                'affected_rows': len(created_objects)
            }
        return mutate

    @classmethod
    def generate_create_mutation_class(cls, model):
        argument_class = cls.generate_argument_class(model)
        _ =  type(
            f'{model.__name__}CreateMutation',
            (graphene.Mutation,),
            {
                'Arguments': argument_class,
                'data': graphene.List(cls.get_or_generate_django_object_type(model)),
                'affected_rows': graphene.Int(),
                'mutate': cls.create_mutate(model)
            }
        )
        return _

    @classmethod
    def generate_mutations(cls, _apps):
        models = cls.find_all_models(_apps)
        for model in models:
            create_mutation_class = cls.generate_create_mutation_class(model)
            setattr(cls, f'create_{model.__name__.lower()}', create_mutation_class.Field())
