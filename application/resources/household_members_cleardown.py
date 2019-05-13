from ..models.user_details import UserDetails


def run(*args):
    UserDetails.objects.filter(service='HOUSEHOLD_MEMBERS').delete()
