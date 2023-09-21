# Generated by Django 4.2.5 on 2023-09-21 02:13

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('activated_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_months', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('expiration_date', models.DateTimeField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.subscriptionplan')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('start_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('business_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.businessaccount')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.subscriptionplan')),
            ],
        ),
        migrations.AddField(
            model_name='businessaccount',
            name='subscription_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.subscriptionticket'),
        ),
        migrations.CreateModel(
            name='AccountProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=20)),
                ('full_name', models.CharField(blank=True, max_length=60)),
                ('phone', models.CharField(blank=True, max_length=14)),
                ('address', models.CharField(blank=True, max_length=160)),
                ('description', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(choices=[('benue', 'Benue')], max_length=50, null=True)),
                ('lga', models.CharField(choices=[('gboko', 'Gboko'), ('kwande', 'Kwande'), ('katsina-ala', 'Katsina-Ala')], max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', imagekit.models.fields.ProcessedImageField(default='avatar.jpg', upload_to='profile_images', validators=[accounts.models.FileExtensionValidator(['jpeg', 'jpg', 'gif', 'png'])])),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.businessaccount')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
