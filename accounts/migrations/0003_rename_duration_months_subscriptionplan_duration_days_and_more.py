# Generated by Django 4.2.5 on 2023-09-26 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_accountprofile_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriptionplan',
            old_name='duration_months',
            new_name='duration_days',
        ),
        migrations.AlterField(
            model_name='subscriptionplan',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='subscriptionplan',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
