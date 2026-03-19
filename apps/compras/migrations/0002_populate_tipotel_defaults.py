from django.db import migrations


def create_tipotel_defaults(apps, schema_editor):
    TipoTel = apps.get_model("compras", "TipoTel")
    defaults = [
        "RESIDENCIAL",
        "CELULAR",
        "FAX",
        "TRABAJO",
        "EMERGENCIA",
        "RESPONSABLE",
    ]
    for tipo in defaults:
        TipoTel.objects.get_or_create(tipo=tipo)


class Migration(migrations.Migration):

    dependencies = [
        ("compras", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_tipotel_defaults, migrations.RunPython.noop),
    ]

