# Generated by Django 2.1.2 on 2019-11-10 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('status_code', models.CharField(max_length=100)),
                ('current_status_code', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_execution', models.DateTimeField(blank=True, null=True)),
                ('last_trouble', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(blank=True, null=True)),
                ('is_online', models.BooleanField(blank=True, null=True)),
            ],
        ),
    ]
