# Django Graphene CRUD Generator

## Installation
```
pip install graphi-crud
```

## Usage

```
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


schema = graphene.Schema(query=Query, mutation=Mutation)

```

register your `schema` in settings and your good to go

## writing Queries

```
{
  user(where: {email: {icontains: "user"}}, offset: 10, limit: 10){
    id
    email
  }
}
```

## create mutation example

```
mutation{
  createUser(inputs: {email: "user@gmail.com", username: "newuser"}){
    data{
      id
      email
    }
  }
}
```

## update mutation example

```
mutation{
  updateUser(inputs: {lastLogin: "2023-12-12"}, where: {email: {icontains: "someuser"}}){
    affectedRows
    data {
      id
      username
    }
  }
}
```

## delete mutation examples

```
mutation{
  deleteUser(where: {email: {icontains: "someuser"}}){
    affectedRows
  }
}
```

## permissions
add `graphql_permissions` attribute on your model class with a list of permissions
example:
```  
  class Employee(models.Model):
      ...fields...
      graphql_permissions = ['accounts.add_employee', 'accounts.change_employee']
```