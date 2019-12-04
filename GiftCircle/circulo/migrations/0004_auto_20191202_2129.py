# Generated by Django 2.2.7 on 2019-12-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulo', '0003_persona_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='telefono',
            field=models.CharField(blank=True, default=None, max_length=15, null=True),
        ),
    ]
