FAVOURITE_SESSION_ID = 'favourite_places'


def get_favourite_place_ids(request):
    return request.session.get(FAVOURITE_SESSION_ID, [])


def add_favourite_place(request, place_id):
    favourite_places = get_favourite_place_ids(request)

    if place_id not in favourite_places:
        favourite_places.insert(0, place_id)

    request.session[FAVOURITE_SESSION_ID] = favourite_places
    request.session.modified = True


def delete_favourite_place(request, place_id):
    favourite_places = get_favourite_place_ids(request)

    if place_id in favourite_places:
        favourite_places.remove(place_id)

    request.session[FAVOURITE_SESSION_ID] = favourite_places
    request.session.modified = True
