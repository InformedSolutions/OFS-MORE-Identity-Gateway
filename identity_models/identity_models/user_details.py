import os
from uuid import uuid4

from django.contrib.sites import requests
from django.core import serializers
from django.db import models


class ApiCalls(models.Manager):

    identity_prefix = os.environ.get('APP_IDENTITY_URL')

    def get_record(self, email=None, pk=None, magic_link=None):
        if email != None:
            query_url = self.identity_prefix + '/api/v1/email' + email
        if pk != None:
            query_url = self.identity_prefix + '/api/v1/user' + pk
        if magic_link != None:
            query_url = self.identity_prefix + '/api/v1/magic_link' + magic_link

        response = requests.get(query_url)

        print(response)




    def __deserialize(self):
        user_generator = serializers.json.Deserializer(self.response.POST['data'])


class UserDetails(models.Model):
    """
    login_id:
    Test
    """
    # Managers
    objects = models.Manager()
    api = ApiCalls()

    login_id = models.UUIDField(primary_key=True, default=uuid4, help_text="Unique UUID4 Identifier")
    #application_id = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='application_id', default=uuid4)
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