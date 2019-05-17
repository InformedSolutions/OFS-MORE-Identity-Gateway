import os

import django


def household_members_cleardown():
    from application.models import UserDetails

    UserDetails.objects.filter(service='NANNY').delete()


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('PROJECT_SETTINGS'))

    django.setup()

    household_members_cleardown()
