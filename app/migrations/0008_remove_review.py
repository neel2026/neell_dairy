# Generated manually to remove Review model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_review'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ] 