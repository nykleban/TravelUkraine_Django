from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render

from favourite_app.favourite import get_favourite_place_ids
from places_app.forms.place_form import PlaceForm
from places_app.models import Place

MAX_PLACE_IMAGES = 10


def save_place_gallery_images(place, images):
    current_images = list(place.gallery_images or [])
    remaining_count = MAX_PLACE_IMAGES - len(current_images)
    saved_images = []

    for image in images[:remaining_count]:
        image_path = default_storage.save(f'place_images/{image.name}', image)
        saved_images.append(image_path)

    if saved_images:
        place.gallery_images = current_images + saved_images
        place.save(update_fields=['gallery_images'])

    return len(images) > remaining_count


def delete_place_gallery_images(place, images_to_delete):
    selected_images = set(images_to_delete)
    current_images = list(place.gallery_images or [])
    deleted_count = 0
    new_images = []

    for image_path in current_images:
        if image_path in selected_images:
            if default_storage.exists(image_path):
                default_storage.delete(image_path)
            deleted_count += 1
        else:
            new_images.append(image_path)

    if deleted_count:
        place.gallery_images = new_images
        place.save(update_fields=['gallery_images'])

    return deleted_count


def get_place_gallery_images(place):
    return [
        {
            'path': image_path,
            'url': default_storage.url(image_path),
        }
        for image_path in place.gallery_images
        if image_path
    ]


def index(request):
    return render(request, 'index.html')


def place_list(request):
    places = Place.objects.all()
    return render(request, 'places/place_list.html', {'places': places})


def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    return render(request, 'places/place_detail.html', {
        'place': place,
        'gallery_image_urls': place.gallery_image_urls,
        'is_favourite': place.id in get_favourite_place_ids(request),
    })


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
        messages.error(request, 'Місце видалено успішно!')

    return redirect('admin_places')


def create_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save()
            too_many_images = save_place_gallery_images(place, request.FILES.getlist('gallery_images'))

            if too_many_images:
                messages.warning(request, 'Збережено тільки перші 10 фото для цього місця.')

            messages.success(request, 'Місце додано успішно!')
            return redirect('admin_places')
    else:
        form = PlaceForm()

    return render(request, 'places/create_place.html', {'form': form})


def update_place(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    return_url = request.GET.get('return_url')

    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            place = form.save()
            deleted_count = delete_place_gallery_images(
                place,
                request.POST.getlist('delete_gallery_images'),
            )
            too_many_images = save_place_gallery_images(place, request.FILES.getlist('gallery_images'))

            if deleted_count:
                messages.success(request, f'Видалено фото: {deleted_count}.')

            if too_many_images:
                messages.warning(request, 'Збережено тільки перші 10 фото для цього місця.')

            messages.success(request, 'Місце оновлено успішно!')
            if return_url:
                return redirect(return_url)

            return redirect('admin_places')
    else:
        form = PlaceForm(instance=place)

    return render(request, 'places/update_place.html', {
        'form': form,
        'place': place,
        'gallery_images': get_place_gallery_images(place),
    })
