import graphene
from graphi_crud.queries import Queries
from graphi_crud.create_mutation import CreateMutation
from graphi_crud.update_mutation import UpdateMutation
from graphi_crud.delete_mutation import DeleteMutation


Queries.generate_queries(["accounts"])
CreateMutation.generate_mutations(['accounts'])
UpdateMutation.generate_mutations(['accounts'])
DeleteMutation.generate_mutations(['accounts'])


class Query(Queries):
    pass


class Mutation(CreateMutation, UpdateMutation, DeleteMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
