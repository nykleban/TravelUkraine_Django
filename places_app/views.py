from django.shortcuts import get_object_or_404, redirect, render
from places_app.models import Place
from places_app.forms.place_form import PlaceForm

def index(request):
    return render(request, 'index.html')


def place_list(request):
    places = Place.objects.all()
    return render(request, 'places/place_list.html', {'places': places})


def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    return render(request, 'places/place_detail.html', {'place': place})


def search(request):
    query = request.GET.get('q', '')
    days = request.GET.get('days', '')

    places = Place.objects.all()

    if query:
        places = places.filter(name__icontains=query)

    if days.isdigit():
        days_number = int(days)

        places = places.filter(
            ideal_days_for_rest__gte=days_number - 2,
            ideal_days_for_rest__lte=days_number + 2,
        )

    return render(request, 'places/search.html', {
        'places': places,
        'query': query,
        'days': days,
        'is_filter_used': bool(query or days),
    })


def admin_places(request):
    places = Place.objects.all()
    return render(request, 'places/admin_places.html', {'places': places})


def delete_place(request, place_id):
    place = get_object_or_404(Place, pk=place_id)

    if request.method == 'POST':
        place.delete()

    return redirect('admin_places')


def create_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_places')
    else:
        form = PlaceForm()

    return render(request, 'places/create_place.html', {'form': form})


def update_place(request, place_id):
    place = get_object_or_404(Place, pk=place_id)

    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            return redirect('admin_places')
    else:
        form = PlaceForm(instance=place)

    return render(request, 'places/update_place.html', {'form': form,'place': place})

