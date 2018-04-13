# Generated by Django 2.0.4 on 2018-04-13 14:33

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models

import gnosis_safe_push_service.safe.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('push_token', models.CharField(max_length=150, unique=True, verbose_name='push_token')),
                ('owner', models.CharField(max_length=42, primary_key=True, serialize=False, validators=[gnosis_safe_push_service.safe.models.validate_checksumed_address], verbose_name='owner')),
            ],
            options={
                'verbose_name': 'device',
                'verbose_name_plural': 'devices',
            },
        ),
        migrations.CreateModel(
            name='DevicePair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('authorized_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorized_devices', to='safe.Device')),
                ('authorizing_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorizing_devices', to='safe.Device')),
            ],
            options={
                'verbose_name': 'device pair',
                'verbose_name_plural': 'device pairs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='devicepair',
            unique_together={('authorizing_device', 'authorized_device')},
        ),
    ]
