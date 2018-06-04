from rest_framework import serializers
from identity_models.identity_models.user_details import UserDetails

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('login_id', 'email', 'mobile_number', 'add_phone_number', 'email_expiry_date', 'sms_expiry_date',
                  'magic_link_email', 'magic_link_sms', 'sms_resend_attempts', 'sms_resend_attempts_expiry_date')
