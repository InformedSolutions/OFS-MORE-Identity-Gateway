from uuid import uuid4

from rest_framework import serializers
from django.db import models


class UserDetails(models.Model):
    """
    login_id:
    Test
    """
    APP_TYPE = (
        ('CHILDMINDER', 'CHILDMINDER'),
        ('NANNY', 'NANNY'),
        ('NURSERY', 'NURSERY'),
        ('SOCIAL_CARE', 'SOCIAL_CARE')
    )
    # Managers
    objects = models.Manager()

    login_id = models.UUIDField(primary_key=True, default=uuid4, help_text="Unique UUID4 Identifier")
    application_id = models.UUIDField(db_column='application_id')
    email = models.CharField(max_length=100, blank=True, help_text="The Email Address of the applicant, using the following regex:"
                                                                   " ^(07\d{8,12}|447\d{7,11}|00447\d{7,11}|\+447\d{7,11})$")
    change_email = models.CharField(max_length=100, blank=True,
                             help_text="The Updated Email Address of the applicant, using the following regex:"
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
    service = models.CharField(choices=APP_TYPE, max_length=50, blank=True)

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
                  'magic_link_email', 'magic_link_sms', 'sms_resend_attempts', 'sms_resend_attempts_expiry_date', 'application_id', 'change_email', 'service')

    def get_summary_table(self):
        data = self.data
        return [
            {"title": "Your sign in details", "id": data['login_id']},
            {"name": "Your email",
             "value": data['email'],
             'pk': data['login_id'],
             "reverse": "Change-Email",
             "change_link_description": "your email"},
            {"name": "Your mobile number",
             "value": data['mobile_number'],
             'pk': data['login_id'],
             "reverse": "Phone-Number",
             "change_link_description": "your mobile number"},
            {"name": "Other phone number",
             "value": data['add_phone_number'],
             'pk': data['login_id'],
             "reverse": "Phone-Number",
             "change_link_description": "your other phone number"}
        ]
