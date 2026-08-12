from django.db import migrations


GRUPOS_MUSCULARES = [
    "Peito",
    "Costas",
    "Ombro",
    "Bíceps",
    "Tríceps",
    "Antebraço",
    "Perna",
    "Glúteo",
    "Abdômen",
    "Panturrilha",
    "Trapézio",
    "Cardio",
]


def criar_grupos_musculares(apps, schema_editor):
    Grupo_muscular = apps.get_model('aparelhos', 'Grupo_muscular')
    for nome in GRUPOS_MUSCULARES:
        Grupo_muscular.objects.get_or_create(name=nome)


def remover_grupos_musculares(apps, schema_editor):
    Grupo_muscular = apps.get_model('aparelhos', 'Grupo_muscular')
    Grupo_muscular.objects.filter(name__in=GRUPOS_MUSCULARES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('aparelhos', '0009_aparelho_qr_code'),
    ]

    operations = [
        migrations.RunPython(criar_grupos_musculares, remover_grupos_musculares),
    ]