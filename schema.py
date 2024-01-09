import graphene

from graphi_crud.queries import Queries
from graphi_crud.create_mutation import CreateMutation


Queries.generate_queries(["accounts"])
CreateMutation.generate_mutations(['accounts'])

class Query(Queries):
    pass

class Mutation(CreateMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
