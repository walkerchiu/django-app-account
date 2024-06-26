from graphene import ResolveInfo
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
import graphene

from django_app_account.models import User
from django_app_core.relay.connection import ExtendedConnection


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "last_login",
            "profile",
        )


class TenantsType(graphene.ObjectType):
    domain = graphene.String()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            "id": ["exact"],
            "email": ["iexact", "icontains", "istartswith"],
            "username": ["iexact", "icontains", "istartswith"],
        }
        exclude = (
            "deleted",
            "deleted_by_cascade",
        )
        order_by_field = "email"
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info: ResolveInfo):
        raise Exception("This operation is not allowed!")

    @classmethod
    @login_required
    def get_node(cls, info: ResolveInfo, id):
        try:
            user = cls._meta.model.objects.get(pk=info.context.user.id)
        except cls._meta.model.DoesNotExist:
            raise Exception("Bad Request!")

        return user


class UserConnection(graphene.relay.Connection):
    class Meta:
        node = UserType
