import graphene

from graphi_crud.queries import Queries
from graphi_crud.mutations import Mutations


Queries.generate_queries(["accounts"])
Mutations.generate_mutations(['accounts'])

class Query(Queries):
    pass

class Mutation(Mutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
