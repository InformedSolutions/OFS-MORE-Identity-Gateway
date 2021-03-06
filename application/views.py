from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import api_view

from application.models import UserDetails, UserDetailsSerializer
from django.http import JsonResponse


serializers = {'user_details': UserDetailsSerializer}


class UserViewSet(viewsets.ModelViewSet):
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
    lookup_field = 'application_id'
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('login_id', 'email', 'magic_link_email', 'magic_link_sms', 'application_id', 'service')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if not queryset.exists():
            raise NotFound(detail="Error 404, resource not found", code=404)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def summary_table(request, name, application_id):
    if request.method == 'GET':
        if name in serializers.keys():
            serializer = serializers[name]
            model = serializer.Meta.model
            records = model.objects.filter(application_id=application_id)
            return JsonResponse(serializer(records[0]).get_summary_table(), safe=False)