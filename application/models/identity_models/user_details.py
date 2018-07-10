import json
import os
import requests

from uuid import uuid4, UUID

from rest_framework import serializers
from django.db import models
from django.forms import model_to_dict


class ApiCalls(models.Manager):

    identity_prefix = os.environ.get('APP_IDENTITY_URL')

    def get_record(self, email=None, pk=None, magic_link_email=None, magic_link_sms=None, application_id=None):  # Get a list of records by query.
        if email is not None:
            query_url = self.identity_prefix + 'api/v1/user/?email=' + email
        elif pk is not None:
            query_url = self.identity_prefix + 'api/v1/user?login_id=' + pk
        elif magic_link_email is not None:
            query_url = self.identity_prefix + 'api/v1/user?magic_link_email=' + magic_link_email
        elif magic_link_sms is not None:
            query_url = self.identity_prefix + 'api/v1/user?magic_link_sms=' + magic_link_sms
        elif application_id is not None:
            query_url = self.identity_prefix + 'api/v1/user?application_id=' + application_id

        response = requests.get(query_url)

        if response.status_code == 200:
            response.record = json.loads(response.content.decode("utf-8"))[0]
        else:
            response.record = None

        return response

    def create(self, **kwargs):  # Create a record.
        model_record = UserDetails()
        model_dict = model_to_dict(model_record)
        request_params = {**model_dict, **kwargs}
        if not isinstance(request_params['application_id'], UUID):
            raise TypeError('The application id must be an instance of uuid')

        response = requests.post(self.identity_prefix + 'api/v1/user/', data=request_params)

        return response

    def put(self, user_details_record, **kwargs):  # Update a record.
        response = requests.put(self.identity_prefix + 'api/v1/user/' + user_details_record['login_id'] + '/', data=user_details_record)
        return response


class UserDetails(models.Model):
    """
    login_id:
    Test
    """
    # Managers
    objects = models.Manager()
    api = ApiCalls()

    login_id = models.UUIDField(primary_key=True, default=uuid4, help_text="Unique UUID4 Identifier")
    application_id = models.UUIDField(db_column='application_id')
    email = models.CharField(max_length=100, blank=True, help_text="The Email Address of the applicant, using the following regex:"
                                                                   " ^(07\d{8,12}|447\d{7,11}|00447\d{7,11}|\+447\d{7,11})$")
    mobile_number = models.CharField(max_length=20, blank=True,
                                     help_text="The mobile number of the applicant, using following regex:"
                                               " ^([a-zA-Z0-9_\-\.']+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    add_phone_number = models.CharField(max_length=20, blank=True, help_text="The additional mobile number of the applicant, using following regex:"
                                               " ^([a-zA-Z0-9_\-\.']+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    email_expiry_date = models.IntegerField(blank=True, null=True, help_text="The Linux Time Epoch at which the email magic link will expire")
    sms_expiry_date = models.IntegerField(blank=True, null=True, help_text="The Linux Time Epoch at which the sms magic link will expire")
    magic_link_email = models.CharField(max_length=100, blank=True, null=True, help_text="The magic link for email access for TFA")
    magic_link_sms = models.CharField(max_length=100, blank=True, null=True, help_text="The magic link for sms access for TFA")
    sms_resend_attempts = models.IntegerField(default=0, blank=True, null=True, help_text="The amount of times the sms code has been resent")
    sms_resend_attempts_expiry_date = models.IntegerField(default=0, blank=True, null=True, help_text="The Linux Epoch Time after which a user can send sms's again after 3 sends")

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.

        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side

        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'email',
            'mobile_number',
            'add_phone_number',
        )

    class Meta:
        db_table = 'USER_DETAILS'


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('login_id', 'email', 'mobile_number', 'add_phone_number', 'email_expiry_date', 'sms_expiry_date',
                  'magic_link_email', 'magic_link_sms', 'sms_resend_attempts', 'sms_resend_attempts_expiry_date', 'application_id')

    def get_summary_table(self):
        data = self.data
        return [
            {"title": "Your sign in details", "id": data['login_id']},
            {"name": "Email",
             "value": data['email'],
             'pk': data['login_id'],
             "reverse": "Change-Email"},
            {"name": "Mobile phone number",
             "value": data['mobile_number'],
             'pk': data['login_id'],
             "reverse": "Phone-Number"},
            {"name": "Alternative phone number",
             "value": data['add_phone_number'],
             'pk': data['login_id'],
             "reverse": "Phone-Number"}
        ]
