# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-05 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('login_id', models.UUIDField(default=uuid.uuid4, help_text='Unique UUID4 Identifier', primary_key=True, serialize=False)),
                ('application_id', models.UUIDField(db_column='application_id')),
                ('email', models.CharField(blank=True, help_text='The Email Address of the applicant, using the following regex: ^(07\\d{8,12}|447\\d{7,11}|00447\\d{7,11}|\\+447\\d{7,11})$', max_length=100)),
                ('mobile_number', models.CharField(blank=True, help_text="The mobile number of the applicant, using following regex: ^([a-zA-Z0-9_\\-\\.']+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$", max_length=20)),
                ('add_phone_number', models.CharField(blank=True, help_text="The additional mobile number of the applicant, using following regex: ^([a-zA-Z0-9_\\-\\.']+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$", max_length=20)),
                ('email_expiry_date', models.IntegerField(blank=True, help_text='The Linux Time Epoch at which the email magic link will expire', null=True)),
                ('sms_expiry_date', models.IntegerField(blank=True, help_text='The Linux Time Epoch at which the sms magic link will expire', null=True)),
                ('magic_link_email', models.CharField(blank=True, help_text='The magic link for email access for TFA', max_length=100, null=True)),
                ('magic_link_sms', models.CharField(blank=True, help_text='The magic link for sms access for TFA', max_length=100, null=True)),
                ('sms_resend_attempts', models.IntegerField(blank=True, default=0, help_text='The amount of times the sms code has been resent', null=True)),
                ('sms_resend_attempts_expiry_date', models.IntegerField(blank=True, default=0, help_text="The Linux Epoch Time after which a user can send sms's again after 3 sends", null=True)),
            ],
            options={
                'db_table': 'USER_DETAILS',
            },
        ),
    ]
