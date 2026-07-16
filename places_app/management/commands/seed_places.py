from pathlib import Path

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from places_app.models import Place


SEED_PLACES = [
    {
        'id': 1,
        'name': 'Карпати',
        'description': 'Гори, ліси, водоспади та маршрути для активної подорожі.',
        'region': 'Івано-Франківська область',
        'ideal_days_for_rest': 5,
        'best_season': 'summer',
        'image_file': 'carpathians.jpg',
    },
    {
        'id': 2,
        'name': 'Київ',
        'description': 'Столиця з історичними місцями, парками, музеями та набережною.',
        'region': 'Київ',
        'ideal_days_for_rest': 2,
        'best_season': 'any',
        'image_file': 'kyiv.jpg',
    },
    {
        'id': 3,
        'name': 'Львів',
        'description': 'Старе місто, архітектура, кавові традиції та атмосферні вулиці.',
        'region': 'Львівська область',
        'ideal_days_for_rest': 2,
        'best_season': 'any',
        'image_file': 'lviv.jpeg',
    },
    {
        'id': 4,
        'name': 'Одеса',
        'description': 'Морське місто з пляжами, портом, бульварами та південним настроєм.',
        'region': 'Одеська область',
        'ideal_days_for_rest': 3,
        'best_season': 'summer',
        'image_file': 'odesa.webp',
    },
    {
        'id': 5,
        'name': 'Кам’янець-Подільський',
        'description': 'Місто з відомою фортецею, каньйоном і красивими оглядовими місцями.',
        'region': 'Хмельницька область',
        'ideal_days_for_rest': 1,
        'best_season': 'spring',
        'image_file': 'kamianets.jpg',
    },
    {
        'id': 6,
        'name': 'Чернівці',
        'description': 'Місто з красивою архітектурою, затишними вулицями та відомим університетом.',
        'region': 'Чернівецька область',
        'ideal_days_for_rest': 2,
        'best_season': 'autumn',
        'image_file': 'chernivtsi.jpg',
    },
    {
        'id': 7,
        'name': 'Верховина',
        'description': 'Гірська локація з гуцульською культурою, музеями, дерев’яними садибами та краєвидами Карпат.',
        'region': 'Івано-Франківська область',
        'ideal_days_for_rest': 3,
        'best_season': 'summer',
        'image_file': 'verkhovyna.webp',
    },
    {
        'id': 8,
        'name': 'Свидовецький хребет',
        'description': 'Карпатський маршрут для любителів гір, панорамних полонин, туманних схилів і довгих прогулянок.',
        'region': 'Закарпатська область',
        'ideal_days_for_rest': 4,
        'best_season': 'autumn',
        'image_file': 'svydovets.jpg',
    },
    {
        'id': 9,
        'name': 'Майдан Незалежності',
        'description': 'Відома центральна площа України з монументами, фонтанами та важливим історичним значенням.',
        'region': 'Київ',
        'ideal_days_for_rest': 1,
        'best_season': 'any',
        'image_file': 'maidan.jpg',
    },
]


class Command(BaseCommand):
    help = 'Create base TravelUkraine places and upload default images if needed.'

    def handle(self, *args, **options):
        seed_dir = Path(__file__).resolve().parents[2] / 'seed_images'

        for place_data in SEED_PLACES:
            place_defaults = place_data.copy()
            image_file = place_defaults.pop('image_file')
            place, created = Place.objects.get_or_create(
                id=place_defaults['id'],
                defaults=place_defaults,
            )

            storage_path = f'place_images/seed/{image_file}'
            local_image_path = seed_dir / image_file

            if not default_storage.exists(storage_path):
                with local_image_path.open('rb') as image:
                    default_storage.save(storage_path, File(image))

            has_gallery_files = any(
                default_storage.exists(image_path)
                for image_path in place.gallery_images
            )

            if not has_gallery_files:
                place.gallery_images = [storage_path]
                place.save(update_fields=['gallery_images'])

            status = 'created' if created else 'checked'
            self.stdout.write(self.style.SUCCESS(f'{status}: place #{place.id}'))
