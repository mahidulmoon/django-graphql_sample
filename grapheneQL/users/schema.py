from graphene_django import DjangoObjectType
import graphene
from django.contrib.auth import get_user_model

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

class Mutation(graphene.ObjectType):
    """
    This class contains the fields of models that are supposed to be 
    mutated.
    """
    create_user = CreateUser.Field()

schema = graphene.Schema(
    mutation=Mutation  # Adding mutations to our schema
)