import graphene


class StringFilterKeywordsInputType(graphene.InputObjectType):
    exact = graphene.String()
    icontains = graphene.String()
    istartswith = graphene.String()
    iendswith = graphene.String()


class DateFilterKeywordsInputType(graphene.InputObjectType):
    exact = graphene.String()
    lt = graphene.String()
    lte = graphene.String()
    gt = graphene.String()
    gte = graphene.String()

