from django.core.urlresolvers import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth.models import Permission


def get_user_allowed_urls(request):
    """User allowed urls getting

    The "KEY":
        User's permission codenames equals to urls 'name' parameters
        in project urls configuration file.

    How is function work:
        1. Get user permissions
        3. Try to reverse permissions codenames
        4. Add to list if success

    """
    user_allowed_urls = []

    if not request.user.is_authenticated():
        return user_allowed_urls

    permission_codenames = []

    permissions = Permission.objects.filter(user=request.user)
    for permission in permissions:
        permission_codenames.append(permission.codename)

    for permission_codename in permission_codenames:
        try:
            url = reverse(permission_codename)
        except NoReverseMatch:
            pass
        else:
            user_allowed_urls.append(url)

    return user_allowed_urls
