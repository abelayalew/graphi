import graphene

from graphi_crud.queries import Queries

Queries.generate_queries(["accounts"])

class Query(Queries):
    pass


schema = graphene.Schema(query=Query)
