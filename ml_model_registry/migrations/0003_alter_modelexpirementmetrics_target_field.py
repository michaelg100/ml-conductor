# Generated by Django 5.1.2 on 2024-11-04 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_model_registry', '0002_alter_modelexpirementmetrics_feature_set_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelexpirementmetrics',
            name='target_field',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
