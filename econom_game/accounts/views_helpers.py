from django.core.urlresolvers import reverse
from django.urls.exceptions import NoReverseMatch


def get_user_allowed_urls(request):
    """User allowed urls getting

    The "KEY":
        User's groups permission codenames equals to urls 'name' parameters
        in project urls configuration file.

    How is function work:
        1. Get user groups
        2. Get groups permissions
        3. Try to reverse permissions codenames
        4. Add to list if success

    """
    permission_codenames = []

    for group in request.user.groups.all():
        for permission in group.permissions.all():
            permission_codenames.append(permission.codename)

    user_allowed_urls = []

    for permission_codename in permission_codenames:
        try:
            url = reverse(permission_codename)
        except NoReverseMatch:
            pass
        else:
            user_allowed_urls.append(url)

    return user_allowed_urls
