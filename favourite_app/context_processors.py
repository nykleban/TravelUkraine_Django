from favourite_app.favourite import get_favourite_place_ids


def favourite_count(request):
    return {
        'favourite_count': len(get_favourite_place_ids(request)),
    }
