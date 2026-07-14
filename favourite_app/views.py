from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from favourite_app.favourite import (
    add_favourite_place,
    delete_favourite_place,
    get_favourite_place_ids,
)
from places_app.models import Place


def favourite_list(request):
    favourite_ids = get_favourite_place_ids(request)
    places = Place.objects.filter(id__in=favourite_ids)
    places_by_id = {place.id: place for place in places}
    favourite_places = [
        places_by_id[place_id]
        for place_id in favourite_ids
        if place_id in places_by_id
    ]

    return render(request, 'favourite/index.html', {
        'favourite_places': favourite_places,
    })


def add_to_favourite(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    add_favourite_place(request, place.id)
    messages.success(request, 'Місце додано в обране.')

    return redirect(request.GET.get('return_url') or 'favourite_list')


def delete_from_favourite(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    delete_favourite_place(request, place.id)
    messages.error(request, 'Місце прибрано з обраного.')

    return redirect(request.GET.get('return_url') or 'favourite_list')
