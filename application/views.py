from rest_framework import mixins
from django_filters import rest_framework as filters
from rest_framework.viewsets import GenericViewSet

from identity_models.identity_models.user_details import UserDetails
from identity_models.identity_models.serializers import UserDetailsSerializer


class UserViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    list:
    List all current users stored in the database
    create:
    Create a new full user in the database
    retrieve:
    List the user with the corresponding primary key (login_id) from the database
    update:
    Update all fields in a record with the corresponding primary key (login_id) from the database
    partial_update:
    Update any amount of fields in  a record with the corresponding primary key (login_id) from the database
    destroy:
    Delete the user with the corresponding primary key (login_id) from the database

    """
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('login_id', 'email', 'magic_link_email', 'magic_link_sms')


class MagicLinkViewSet(mixins.RetrieveModelMixin,
                       GenericViewSet):

    queryset = UserDetails.objects.filter()
    serializer_class = UserDetailsSerializer
    lookup_field = 'magic_link_email'

class EmailViewSet(mixins.RetrieveModelMixin,
                   GenericViewSet):

    queryset = UserDetails.objects.filter()
    serializer_class = UserDetailsSerializer
    lookup_field = 'email'
