# Generated by Django 3.0 on 2019-12-29 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20191229_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='page',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
