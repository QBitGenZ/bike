# Generated by Django 5.0.3 on 2024-03-20 07:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bicycle', '0003_remove_bicycle_price_bicycletype_price'),
        ('transaction_location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bicycle',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='transaction_location.transaction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bicycle',
            name='status',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bicycle',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bicycles', to='bicycle.bicycletype'),
        ),
    ]
