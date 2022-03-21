from graphene_django import DjangoObjectType
import graphene
from django.contrib.auth import get_user_model
#################################### create user #################################
User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class CreateUser(graphene.Mutation):
    """
    This is the main class where user object is created.
    This class must implement a mutate method.
    """
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **user_data):
        user = User(
            first_name=user_data.get('first_name'),
            username=user_data.get('username'),
            email=user_data.get('email'),
        )
        user.set_password(user_data.password)  # This will hash the password

        user.save()
        return CreateUser(user=user)


# class Mutation(graphene.ObjectType):
#     """
#     This class contains the fields of models that are supposed to be
#     mutated.
#     """
#     create_user = CreateUser.Field()

# schema = graphene.Schema(
#     mutation=Mutation  # Adding mutations to our schema
# )


#################################### create user #################################


#################################### update user #################################
class UpdateUser(graphene.Mutation):
        class Arguments:
            id = graphene.ID()
            username = graphene.String()
            email = graphene.String()
            first_name = graphene.String()
            last_name = graphene.String()

        user = graphene.Field(UserType)

        @classmethod
        def mutate(cls, root, info, id, **update_data):
            user = User.objects.filter(id=id)
            if user:
                params = update_data
                user.update(**{k: v for k, v in params.items() if params[k]})
                return UpdateUser(user=user.first())
            else:
                print('User with given ID does not exist.')




#################################### update user #################################


#################################### get user #################################

class QueryType(graphene.ObjectType):
        """
        This is what read query looks like:
            query {
                  user(id or username like-> username:"boopDog") {
                    firstName
                    lastName
                    ... -> fetch fields
                  }
                }
        """
        user = graphene.Field(
            UserType,
            id=graphene.String(),
            username=graphene.String()
        )

        @staticmethod
        def resolve_user(*args, **kwargs):
            return User.objects.filter(**kwargs).first()


#################################### get user #################################


#################################### delete user #################################
class DeleteUser(graphene.Mutation):
        class Arguments:
            id = graphene.ID()

        user = graphene.Field(UserType)

        @classmethod
        def mutate(cls, root, info, id):
            user = User.objects.get(id=id)
            user.delete()
            return DeleteUser(user)
    
    
     

#################################### delete user #################################


class Mutation(graphene.ObjectType):
        """
        This class contains the fields of models that are supposed to be 
        mutated.
        """
        create_user = CreateUser.Field()
        update_user = UpdateUser.Field()


schema = graphene.Schema(
    query=QueryType,
    mutation=Mutation  # Adding mutations to our schema
)