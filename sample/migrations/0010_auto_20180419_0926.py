# Generated by Django 2.0.3 on 2018-04-19 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0009_auto_20180417_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='tubes_in_a_row',
            field=models.IntegerField(default=6, help_text='How many tubes fit in one row of the box'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='tubes_in_a_row',
            field=models.IntegerField(default=6, help_text='How many tubes fit in one row of the box'),
            preserve_default=False,
        ),
    ]
