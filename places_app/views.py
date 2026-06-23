from django.shortcuts import get_object_or_404, redirect, render
from places_app.models import Place
from places_app.forms.place_form import PlaceForm

places_hardcoded = [
    {
        'id': 1,
        'name': 'Карпати',
        'description': 'Гори, ліси, водоспади та маршрути для активної подорожі.',
        'region': 'Івано-Франківська область',
        'image_url': 'https://th.bing.com/th/id/R.474abf4ee42434d69383faaaca8a88d9?rik=3cBY6f%2f4hDiXMA&riu=http%3a%2f%2fbm.img.com.ua%2fberlin%2fstorage%2forig%2f3%2fbd%2f62c5ac203d7cb401f3ddd5bfd263abd3.jpg&ehk=zHohUxoHAhmMugUi67ERV7KoW9kCrdwJWvfprVfIjQQ%3d&risl=&pid=ImgRaw&r=0',
        'created_at': '07.06.2026',
    },
    {
        'id': 2,
        'name': 'Київ',
        'description': 'Столиця з історичними місцями, парками, музеями та набережною.',
        'region': 'Київ',
        'image_url': 'https://tse1.explicit.bing.net/th/id/OIP.acyQch4CKD4glOlgqyXukQHaE7?r=0&cb=thfvnextfalcon2&w=700&h=466&rs=1&pid=ImgDetMain&o=7&rm=3',
        'created_at': '05.06.2026',
    },
    {
        'id': 3,
        'name': 'Львів',
        'description': 'Старе місто, архітектура, кавові традиції та атмосферні вулиці.',
        'region': 'Львівська область',
        'image_url': 'https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=900&q=80',
        'created_at': '01.06.2026',
    },
    {
        'id': 4,
        'name': 'Одеса',
        'description': 'Морське місто з пляжами, портом, бульварами та південним настроєм.',
        'region': 'Одеська область',
        'image_url': 'https://ecolines.net/storage/offers/dWXywv9OxHtN0wHq5Oe8WZRDqgfnT9-metaT2Rlc2EuanBn-.jpg',
        'created_at': '05.05.2026',
    },
    {
        'id': 5,
        'name': 'Кам’янець-Подільський',
        'description': 'Місто з відомою фортецею, каньйоном і красивими оглядовими місцями.',
        'region': 'Хмельницька область',
        'image_url': 'https://karpaty.love/uploads/posts/2017-12/1513090759_vyd-na-kamjanec-podilsku-fortecju.jpg',
        'created_at': '08.04.2026',
    },
]


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
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_places')
    else:
        form = PlaceForm()

    return render(request, 'places/create_place.html', {'form': form})
