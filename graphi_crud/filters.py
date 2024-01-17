import graphene


class StringFilterKeywordsInputType(graphene.InputObjectType):
    exact = graphene.String()
    contains = graphene.String()
    icontains = graphene.String()
    startswith = graphene.String()
    istartswith = graphene.String()
    endswith = graphene.String()
    iendswith = graphene.String()
    regex = graphene.String()
    iregex = graphene.String()
    isnull = graphene.Boolean()


class NumberFilterKeywordsInputType(graphene.InputObjectType):
    exact = graphene.Int()
    lt = graphene.Int()
    lte = graphene.Int()
    gt = graphene.Int()
    gte = graphene.Int()
    range = graphene.List(graphene.Int)
    isnull = graphene.Boolean()


class DateFilterKeywordsInputType(graphene.InputObjectType):
    exact = graphene.String()
    lt = graphene.String()
    lte = graphene.String()
    gt = graphene.String()
    gte = graphene.String()
    range = graphene.List(graphene.String)
    isnull = graphene.Boolean()
    year = graphene.String()
    month = graphene.String()
    day = graphene.String()
    week_day = graphene.String()
    hour = graphene.String()
    minute = graphene.String()
    second = graphene.String()
    date = graphene.String()
    time = graphene.String()
    iso_year = graphene.String()
    iso_week = graphene.String()
    iso_week_day = graphene.String()

