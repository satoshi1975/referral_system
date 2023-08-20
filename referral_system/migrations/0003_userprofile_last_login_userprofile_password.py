# Generated by Django 4.2.4 on 2023-08-19 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0002_referral'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(default=None, max_length=128),
        ),
    ]