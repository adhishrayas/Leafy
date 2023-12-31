# Generated by Django 4.2.7 on 2023-12-05 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Authmodules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Address_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('Address_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('City', models.CharField(blank=True, max_length=255, null=True)),
                ('State', models.CharField(blank=True, max_length=255, null=True)),
                ('Pin_code', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
