# Generated by Django 5.1.2 on 2024-11-05 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_model_registry', '0004_remove_modelexpirementmetrics_feature_set_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelmetadata',
            name='feature_set',
            field=models.JSONField(blank=dict, default=dict, null=True),
        ),
    ]
