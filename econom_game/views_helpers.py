from teams.models import Team


def is_in_database(new_object, queryset):
    database = queryset.objects.all()
    if new_object in database:
        return True
    return False
