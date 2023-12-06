# Generated by Django 4.2.7 on 2023-12-05 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('Address_line', models.CharField(max_length=255)),
                ('City', models.CharField(max_length=255)),
                ('State', models.CharField(max_length=255)),
                ('Pin_code', models.IntegerField(max_length=6)),
                ('Contact_no', models.IntegerField(max_length=10)),
                ('Shop_icon', models.ImageField(blank=True, null=True, upload_to='shop_icons/')),
                ('Customer_no', models.IntegerField(default=0)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]