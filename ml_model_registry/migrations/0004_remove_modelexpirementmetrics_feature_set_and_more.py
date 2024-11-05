# Generated by Django 5.1.2 on 2024-11-05 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_model_registry', '0003_alter_modelexpirementmetrics_target_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelexpirementmetrics',
            name='feature_set',
        ),
        migrations.AddField(
            model_name='modelmetadata',
            name='feature_set',
            field=models.JSONField(blank=list, default=list, null=True),
        ),
        migrations.AddField(
            model_name='modelmetadata',
            name='model_type',
            field=models.CharField(choices=[('TENSORFLOW', 'Tensorflow'), ('PYTORCH', 'Pytorch'), ('SCIKIT', 'Scikit')], default='SCIKIT', max_length=250),
        ),
    ]