# Generated by Django 2.0.3 on 2018-04-17 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0006_auto_20180417_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tube',
            name='biosample',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sample.BioSample'),
        ),
    ]
