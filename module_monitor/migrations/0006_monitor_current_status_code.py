# Generated by Django 2.1.2 on 2018-12-16 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_monitor', '0005_auto_20181212_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='current_status_code',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]