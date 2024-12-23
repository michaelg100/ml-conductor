# Generated by Django 5.1.2 on 2024-11-04 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_model_registry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelexpirementmetrics',
            name='feature_set',
            field=models.JSONField(blank=list, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='modelexpirementmetrics',
            name='metrics',
            field=models.JSONField(blank=dict, default=dict, null=True),
        ),
    ]
