# Generated by Django 5.1 on 2025-01-27 06:10

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Hotel',
                'verbose_name_plural': 'Hotels',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('capacity', models.IntegerField(default=1, verbose_name='Capacity')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='core.hotel', verbose_name='Hotel')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('start_at', models.DateTimeField(verbose_name='Start-at')),
                ('end_at', models.DateTimeField(verbose_name='End-at')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Guest')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='core.room', verbose_name='Room')),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('end_at__gt', models.F('start_at'))), name='end_at_after_start_at'), models.UniqueConstraint(fields=('room', 'start_at', 'end_at'), name='unique_reservation_per_room')],
            },
        ),
    ]
